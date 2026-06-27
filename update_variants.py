import pandas as pd
from app import query_db, get_db_connection

def update_db():
    print("Connecting to DB...")
    try:
        query_db("ALTER TABLE car_models ADD COLUMN variants TEXT", commit=True)
        print("Added 'variants' column.")
    except Exception as e:
        print("Column may already exist", e)

    df = pd.read_csv("models_with_variants (1).csv")
    conn = get_db_connection()
    cursor = conn.cursor()
    count = 0
    for index, row in df.iterrows():
        variants = str(row['variants']) if pd.notnull(row['variants']) else ''
        model_id = row['id']
        cursor.execute("UPDATE car_models SET variants = %s WHERE id = %s", (variants, model_id))
        count += 1
    conn.commit()
    cursor.close()
    conn.close()
    print(f"Database updated for {count} models!")

if __name__ == "__main__":
    update_db()
