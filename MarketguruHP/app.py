import os
import hashlib
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import mysql.connector
from mysql.connector import pooling
from config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME
from init_db import init_database

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin frontend requests

# Ensure database and tables exist at startup
try:
    init_database()
except Exception as e:
    print(f"Database init warning: {e}")

# Initialize Connection Pool
try:
    db_pool = pooling.MySQLConnectionPool(
        pool_name="mg_pool",
        pool_size=10,
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    print("MySQL Connection Pool initialized successfully with size 10.")
except Exception as pool_err:
    print(f"Warning: Connection Pool initialization failed: {pool_err}")
    db_pool = None

def get_db_connection():
    if db_pool:
        return db_pool.get_connection()
    return mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

def query_db(query, args=(), one=False, commit=False):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, args)
    if commit:
        conn.commit()
        last_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return last_id
    
    rv = cursor.fetchall()
    cursor.close()
    conn.close()
    return (rv[0] if rv else None) if one else rv

def get_hash(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

@app.route('/api/ping', methods=['GET'])
def ping():
    return jsonify({"status": "ok"})

@app.route('/api/init', methods=['GET'])
def db_init_data():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM cars")
        cars = cursor.fetchall()
        # Format features from string to list
        for car in cars:
            if car['features']:
                car['features'] = [f.strip() for f in car['features'].split(',') if f.strip()]
            else:
                car['features'] = []
            # Map database field verified to true/false
            car['verified'] = bool(car['verified'])

        cursor.execute("SELECT * FROM leads")
        leads = cursor.fetchall()

        cursor.execute("SELECT * FROM enquiries")
        enquiries = cursor.fetchall()

        cursor.execute("SELECT * FROM customers")
        customers = cursor.fetchall()

        cursor.execute("SELECT * FROM followups")
        followups = cursor.fetchall()

        cursor.execute("SELECT * FROM revenue")
        revenue = cursor.fetchall()

        cursor.execute("SELECT * FROM staff")
        staff = cursor.fetchall()
        # Exclude password hashes from staff data
        for s in staff:
            if 'password' in s:
                del s['password']

        cursor.execute("SELECT * FROM wishlist")
        wishlist = cursor.fetchall()

        cursor.execute("SELECT * FROM subscriptions")
        subscriptions = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify({
            "status": "success",
            "cars": cars,
            "leads": leads,
            "enquiries": enquiries,
            "customers": customers,
            "followups": followups,
            "revenue": revenue,
            "staff": staff,
            "wishlist": wishlist,
            "subscriptions": subscriptions
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/cars', methods=['POST'])
def add_car():
    try:
        data = request.json
        name = data.get('name')
        year = int(data.get('year', 2020))
        price = data.get('price', '5.00')
        priceN = int(data.get('priceN', 500000))
        km = data.get('km', '30,000')
        fuel = data.get('fuel', 'Petrol')
        trans = data.get('trans', 'Manual')
        owner = data.get('owner', '1st')
        color = data.get('color', '#e8eef5')
        emoji = data.get('emoji', '🚗')
        city = data.get('city', 'Vadodara')
        description = data.get('desc', '')
        listed_by = data.get('listed_by')
        image = data.get('image', None)
        
        features_list = data.get('features', [])
        if isinstance(features_list, list):
            features = ", ".join(features_list)
        else:
            features = str(features_list)
            
        emi = data.get('emi')
        if not emi:
            # calculate a mock emi
            emi = f"{int(priceN * 0.019):,}"
            
        # Check if listed_by is a dealer or private
        user_type = data.get('user_type', 'private')
        if listed_by:
            if user_type == 'dealer':
                # Verify they are actually registered as a dealer
                is_dealer = query_db("SELECT id FROM dealers WHERE mobile = %s", (listed_by,), one=True)
                if not is_dealer:
                    return jsonify({"status": "error", "message": "Account is not registered as a dealer partner."}), 400
            else:
                # Individual seller: check active listing count
                active_count = query_db("SELECT COUNT(*) as count FROM cars WHERE listed_by = %s", (listed_by,), one=True)
                if active_count and active_count.get('count', 0) >= 1:
                    return jsonify({"status": "error", "message": "Individual sellers are limited to exactly 1 car listing."}), 400

        # Default verification
        verified = int(data.get('verified', 0))

        car_id = query_db(
            "INSERT INTO cars (name, year, price, priceN, km, fuel, trans, owner, color, emoji, image, verified, emi, city, description, features, listed_by) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (name, year, price, priceN, km, fuel, trans, owner, color, emoji, image, verified, emi, city, description, features, listed_by),
            commit=True
        )

        return jsonify({
            "status": "success",
            "car": {
                "id": car_id,
                "name": name,
                "year": year,
                "price": price,
                "priceN": priceN,
                "km": km,
                "fuel": fuel,
                "trans": trans,
                "owner": owner,
                "color": color,
                "emoji": emoji,
                "image": image,
                "verified": bool(verified),
                "emi": emi,
                "city": city,
                "desc": description,
                "features": features_list if isinstance(features_list, list) else [f.strip() for f in features.split(',') if f.strip()],
                "listed_by": listed_by
            }
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/cars/verify', methods=['POST'])
def verify_car():
    try:
        data = request.json
        car_id = int(data.get('car_id'))
        verified = int(data.get('verified', 0))

        query_db("UPDATE cars SET verified = %s WHERE id = %s", (verified, car_id), commit=True)
        return jsonify({"status": "success", "car_id": car_id, "verified": bool(verified)})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/cars/sold', methods=['POST'])
def sell_car_api():
    try:
        data = request.json
        car_id = int(data.get('car_id'))
        query_db("DELETE FROM cars WHERE id = %s", (car_id,), commit=True)
        return jsonify({"status": "success", "car_id": car_id})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/cars/by-user', methods=['POST'])
def get_cars_by_user():
    """Fetch all cars listed by a specific user, with flexible mobile number matching."""
    try:
        data = request.json
        mobile = str(data.get('mobile', '')).strip()
        # Normalize: strip +91 prefix and spaces for matching
        mobile_bare = mobile.lstrip('+').replace(' ', '').replace('-', '')
        if mobile_bare.startswith('91') and len(mobile_bare) == 12:
            mobile_bare = mobile_bare[2:]  # strip country code

        # Query with both formats: exact match and bare 10-digit
        cars = query_db(
            "SELECT * FROM cars WHERE listed_by = %s OR listed_by = %s OR listed_by = %s",
            (mobile, '+91' + mobile_bare, mobile_bare)
        )
        for car in cars:
            if car['features']:
                car['features'] = [f.strip() for f in car['features'].split(',') if f.strip()]
            else:
                car['features'] = []
            car['verified'] = bool(car['verified'])

        return jsonify({"status": "success", "cars": cars})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/cars/update', methods=['POST'])
def update_car():
    """Update a car listing's price, km, or description."""
    try:
        data = request.json
        car_id = int(data.get('car_id'))
        mobile = str(data.get('mobile', '')).strip()

        # Build dynamic update
        updates = []
        params = []
        if 'price' in data:
            updates.append('price = %s')
            params.append(str(data['price']))
        if 'priceN' in data:
            updates.append('priceN = %s')
            params.append(int(data['priceN']))
        if 'km' in data:
            updates.append('km = %s')
            params.append(str(data['km']))
        if 'description' in data:
            updates.append('description = %s')
            params.append(str(data['description']))

        if not updates:
            return jsonify({"status": "error", "message": "No fields to update"}), 400

        params.append(car_id)
        query_db(f"UPDATE cars SET {', '.join(updates)} WHERE id = %s", tuple(params), commit=True)
        return jsonify({"status": "success", "car_id": car_id})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/cars/delete', methods=['POST'])
def delete_car():
    """Delete/remove a car listing. Only the owner can delete their own listing."""
    try:
        data = request.json
        car_id = int(data.get('car_id'))
        mobile = str(data.get('mobile', '')).strip()

        # Normalize mobile for matching
        mobile_bare = mobile.lstrip('+').replace(' ', '').replace('-', '')
        if mobile_bare.startswith('91') and len(mobile_bare) == 12:
            mobile_bare = mobile_bare[2:]

        # Verify ownership first
        car = query_db(
            "SELECT id, listed_by FROM cars WHERE id = %s",
            (car_id,), one=True
        )
        if not car:
            return jsonify({"status": "error", "message": "Car not found"}), 404

        # Allow deletion if ownership matches OR mobile is empty (admin)
        owner = str(car.get('listed_by') or '').strip()
        owner_bare = owner.lstrip('+').replace(' ', '').replace('-', '')
        if owner_bare.startswith('91') and len(owner_bare) == 12:
            owner_bare = owner_bare[2:]

        if mobile and owner_bare and mobile_bare != owner_bare:
            return jsonify({"status": "error", "message": "Not authorized to delete this listing"}), 403

        query_db("DELETE FROM cars WHERE id = %s", (car_id,), commit=True)
        return jsonify({"status": "success", "car_id": car_id, "message": "Listing removed"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/leads', methods=['POST'])
def add_lead():
    try:
        data = request.json
        name = data.get('name')
        mobile = data.get('mobile')
        car = data.get('car')
        budget = data.get('budget', 'Any')
        source = data.get('source', 'Website')
        stage = data.get('stage', 'new')
        assigned = data.get('assigned', 'Rahul Sharma')
        date = data.get('date', 'Today')

        lead_id = query_db(
            "INSERT INTO leads (name, mobile, car, budget, source, stage, assigned, date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (name, mobile, car, budget, source, stage, assigned, date),
            commit=True
        )
        
        # Upsert Customer database record
        cust_exists = query_db("SELECT id FROM customers WHERE mobile = %s", (mobile,), one=True)
        if not cust_exists:
            query_db(
                "INSERT INTO customers (name, mobile, city, interests, purchases, last) VALUES (%s, %s, %s, %s, %s, %s)",
                (name, mobile, 'Vadodara', f"Interested in {car}", '0', 'Today'),
                commit=True
            )

        return jsonify({
            "status": "success",
            "lead": {
                "id": lead_id,
                "name": name,
                "mobile": mobile,
                "car": car,
                "budget": budget,
                "source": source,
                "stage": stage,
                "assigned": assigned,
                "date": date
            }
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/enquiries', methods=['POST'])
def add_enquiry():
    try:
        data = request.json
        name = data.get('name')
        mobile = data.get('mobile')
        car = data.get('car')
        query = data.get('query')
        date = data.get('date', 'Today')
        status = data.get('status', 'new')

        enquiry_id = query_db(
            "INSERT INTO enquiries (name, mobile, car, query, date, status) VALUES (%s, %s, %s, %s, %s, %s)",
            (name, mobile, car, query, date, status),
            commit=True
        )

        # Also push to CRM lead pipeline
        query_db(
            "INSERT INTO leads (name, mobile, car, budget, source, stage, assigned, date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (name, mobile, car, 'Any', 'Website', 'new', 'Rahul Sharma', 'Today'),
            commit=True
        )

        return jsonify({
            "status": "success",
            "enquiry": {
                "id": enquiry_id,
                "name": name,
                "mobile": mobile,
                "car": car,
                "query": query,
                "date": date,
                "status": status
            }
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/enquiries/resolve', methods=['POST'])
def resolve_enquiry():
    try:
        data = request.json
        name = data.get('name')

        query_db("UPDATE enquiries SET status = 'replied' WHERE name = %s", (name,), commit=True)
        return jsonify({"status": "success", "name": name})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/staff', methods=['POST'])
def add_staff():
    try:
        data = request.json
        name = data.get('name')
        email = data.get('email')
        role = data.get('role')
        dept = data.get('dept', 'Sales')
        status = data.get('status', 'active')
        last = data.get('last', 'Just now')
        password = get_hash('admin123')

        staff_id = query_db(
            "INSERT INTO staff (name, email, role, dept, status, last, password) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (name, email, role, dept, status, last, password),
            commit=True
        )

        return jsonify({
            "status": "success",
            "staff": {
                "id": staff_id,
                "name": name,
                "email": email,
                "role": role,
                "dept": dept,
                "status": status,
                "last": last
            }
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/auth/check-mobile', methods=['POST'])
def check_mobile():
    try:
        data = request.json
        mobile = data.get('mobile')
        role = data.get('role', 'individual')
        check_all = data.get('check_all', False)

        if check_all:
            res_d = query_db("SELECT id FROM dealers WHERE mobile = %s", (mobile,), one=True)
            res_c = query_db("SELECT id FROM customers WHERE mobile = %s", (mobile,), one=True)
            return jsonify({"status": "success", "exists": bool(res_d or res_c)})

        res_d = query_db("SELECT id FROM dealers WHERE mobile = %s", (mobile,), one=True)
        res_c = query_db("SELECT id FROM customers WHERE mobile = %s", (mobile,), one=True)

        if role == 'dealer':
            if res_d:
                return jsonify({"status": "success", "exists": True})
            elif res_c:
                return jsonify({"status": "success", "exists": False, "registered_role": "individual"})
            else:
                return jsonify({"status": "success", "exists": False, "registered_role": None})
        else:
            if res_c:
                return jsonify({"status": "success", "exists": True})
            elif res_d:
                return jsonify({"status": "success", "exists": False, "registered_role": "dealer"})
            else:
                return jsonify({"status": "success", "exists": False, "registered_role": None})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = request.json
        login_id = data.get('id')
        password = data.get('password')
        role = data.get('role', 'individual')

        # Check OTP login based on role
        if password == 'OTP_LOGIN':
            if role == 'dealer':
                dealer = query_db("SELECT * FROM dealers WHERE mobile = %s", (login_id,), one=True)
                if dealer:
                    return jsonify({
                        "status": "success",
                        "user": {
                            "name": dealer['dealership_name'],
                            "mobile": dealer['mobile'],
                            "email": dealer['email'],
                            "type": "dealer"
                        }
                    })
            else:
                indiv = query_db("SELECT * FROM customers WHERE mobile = %s", (login_id,), one=True)
                if indiv:
                    return jsonify({
                        "status": "success",
                        "user": {
                            "name": indiv['name'],
                            "mobile": indiv['mobile'],
                            "type": "private"
                        }
                    })

        hashed_pwd = get_hash(password)
        
        # Check dealers
        dealer = query_db("SELECT * FROM dealers WHERE (mobile = %s OR email = %s) AND password = %s", (login_id, login_id, hashed_pwd), one=True)
        if dealer:
            return jsonify({
                "status": "success",
                "user": {
                    "name": dealer['dealership_name'],
                    "mobile": dealer['mobile'],
                    "email": dealer['email'],
                    "type": "dealer"
                }
            })
        
        # Fallback to Staff verification in case admin logs in via standard window
        staff = query_db(
            "SELECT * FROM staff WHERE email = %s AND password = %s",
            (login_id, hashed_pwd),
            one=True
        )
        if staff:
            return jsonify({
                "status": "success",
                "user": {
                    "name": staff['name'],
                    "mobile": "0000000000",
                    "email": staff['email'],
                    "type": "admin"
                }
            })

        return jsonify({"status": "error", "message": "Incorrect details, please register."}), 401
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/auth/profile/update', methods=['POST'])
def update_profile():
    try:
        data = request.json
        mobile = data.get('mobile')
        new_name = data.get('name')
        new_email = data.get('email', '')
        new_city = data.get('city', '')
        user_type = data.get('type', 'private')

        if user_type == 'dealer':
            dealer = query_db("SELECT id FROM dealers WHERE mobile = %s", (mobile,), one=True)
            if dealer:
                query_db(
                    "UPDATE dealers SET dealership_name = %s, email = %s, city = %s WHERE mobile = %s",
                    (new_name, new_email, new_city, mobile),
                    commit=True
                )
                return jsonify({"status": "success", "message": "Dealer profile updated successfully."})
        else:
            customer = query_db("SELECT id FROM customers WHERE mobile = %s", (mobile,), one=True)
            if customer:
                query_db(
                    "UPDATE customers SET name = %s, city = %s WHERE mobile = %s",
                    (new_name, new_city, mobile),
                    commit=True
                )
                return jsonify({"status": "success", "message": "Customer profile updated successfully."})
        
        return jsonify({"status": "error", "message": "User not found."}), 404
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/auth/register', methods=['POST'])
def register():
    try:
        data = request.json
        mobile = data.get('mobile')
        account_type = data.get('account_type', 'private')

        # Check if mobile number is already registered in either table
        exists_dealer = query_db("SELECT id FROM dealers WHERE mobile = %s", (mobile,), one=True)
        exists_customer = query_db("SELECT id FROM customers WHERE mobile = %s", (mobile,), one=True)
        if exists_dealer or exists_customer:
            return jsonify({"status": "error", "message": f"Mobile number {mobile} is already registered on the platform."}), 400

        if account_type == 'dealer':
            dealership_name = data.get('dealership_name', '')
            address = data.get('address', '')
            state = data.get('state', '')
            city = data.get('city', '')
            email = data.get('email', '')
            password = data.get('password', '')
            hashed_pwd = get_hash(password)

            query_db(
                "INSERT INTO dealers (dealership_name, address, state, city, email, mobile, password) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (dealership_name, address, state, city, email, mobile, hashed_pwd),
                commit=True
            )
            return jsonify({
                "status": "success",
                "user": {
                    "name": dealership_name,
                    "mobile": mobile,
                    "email": email,
                    "type": "dealer"
                }
            })
        else:
            f_name = data.get('fName', '')
            l_name = data.get('lName', '')
            full_name = f"{f_name} {l_name}".strip()

            query_db(
                "INSERT INTO customers (name, mobile, city, interests, purchases, last) VALUES (%s, %s, %s, %s, %s, %s)",
                (full_name, mobile, '', '', '0', 'Today'),
                commit=True
            )
            return jsonify({
                "status": "success",
                "user": {
                    "name": full_name,
                    "mobile": mobile,
                    "type": "private"
                }
            })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/auth/admin-login', methods=['POST'])
def admin_login():
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')

        hashed_pwd = get_hash(password)
        staff = query_db(
            "SELECT * FROM staff WHERE email = %s AND password = %s",
            (email, hashed_pwd),
            one=True
        )

        if staff:
            return jsonify({
                "status": "success",
                "user": {
                    "name": staff['name'],
                    "email": staff['email'],
                    "role": staff['role'],
                    "type": "admin"
                }
            })

        return jsonify({"status": "error", "message": "Invalid Admin credentials"}), 401
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/subscription/activate', methods=['POST'])
def activate_sub():
    try:
        data = request.json
        mobile = data.get('user_mobile')
        
        import datetime
        expiry_date = (datetime.date.today() + datetime.timedelta(days=30)).strftime('%d %b %Y')

        # Insert or update
        sub_exists = query_db("SELECT id FROM subscriptions WHERE user_mobile = %s", (mobile,), one=True)
        if sub_exists:
            query_db(
                "UPDATE subscriptions SET status = 'active', expiry = %s WHERE user_mobile = %s",
                (expiry_date, mobile),
                commit=True
            )
        else:
            query_db(
                "INSERT INTO subscriptions (user_mobile, status, expiry) VALUES (%s, 'active', %s)",
                (mobile, expiry_date),
                commit=True
            )

        return jsonify({"status": "success", "user_mobile": mobile, "expiry": expiry_date})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/subscription/cancel', methods=['POST'])
def cancel_sub():
    try:
        data = request.json
        mobile = data.get('user_mobile')

        query_db(
            "UPDATE subscriptions SET status = 'inactive', expiry = NULL WHERE user_mobile = %s",
            (mobile,),
            commit=True
        )
        return jsonify({"status": "success", "user_mobile": mobile})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/wishlist/toggle', methods=['POST'])
def toggle_wishlist():
    try:
        data = request.json
        mobile = data.get('user_mobile')
        car_id = int(data.get('car_id'))

        exists = query_db(
            "SELECT id FROM wishlist WHERE user_mobile = %s AND car_id = %s",
            (mobile, car_id),
            one=True
        )

        if exists:
            query_db("DELETE FROM wishlist WHERE id = %s", (exists['id'],), commit=True)
            return jsonify({"status": "success", "added": False})
        else:
            query_db(
                "INSERT INTO wishlist (user_mobile, car_id) VALUES (%s, %s)",
                (mobile, car_id),
                commit=True
            )
            return jsonify({"status": "success", "added": True})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Serve static files for double-clicking logic
@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
