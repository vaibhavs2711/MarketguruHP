import mysql.connector
from config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME
from datetime import datetime
import re

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

def seed_database():
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = conn.cursor()

        # CREATE TABLES
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS car_makes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL UNIQUE,
            slug VARCHAR(100) NOT NULL UNIQUE,
            logo_url VARCHAR(255) DEFAULT NULL,
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            INDEX idx_slug (slug)
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS car_models (
            id INT AUTO_INCREMENT PRIMARY KEY,
            make_id INT NOT NULL,
            name VARCHAR(100) NOT NULL,
            slug VARCHAR(150) NOT NULL UNIQUE,
            body_type VARCHAR(50) DEFAULT NULL,
            launched_year INT DEFAULT NULL,
            discontinued_year INT DEFAULT NULL,
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (make_id) REFERENCES car_makes(id) ON DELETE CASCADE,
            UNIQUE KEY unique_make_model (make_id, name),
            INDEX idx_make (make_id),
            INDEX idx_slug (slug)
        )
        """)

        # Future Expansion Tables
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS fuel_types (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(50) NOT NULL UNIQUE,
            slug VARCHAR(50) NOT NULL UNIQUE
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS transmissions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(50) NOT NULL UNIQUE,
            slug VARCHAR(50) NOT NULL UNIQUE
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS body_types (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(50) NOT NULL UNIQUE,
            slug VARCHAR(50) NOT NULL UNIQUE
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS drivetrain_types (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(50) NOT NULL UNIQUE,
            slug VARCHAR(50) NOT NULL UNIQUE
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS car_variants (
            id INT AUTO_INCREMENT PRIMARY KEY,
            model_id INT NOT NULL,
            name VARCHAR(150) NOT NULL,
            slug VARCHAR(200) NOT NULL UNIQUE,
            engine_cc INT,
            fuel_type_id INT,
            transmission_id INT,
            drivetrain_id INT,
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (model_id) REFERENCES car_models(id) ON DELETE CASCADE,
            FOREIGN KEY (fuel_type_id) REFERENCES fuel_types(id) ON DELETE SET NULL,
            FOREIGN KEY (transmission_id) REFERENCES transmissions(id) ON DELETE SET NULL,
            FOREIGN KEY (drivetrain_id) REFERENCES drivetrain_types(id) ON DELETE SET NULL
        )
        """)

        conn.commit()
        
        # Populate Makes
        makes = [
            "Maruti Suzuki", "Hyundai", "Tata", "Mahindra", "Honda", "Toyota", "Kia", "MG", 
            "Skoda", "Volkswagen", "Ford", "Renault", "Nissan", "Jeep", "BMW", "Mercedes-Benz", 
            "Audi", "Volvo", "Jaguar", "Land Rover", "Porsche", "Lexus", "Mini", "Fiat", 
            "Chevrolet", "Datsun", "Mitsubishi", "Citroen", "BYD", "Aston Martin", "Ferrari",
            "Lamborghini", "Maserati", "Rolls-Royce", "Bentley", "McLaren", "Isuzu", "Force Motors", "Hindustan Motors"
        ]

        # Insert Makes
        for make in makes:
            slug = slugify(make)
            cursor.execute("INSERT IGNORE INTO car_makes (name, slug, is_active) VALUES (%s, %s, %s)", (make, slug, True))
        conn.commit()

        # Dictionary of models
        models_data = {
            "Maruti Suzuki": ["800", "Alto", "Alto 800", "Alto K10", "A Star", "Baleno", "Brezza", "Celerio", "Celerio X", "Ciaz", "Dzire", "Eeco", "Ertiga", "Esteem", "Fronx", "Grand Vitara", "Ignis", "Invicto", "Jimny", "Kizashi", "Omni", "Ritz", "S-Cross", "S-Presso", "Swift", "Swift Dzire", "SX4", "Vitara Brezza", "Wagon R", "Wagon R 1.0", "Wagon R Duo", "Wagon R Stingray", "XL6", "Zen", "Zen Estilo", "Gypsy", "Versa", "Grand Vitara XL7", "Baleno RS"],
            "Hyundai": ["Accent", "Alcazar", "Aura", "Creta", "Creta N Line", "Creta Electric", "Elite i20", "Elantra", "Eon", "Exter", "Getz", "Getz Prime", "Grand i10", "Grand i10 Nios", "Grand i10 Prime", "i10", "i20", "i20 Active", "i20 N Line", "Ioniq 5", "Kona Electric", "New Elantra", "New i20", "New Santro", "Santa Fe", "Santro", "Santro Xing", "Sonata", "Sonata Embera", "Sonata Transform", "Terracan", "Tucson", "Venue", "Venue N Line", "Verna", "Verna Transform", "Xcent", "Xcent Prime"],
            "Tata": ["Altroz", "Aria", "Bolt", "Curvv", "Curvv EV", "Harrier", "Harrier EV", "Hexa", "Indica", "Indica Vista", "Indica V2", "Indigo", "Indigo CS", "Indigo ECS", "Indigo Marina", "Manza", "Nano", "Nexon", "Nexon EV", "Punch", "Punch EV", "Safari", "Safari Storme", "Safari Dicor", "Sumo", "Sumo Gold", "Sumo Grande", "Tiago", "Tiago JTP", "Tiago NRG", "Tiago EV", "Tigor", "Tigor EV", "Zest", "Sierra", "Estate"],
            "Mahindra": ["Alturas G4", "Armada", "Bolero", "Bolero Neo", "Bolero Neo Plus", "Bolero Power Plus", "E2O", "E2O Plus", "E Verito", "KUV100", "KUV100 NXT", "Marazzo", "Marshal", "Maxx", "NuvoSport", "Quanto", "Scorpio", "Scorpio-N", "Scorpio Classic", "Thar", "Thar Roxx", "TUV300", "TUV300 Plus", "Verito", "Verito Vibe", "XUV300", "XUV3XO", "XUV400", "XUV500", "XUV700", "Xylo"],
            "Honda": ["Accord", "Amaze", "BR-V", "Brio", "City", "Civic", "CR-V", "Elevate", "Jazz", "Mobilio", "WR-V"],
            "Toyota": ["Camry", "Corolla", "Corolla Altis", "Etios", "Etios Cross", "Etios Liva", "Fortuner", "Fortuner Legender", "Glanza", "Hilux", "Innova", "Innova Crysta", "Innova Hycross", "Land Cruiser", "Land Cruiser Prado", "Prius", "Qualis", "Rumion", "Urban Cruiser", "Urban Cruiser Hyryder", "Vellfire", "Yaris"],
            "Kia": ["Carens", "Carnival", "EV6", "EV9", "Seltos", "Sonet"],
            "MG": ["Astor", "Cloud EV", "Comet EV", "Gloster", "Hector", "Hector Plus", "Windsor EV", "ZS EV"],
            "Skoda": ["Enyaq", "Fabia", "Kodiaq", "Kushaq", "Laura", "Octavia", "Octavia Combi", "Rapid", "Slavia", "Superb", "Yeti"],
            "Volkswagen": ["Ameo", "Beetle", "Cross Polo", "Jetta", "Passat", "Phaeton", "Polo", "Taigun", "Tiguan", "Tiguan Allspace", "Touareg", "Vento", "Virtus"],
            "Ford": ["Classic", "EcoSport", "Endeavour", "Escort", "Fiesta", "Fiesta Classic", "Figo", "Figo Aspire", "Freestyle", "Fusion", "Ikon", "Mustang"],
            "Renault": ["Captur", "Duster", "Fluence", "Kiger", "Kwid", "Lodgy", "Pulse", "Scala", "Triber"],
            "Nissan": ["370Z", "Evalia", "GT-R", "Kicks", "Magnite", "Micra", "Micra Active", "Sunny", "Teana", "Terrano", "X-Trail"],
            "Jeep": ["Cherokee", "Compass", "Grand Cherokee", "Meridian", "Wrangler"],
            "BMW": ["1 Series", "2 Series", "3 Series", "3 Series Gran Limousine", "3 Series GT", "4 Series", "5 Series", "5 Series GT", "6 Series", "6 Series GT", "7 Series", "8 Series", "i3", "i4", "i7", "iX", "iX1", "M2", "M3", "M4", "M5", "M6", "M8", "X1", "X2", "X3", "X3 M", "X4", "X4 M", "X5", "X5 M", "X6", "X6 M", "X7", "Z3", "Z4"],
            "Mercedes-Benz": ["A-Class", "B-Class", "C-Class", "CLA", "CLE", "CLK", "CLS", "E-Class", "EQA", "EQB", "EQC", "EQE", "EQS", "G-Class", "GLA", "GLB", "GLC", "GLE", "GLK", "GLS", "M-Class", "Maybach S-Class", "Maybach GLS", "R-Class", "S-Class", "SL", "SLC", "SLK", "V-Class", "AMG GT", "SLS AMG"],
            "Audi": ["A3", "A4", "A5", "A6", "A7", "A8", "A8 L", "e-tron", "e-tron GT", "Q2", "Q3", "Q5", "Q7", "Q8", "Q8 e-tron", "R8", "RS5", "RS7", "S5", "TT"],
            "Volvo": ["C40 Recharge", "S60", "S60 Cross Country", "S80", "S90", "V40", "V40 Cross Country", "V90 Cross Country", "XC40", "XC40 Recharge", "XC60", "XC90"],
            "Jaguar": ["F-Pace", "F-Type", "I-Pace", "XE", "XF", "XJ", "XK"],
            "Land Rover": ["Defender", "Discovery", "Discovery Sport", "Freelander", "Range Rover", "Range Rover Evoque", "Range Rover Sport", "Range Rover Velar"],
            "Porsche": ["718", "911", "Boxster", "Cayenne", "Cayenne Coupe", "Cayman", "Macan", "Panamera", "Taycan"],
            "Lexus": ["ES", "GS", "LC", "LM", "LS", "LX", "NX", "RX"],
            "Mini": ["Clubman", "Cooper", "Countryman", "Convertible"],
            "Fiat": ["500", "Abarth Punto", "Avventura", "Linea", "Linea Classic", "Palio", "Palio Stile", "Punto", "Punto Evo", "Punto Pure", "Uno"],
            "Chevrolet": ["Aveo", "Aveo U-VA", "Beat", "Captiva", "Cruze", "Enjoy", "Optra", "Optra Magnum", "Sail", "Sail U-VA", "Spark", "Tavera", "Trailblazer"],
            "Datsun": ["GO", "GO+", "redi-GO"],
            "Mitsubishi": ["Cedia", "Lancer", "Montero", "Outlander", "Pajero", "Pajero Sport"],
            "Citroen": ["Basalt", "C3", "C3 Aircross", "C5 Aircross", "eC3"],
            "BYD": ["Atto 3", "e6", "Seal"],
            "Aston Martin": ["DB11", "DB12", "DBX", "Rapide", "Vantage", "Vanquish"],
            "Ferrari": ["296 GTB", "488", "812", "California", "F8 Tributo", "Portofino", "Purosangue", "Roma", "SF90 Stradale"],
            "Lamborghini": ["Aventador", "Huracan", "Revuelto", "Urus"],
            "Maserati": ["Ghibli", "GranTurismo", "Levante", "MC20", "Quattroporte", "Grecale"],
            "Rolls-Royce": ["Cullinan", "Dawn", "Ghost", "Phantom", "Wraith"],
            "Bentley": ["Bentayga", "Continental GT", "Flying Spur", "Mulsanne"],
            "McLaren": ["720S", "750S", "Artura", "GT"],
            "Isuzu": ["D-Max", "MU-7", "MU-X", "V-Cross"],
            "Force Motors": ["Gurkha", "Trax Cruiser", "Trax Toofan", "One"],
            "Hindustan Motors": ["Ambassador", "Contessa"]
        }

        # Fetch makes map
        cursor.execute("SELECT name, id FROM car_makes")
        make_map = {row[0]: row[1] for row in cursor.fetchall()}

        for make, models in models_data.items():
            if make in make_map:
                make_id = make_map[make]
                for model in models:
                    model_slug = slugify(f"{make}-{model}")
                    cursor.execute(
                        "INSERT IGNORE INTO car_models (make_id, name, slug, is_active) VALUES (%s, %s, %s, %s)",
                        (make_id, model, model_slug, True)
                    )
        conn.commit()

        print("Database seeded with automotive schema!")
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    seed_database()
