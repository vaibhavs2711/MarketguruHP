import mysql.connector
from config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME

def alter_users_table():
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = conn.cursor()
        print("Creating individuals table...")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS individuals (
            id INT AUTO_INCREMENT PRIMARY KEY,
            full_name VARCHAR(100),
            mobile VARCHAR(20) UNIQUE
        )
        """)
        
        print("Creating dealers table...")
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
        conn.commit()
        print("Tables created successfully.")
        
        # Optional: migrate data from existing users table
        try:
            cursor.execute("SELECT * FROM users")
            users = cursor.fetchall()
            for u in users:
                # u format depending on cursor. Not using dictionary cursor.
                # let's just ignore migration for now or do it safely
                pass
        except Exception:
            pass
            
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    alter_users_table()
