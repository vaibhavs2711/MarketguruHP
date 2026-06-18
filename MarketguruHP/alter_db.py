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
        print("Checking if columns exist...")
        cursor.execute("SHOW COLUMNS FROM users LIKE 'dealership_name'")
        if not cursor.fetchone():
            print("Adding dealer columns...")
            cursor.execute("ALTER TABLE users ADD COLUMN dealership_name VARCHAR(100), ADD COLUMN address VARCHAR(255), ADD COLUMN city VARCHAR(50), ADD COLUMN state VARCHAR(50)")
            conn.commit()
            print("Columns added successfully.")
        else:
            print("Columns already exist.")
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    alter_users_table()
