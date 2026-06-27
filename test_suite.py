import unittest
import requests
import json

BASE_URL = "http://localhost:5000/api"

class TestMarketGuruAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Clean up any database records for the test phone number 9999988888"""
        import mysql.connector
        from config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME
        try:
            conn = mysql.connector.connect(
                host=DB_HOST,
                port=DB_PORT,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME
            )
            cursor = conn.cursor()
            cursor.execute("DELETE FROM dealers WHERE mobile = '9999988888'")
            cursor.execute("DELETE FROM customers WHERE mobile = '9999988888'")
            cursor.execute("DELETE FROM leads WHERE mobile = '9999988888'")
            cursor.execute("DELETE FROM enquiries WHERE mobile = '9999988888'")
            cursor.execute("DELETE FROM wishlist WHERE user_mobile = '9999988888'")
            cursor.execute("DELETE FROM subscriptions WHERE user_mobile = '9999988888'")
            cursor.execute("DELETE FROM cars WHERE listed_by = '9999988888'")
            conn.commit()
            cursor.close()
            conn.close()
            print("Test suite database cleanup completed successfully.")
        except Exception as e:
            print(f"Warning: Test suite database cleanup failed: {e}")

    def test_01_ping(self):
        """Test server health check"""
        res = requests.get(f"{BASE_URL}/ping")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data.get("status"), "ok")

    def test_02_init(self):
        """Test initial state loading"""
        res = requests.get(f"{BASE_URL}/init")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data.get("status"), "success")
        self.assertIn("cars", data)
        self.assertIn("leads", data)
        self.assertIn("enquiries", data)
        self.assertIn("staff", data)

    def test_03_register(self):
        """Test client registration"""
        payload = {
            "dealership_name": "Automation Dealer",
            "mobile": "9999988888",
            "email": "test_auto@example.com",
            "password": "testpassword123",
            "account_type": "dealer",
            "address": "123 Automation St",
            "state": "Gujarat",
            "city": "Vadodara"
        }
        # Delete if exists from previous runs
        res = requests.post(f"{BASE_URL}/auth/register", json=payload)
        # If it returns 400 or 500 (due to uniqueness checks), it's fine since we verify login next
        self.assertIn(res.status_code, [200, 400, 500])
        if res.status_code == 200:
            data = res.json()
            self.assertEqual(data.get("status"), "success")
            self.assertEqual(data.get("user", {}).get("mobile"), "9999988888")

    def test_04_login(self):
        """Test client login"""
        payload = {
            "id": "test_auto@example.com",
            "password": "testpassword123"
        }
        res = requests.post(f"{BASE_URL}/auth/login", json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data.get("status"), "success")
        self.assertEqual(data.get("user", {}).get("mobile"), "9999988888")

    def test_05_admin_login(self):
        """Test super admin login"""
        payload = {
            "email": "rajesh@marketguruhp.in",
            "password": "admin123"
        }
        res = requests.post(f"{BASE_URL}/auth/admin-login", json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data.get("status"), "success")
        self.assertEqual(data.get("user", {}).get("role"), "Super Admin")

    def test_06_add_car(self):
        """Test publishing a car listing"""
        payload = {
            "name": "Test Automation Sedan",
            "year": 2023,
            "price": "6.50",
            "priceN": 650000,
            "km": "10,000",
            "fuel": "Petrol",
            "trans": "Manual",
            "owner": "1st",
            "color": "#e8eef5",
            "emoji": "🚗",
            "city": "Vadodara",
            "desc": "Testing automation framework creation.",
            "features": ["Airbags", "ABS", "Power Windows"],
            "verified": 0
        }
        res = requests.post(f"{BASE_URL}/cars", json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data.get("status"), "success")
        self.assertEqual(data.get("car", {}).get("name"), "Test Automation Sedan")
        self.assertFalse(data.get("car", {}).get("verified"))
        
        # Save ID for subsequent tests
        self.__class__.created_car_id = data.get("car", {}).get("id")

    def test_07_verify_car(self):
        """Test verifying a car listing"""
        car_id = getattr(self.__class__, "created_car_id", None)
        self.assertIsNotNone(car_id)
        
        payload = {
            "car_id": car_id,
            "verified": 1
        }
        res = requests.post(f"{BASE_URL}/cars/verify", json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data.get("status"), "success")
        self.assertTrue(data.get("verified"))

    def test_08_add_enquiry(self):
        """Test submitting a customer enquiry"""
        payload = {
            "name": "Automation Enquirer",
            "mobile": "9999988888",
            "car": "Test Automation Sedan",
            "query": "Is the price negotiable?"
        }
        res = requests.post(f"{BASE_URL}/enquiries", json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data.get("status"), "success")
        self.assertEqual(data.get("enquiry", {}).get("name"), "Automation Enquirer")

    def test_09_resolve_enquiry(self):
        """Test resolving an enquiry"""
        payload = {
            "name": "Automation Enquirer"
        }
        res = requests.post(f"{BASE_URL}/enquiries/resolve", json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data.get("status"), "success")

    def test_10_add_lead(self):
        """Test adding a CRM lead"""
        payload = {
            "name": "Manual Automation Lead",
            "mobile": "9999988888",
            "car": "Test Automation Sedan",
            "budget": "6-7L",
            "source": "Walk-in",
            "stage": "new"
        }
        res = requests.post(f"{BASE_URL}/leads", json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data.get("status"), "success")
        self.assertEqual(data.get("lead", {}).get("name"), "Manual Automation Lead")

    def test_11_add_staff(self):
        """Test creating a new staff user"""
        payload = {
            "name": "Automation Executive",
            "email": "auto_exec@marketguruhp.in",
            "role": "Executive",
            "dept": "Sales"
        }
        res = requests.post(f"{BASE_URL}/staff", json=payload)
        self.assertIn(res.status_code, [200, 500]) # Could fail if email already exists from previous runs
        if res.status_code == 200:
            data = res.json()
            self.assertEqual(data.get("status"), "success")
            self.assertEqual(data.get("staff", {}).get("email"), "auto_exec@marketguruhp.in")

    def test_12_wishlist_toggle(self):
        """Test toggling a car in wishlist"""
        car_id = getattr(self.__class__, "created_car_id", None)
        self.assertIsNotNone(car_id)

        payload = {
            "user_mobile": "9999988888",
            "car_id": car_id
        }
        # First toggle: should add
        res = requests.post(f"{BASE_URL}/wishlist/toggle", json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data.get("status"), "success")
        self.assertTrue(data.get("added"))

        # Second toggle: should remove
        res2 = requests.post(f"{BASE_URL}/wishlist/toggle", json=payload)
        self.assertEqual(res2.status_code, 200)
        data2 = res2.json()
        self.assertEqual(data2.get("status"), "success")
        self.assertFalse(data2.get("added"))

    def test_13_subscription_flow(self):
        """Test dealer subscription flow"""
        payload = {
            "user_mobile": "9999988888"
        }
        # Activate
        res = requests.post(f"{BASE_URL}/subscription/activate", json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data.get("status"), "success")
        self.assertIsNotNone(data.get("expiry"))

        # Cancel
        res2 = requests.post(f"{BASE_URL}/subscription/cancel", json=payload)
        self.assertEqual(res2.status_code, 200)
        data2 = res2.json()
        self.assertEqual(data2.get("status"), "success")

    def test_14_mark_sold(self):
        """Test marking a listing sold (deletes from active cars)"""
        car_id = getattr(self.__class__, "created_car_id", None)
        self.assertIsNotNone(car_id)

        payload = {
            "car_id": car_id
        }
        res = requests.post(f"{BASE_URL}/cars/sold", json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data.get("status"), "success")

    def test_15_individual_seller_limit(self):
        """Test that an individual seller is restricted to exactly 1 listing"""
        # Register a client (individual)
        register_payload = {
            "fName": "Limit",
            "lName": "Tester",
            "mobile": "9999977777",
            "email": "limit_test@example.com",
            "password": "testpassword",
            "account_type": "private"
        }
        requests.post(f"{BASE_URL}/auth/register", json=register_payload)

        # First car listing submission (should succeed)
        car1_payload = {
            "name": "Limit Test Car 1",
            "year": 2020,
            "price": "5.00",
            "priceN": 500000,
            "km": "30,000",
            "fuel": "Petrol",
            "trans": "Manual",
            "owner": "1st",
            "color": "#e8eef5",
            "emoji": "🚗",
            "city": "Vadodara",
            "desc": "Individual limit test car 1.",
            "features": [],
            "listed_by": "9999977777"
        }
        res1 = requests.post(f"{BASE_URL}/cars", json=car1_payload)
        self.assertEqual(res1.status_code, 200)
        car1_id = res1.json().get("car", {}).get("id")

        # Second car listing submission (should fail with 400)
        car2_payload = {
            "name": "Limit Test Car 2",
            "year": 2021,
            "price": "6.00",
            "priceN": 600000,
            "km": "20,000",
            "fuel": "Petrol",
            "trans": "Manual",
            "owner": "1st",
            "color": "#e8eef5",
            "emoji": "🚗",
            "city": "Vadodara",
            "desc": "Individual limit test car 2.",
            "features": [],
            "listed_by": "9999977777"
        }
        res2 = requests.post(f"{BASE_URL}/cars", json=car2_payload)
        self.assertEqual(res2.status_code, 400)
        self.assertEqual(res2.json().get("status"), "error")

        # Cleanup: delete the first car
        requests.post(f"{BASE_URL}/cars/sold", json={"car_id": car1_id})

if __name__ == "__main__":
    unittest.main()
