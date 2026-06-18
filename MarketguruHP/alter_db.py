import mysql.connector
from config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME

def alter_cars_table():
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = conn.cursor()
        print("Checking if column exist...")
        cursor.execute("SHOW COLUMNS FROM cars LIKE 'image'")
        if not cursor.fetchone():
            print("Adding image column...")
            cursor.execute("ALTER TABLE cars ADD COLUMN image LONGTEXT")
            conn.commit()
            print("Image column added successfully.")
        else:
            print("Image column already exists.")
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    alter_cars_table()
