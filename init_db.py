import mysql.connector
import hashlib
from config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME

def get_hash(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def init_database():
    # Connect without database first to create it
    conn = mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    conn.commit()
    cursor.close()
    conn.close()

    # Reconnect to the database
    conn = mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    cursor = conn.cursor()

    # 1. Create tables


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cars (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100),
        year INT,
        price VARCHAR(20),
        priceN INT,
        km VARCHAR(50),
        fuel VARCHAR(20),
        trans VARCHAR(20),
        owner VARCHAR(20),
        color VARCHAR(20),
        emoji VARCHAR(20),
        image LONGTEXT,
        verified BOOLEAN,
        emi VARCHAR(20),
        city VARCHAR(50),
        description TEXT,
        features TEXT,
        listed_by VARCHAR(20),
        images LONGTEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS leads (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100),
        mobile VARCHAR(20),
        car VARCHAR(100),
        budget VARCHAR(50),
        source VARCHAR(50),
        stage VARCHAR(50),
        assigned VARCHAR(100),
        date VARCHAR(50)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS enquiries (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100),
        mobile VARCHAR(20),
        car VARCHAR(100),
        query TEXT,
        date VARCHAR(50),
        status VARCHAR(20)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100),
        mobile VARCHAR(20),
        city VARCHAR(50),
        interests VARCHAR(255),
        purchases VARCHAR(10),
        last VARCHAR(50)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS followups (
        id INT AUTO_INCREMENT PRIMARY KEY,
        customer VARCHAR(100),
        car VARCHAR(100),
        due VARCHAR(50),
        type VARCHAR(50),
        notes TEXT,
        status VARCHAR(20),
        assigned VARCHAR(100)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS revenue (
        id INT AUTO_INCREMENT PRIMARY KEY,
        date VARCHAR(50),
        car VARCHAR(100),
        buyer VARCHAR(100),
        sale VARCHAR(20),
        cost VARCHAR(20),
        profit VARCHAR(20),
        mode VARCHAR(50)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS staff (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100),
        email VARCHAR(100) UNIQUE,
        role VARCHAR(50),
        dept VARCHAR(50),
        status VARCHAR(20),
        last VARCHAR(50),
        password VARCHAR(255)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS wishlist (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_mobile VARCHAR(20),
        car_id INT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS subscriptions (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_mobile VARCHAR(20) UNIQUE,
        status VARCHAR(20),
        expiry VARCHAR(50)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS individuals (
        id INT AUTO_INCREMENT PRIMARY KEY,
        full_name VARCHAR(100),
        mobile VARCHAR(20) UNIQUE
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS dealers (
        id INT AUTO_INCREMENT PRIMARY KEY,
        dealership_name VARCHAR(100),
        address VARCHAR(255),
        state VARCHAR(50),
        city VARCHAR(50),
        email VARCHAR(100),
        mobile VARCHAR(20) UNIQUE,
        password VARCHAR(255)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS car_views (
        id INT AUTO_INCREMENT PRIMARY KEY,
        car_id INT,
        user_name VARCHAR(100),
        user_mobile VARCHAR(20),
        viewed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (car_id) REFERENCES cars(id) ON DELETE CASCADE
    )
    """)
    conn.commit()

    # 2. Seed data if tables are empty
    # Seed Staff
    cursor.execute("SELECT COUNT(*) FROM staff")
    if cursor.fetchone()[0] == 0:
        default_staff = [
            ('Rajesh Patel', 'rajesh@marketguruhp.in', 'Super Admin', 'Management', 'active', 'Just now', get_hash('admin123')),
            ('Rahul Sharma', 'rahul@marketguruhp.in', 'Sales Manager', 'Sales', 'active', '10 min ago', get_hash('admin123')),
            ('Priya Patel', 'priya@marketguruhp.in', 'Executive', 'Sales', 'active', '1 hr ago', get_hash('admin123')),
            ('Amit Joshi', 'amit@marketguruhp.in', 'Executive', 'Sales', 'active', '2 hr ago', get_hash('admin123')),
            ('Neha Verma', 'neha@marketguruhp.in', 'Finance', 'Finance', 'active', 'Yesterday', get_hash('admin123')),
            ('Deepak Shah', 'deepak@marketguruhp.in', 'Executive', 'Sales', 'inactive', '3 days ago', get_hash('admin123'))
        ]
        cursor.executemany(
            "INSERT INTO staff (name, email, role, dept, status, last, password) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            default_staff
        )
        print("Staff seeded.")

    # Seed Cars
    cursor.execute("SELECT COUNT(*) FROM cars")
    if cursor.fetchone()[0] == 0:
        default_cars = [
            (1, 'Maruti Swift VXi', 2021, '5.20', 520000, '32,000', 'Petrol', 'Manual', '1st', '#e8eef5', '🚗', True, '9,800', 'Vadodara', 'Well maintained single owner car. All service records available.', 'Power Windows, Airbags, ABS, Bluetooth', None),
            (2, 'Hyundai i20 Asta', 2020, '6.80', 680000, '45,000', 'Petrol', 'Manual', '1st', '#eef0f5', '🚙', True, '12,800', 'Vadodara', 'Top variant with sunroof. No accidents. Genuine seller.', 'Sunroof, Rear Camera, ABS, Airbags', None),
            (3, 'Honda City ZX CVT', 2019, '9.50', 950000, '58,000', 'Petrol', 'Automatic', '2nd', '#f0eef5', '🚘', False, '17,900', 'Vadodara', 'Premium sedan in excellent condition. Service at Honda authorized center.', 'Cruise Control, Leather Seats, Lane Watch, Android Auto', None),
            (4, 'Tata Nexon XZ+ Dark', 2022, '11.20', 1120000, '22,000', 'Diesel', 'Manual', '1st', '#eef5f0', '🛻', True, '21,100', 'Vadodara', 'Latest model in dark edition. Under warranty till 2027.', 'Panoramic Sunroof, iRA Connected, Harman Audio, 6 Airbags', None),
            (5, 'Kia Seltos HTX+ AT', 2021, '14.50', 1450000, '35,000', 'Petrol', 'Automatic', '1st', '#f5eef0', '🏎️', True, '27,300', 'Vadodara', 'Premium SUV with all luxury features. Full service history.', 'Bose Audio, Ventilated Seats, 10.25\" Screen, Drive Modes', None),
            (6, 'Maruti Ertiga VXi CNG', 2020, '7.90', 790000, '52,000', 'CNG', 'Manual', '1st', '#eff5ee', '🚐', False, '14,900', 'Vadodara', 'Factory fitted CNG. Economy family car. Reasonable mileage.', '7 Seater, Smart Play, Rear AC Vents, CNG Kit', None),
            (7, 'Toyota Fortuner 2.8 4x4', 2020, '28.50', 2850000, '48,000', 'Diesel', 'Automatic', '1st', '#f5f0ee', '🚙', True, '53,700', 'Surat', 'Beast condition. All options available. Must see.', '4x4, Multi Terrain Select, JBL Audio, Power Tailgate', None),
            (8, 'Mahindra Thar LX 4x4', 2022, '17.80', 1780000, '15,000', 'Diesel', 'Automatic', '1st', '#eef2f5', '🛞', True, '33,500', 'Vadodara', 'Almost new. Diesel automatic with hard top. All accessories.', '4x4, Hardtop, Touchscreen, Rock Mode', None)
        ]
        cursor.executemany(
            "INSERT INTO cars (id, name, year, price, priceN, km, fuel, trans, owner, color, emoji, verified, emi, city, description, features, listed_by) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            default_cars
        )
        print("Cars seeded.")

    # Seed Leads
    cursor.execute("SELECT COUNT(*) FROM leads")
    if cursor.fetchone()[0] == 0:
        default_leads = [
            ('Arjun Mehta', '98765-43210', 'Maruti Swift', '4-6L', 'Website', 'negotiation', 'Rahul S.', '12 Jun'),
            ('Priya Shah', '87654-32109', 'Honda City', '8-12L', 'Walk-in', 'test-drive', 'Priya P.', '12 Jun'),
            ('Kiran Patel', '76543-21098', 'Toyota Innova', '15-20L', 'Referral', 'new', 'Rahul S.', '11 Jun'),
            ('Suresh Joshi', '65432-10987', 'Tata Nexon', '10-12L', 'Social', 'new', 'Amit J.', '11 Jun'),
            ('Meera Trivedi', '54321-09876', 'Hyundai Creta', '8-10L', 'Website', 'contacted', 'Priya P.', '10 Jun'),
            ('Rahul Gupta', '43210-98765', 'Kia Seltos', '12-16L', 'Phone', 'won', 'Rahul S.', '9 Jun'),
            ('Anita Roy', '32109-87654', 'Maruti Baleno', '5-7L', 'Website', 'lost', 'Amit J.', '8 Jun')
        ]
        cursor.executemany(
            "INSERT INTO leads (name, mobile, car, budget, source, stage, assigned, date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            default_leads
        )
        print("Leads seeded.")

    # Seed Enquiries
    cursor.execute("SELECT COUNT(*) FROM enquiries")
    if cursor.fetchone()[0] == 0:
        default_enquiries = [
            ('Mohan Lal', '98765-XXXXX', 'Maruti Swift VXi 2021', 'Is first owner? Service history?', '12 Jun 2:30pm', 'new'),
            ('Sunita Patel', '98765-XXXXX', 'Honda City ZX', 'What is lowest price possible?', '12 Jun 1:15pm', 'new'),
            ('Vijay Shah', '98765-XXXXX', 'Tata Nexon XZ+', 'Still available? Can I test drive?', '11 Jun 4:00pm', 'replied'),
            ('Kavita Mehta', '98765-XXXXX', 'Toyota Fortuner', 'Any warranty left? Exchange possible?', '11 Jun 11:30am', 'replied'),
            ('Dilip Chauhan', '98765-XXXXX', 'Kia Seltos HTX', 'What accessories are included?', '10 Jun 3:45pm', 'closed')
        ]
        cursor.executemany(
            "INSERT INTO enquiries (name, mobile, car, query, date, status) VALUES (%s, %s, %s, %s, %s, %s)",
            default_enquiries
        )
        print("Enquiries seeded.")



    # Seed Followups
    cursor.execute("SELECT COUNT(*) FROM followups")
    if cursor.fetchone()[0] == 0:
        default_followups = [
            ('Kiran Patel', 'Toyota Innova', 'Today 4:00 PM', 'Phone Call', 'Discuss price drop', 'pending', 'Rahul S.'),
            ('Suresh Joshi', 'Tata Nexon', 'Today 6:00 PM', 'WhatsApp', 'Send updated photos', 'pending', 'Amit J.'),
            ('Meera Trivedi', 'Hyundai Creta', 'Tomorrow 10AM', 'Test Drive', 'Confirm time', 'scheduled', 'Priya P.'),
            ('Dilip Chauhan', 'Kia Seltos', 'Yesterday', 'Phone Call', 'Follow up on offer', 'overdue', 'Rahul S.'),
            ('Mohan Lal', 'Swift VXi', '13 Jun 2PM', 'Visit', 'Show car', 'scheduled', 'Amit J.')
        ]
        cursor.executemany(
            "INSERT INTO followups (customer, car, due, type, notes, status, assigned) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            default_followups
        )
        print("Followups seeded.")

    # Seed Revenue
    cursor.execute("SELECT COUNT(*) FROM revenue")
    if cursor.fetchone()[0] == 0:
        default_revenue = [
            ('12 Jun', 'Maruti Swift VXi 2021', 'Arjun Mehta', '₹5.20L', '₹4.10L', '₹1.10L', 'Bank Transfer'),
            ('10 Jun', 'Kia Seltos HTX', 'Rahul Gupta', '₹14.50L', '₹12.80L', '₹1.70L', 'Loan (HDFC)'),
            ('8 Jun', 'Honda Amaze S', 'Sunita Patel', '₹7.20L', '₹6.30L', '₹0.90L', 'Cash'),
            ('6 Jun', 'Tata Harrier XZ', 'Vikram Shah', '₹17.80L', '₹16.00L', '₹1.80L', 'Loan (SBI)'),
            ('4 Jun', 'Maruti Dzire ZXi', 'Pooja Mehta', '₹8.10L', '₹7.20L', '₹0.90L', 'Bank Transfer')
        ]
        cursor.executemany(
            "INSERT INTO revenue (date, car, buyer, sale, cost, profit, mode) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            default_revenue
        )
        print("Revenue seeded.")



    conn.commit()
    cursor.close()
    conn.close()
    print("Database initialized successfully!")

if __name__ == "__main__":
    init_database()
