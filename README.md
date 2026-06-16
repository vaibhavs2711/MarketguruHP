# Market Guru HP - Used Cars Marketplace

Market Guru HP is Gujarat's premier pre-owned certified car marketplace. The application connects buyers directly with certified sellers and dealers across Gujarat (Vadodara, Ahmedabad, Surat, Rajkot, etc.) with complete transparency and zero middleman markup.

This project is built using an HTML/JS/CSS frontend and integrated with a **MySQL database** backend powered by a **Python Flask API**.

---

## Repository Structure

The project files are structured as follows:

*   **`MarketguruHP/`**: Main project folder containing:
    *   **Frontend HTML Pages**:
        *   `index.html` - Homepage with 3D Trust Carousel & Featured Vehicles.
        *   `buy-cars.html` - Search, filter and list used cars.
        *   `car-detail.html` - Vehicle specification details, EMI loan calculator, and contact details.
        *   `sell.html` - 4-step wizard to value and list a pre-owned car.
        *   `login.html` - Secure client sign-in, signup, and admin login console.
        *   `customer-dashboard.html` - Customer console for saved cars, active listings, and subscription billing.
        *   `emi-calculator.html` - Interactive loan eligibility calculator.
        *   `about.html` - Information about Market Guru HP.
    *   **Style sheets & visual assets**: `logo.png`, `phone-mockup.png`, `influencer.jpg`, `frames/`.
    *   **Database Connector (`cars-data.js`)**: Coordinates frontend components and synchronizes them with the backend REST APIs. Has built-in **automatic fallback to `localStorage`** if the Python server is offline.
    *   **Backend Server (`app.py`)**: REST API server running on Flask that handles authentication, listings, enquiries, leads, and staff data.
    *   **Database Initialization (`init_db.py`)**: Creates database tables and seeds them with complete mock data on first execution.
    *   **Database Config (`config.py`)**: Stores MySQL connection parameters.
    *   **Database SQL Dump (`marketguruhp.sql`)**: Raw SQL backup of the MySQL database structure and mock entries.

---

## Technical Stack

*   **Frontend**: HTML5, Vanilla JavaScript, CSS3
*   **Backend**: Python, Flask, Flask-CORS
*   **Database**: MySQL
*   **Authentication**: Secure SHA256 hashed password authentication

---

## Setup & Running the Application

### 1. Prerequisites
Ensure you have Python 3 and MySQL server running on your system. Install the required Python dependencies:
```bash
pip install flask flask-cors mysql-connector-python
```

### 2. Configure Database Credentials
Open `MarketguruHP/config.py` and adjust the MySQL connection parameters if they differ from your local setup:
```python
DB_HOST = "localhost"
DB_PORT = 3306
DB_USER = "root"
DB_PASSWORD = "root"  # Set to your MySQL password
DB_NAME = "marketguruhp"
```

### 3. Initialize the MySQL Database
Run the database initialization script to create the schema and automatically seed all default listings, staff, and leads:
```bash
cd MarketguruHP
python init_db.py
```
*(Note: If you want to import manually, you can also import `marketguruhp.sql` directly into your MySQL server).*

### 4. Start the Flask API Backend
Run the backend server:
```bash
python app.py
```
The server will start on [http://localhost:5000](http://localhost:5000).

### 5. Access the Platform
You can open the marketplace in one of two ways:
*   **Direct Server URL**: Navigate to [http://localhost:5000/index.html](http://localhost:5000/index.html) in your browser.
*   **Local File**: Double-click `MarketguruHP/index.html` on your filesystem.

---

## API Documentation

The Flask backend exposes the following REST API endpoints:

*   `GET /api/ping` - Server health check
*   `GET /api/init` - Loads initial state for all database tables (cars, leads, followups, staff, wishlist, etc.)
*   `POST /api/auth/login` - Authenticates customer login
*   `POST /api/auth/register` - Creates a new customer account
*   `POST /api/auth/admin-login` - Authenticates admin panel login
*   `POST /api/cars` - Publishes a new used car listing
*   `POST /api/cars/verify` - Verifies/unverifies a vehicle listing (Admin only)
*   `POST /api/cars/sold` - Marks a vehicle listing as sold
*   `POST /api/enquiries` - Submits a customer inquiry
*   `POST /api/enquiries/resolve` - Resolves an open inquiry (Admin only)
*   `POST /api/leads` - Saves a new CRM lead (Admin only)
*   `POST /api/staff` - Creates a new staff manager (Admin only)
*   `POST /api/subscription/activate` - Activates dealer partner subscription
*   `POST /api/subscription/cancel` - Cancels dealer partner subscription
*   `POST /api/wishlist/toggle` - Saves or removes a vehicle from customer wishlist
