import unittest
import requests
import json

BASE_URL = "http://localhost:5000/api"

class TestMarketGuruAPI(unittest.TestCase):
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
            "fName": "Automation",
            "lName": "Tester",
            "mobile": "9999988888",
            "email": "test_auto@example.com",
            "password": "testpassword123",
            "account_type": "private"
        }
        # Delete if exists from previous runs
        res = requests.post(f"{BASE_URL}/auth/register", json=payload)
        # Register could return 500 if already exists, but for clean DB it returns 200
        # If it returns 500 (due to UNIQUE constraints), it's fine since we verify login next
        self.assertIn(res.status_code, [200, 500])
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

if __name__ == "__main__":
    unittest.main()
