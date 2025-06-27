import mysql.connector
import csv
import uuid
import os

DB_NAME = "ALX_prodev"
TABLE_NAME = "user_data"

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345678910"  # <- Change this to your MySQL password
    )

def create_database(connection):
    cursor = connection.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    cursor.close()
    print(f"✅ Database '{DB_NAME}' ensured.")

def connect_to_prodev():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345678910",  # <- Change this too
        database=DB_NAME
    )

def create_table(connection):
    cursor = connection.cursor()
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            user_id CHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL(5, 2) NOT NULL,
            INDEX (user_id)
        )
    """)
    cursor.close()
    print(f"✅ Table '{TABLE_NAME}' ensured.")

def insert_data(connection, data):
    cursor = connection.cursor()
    insert_query = f"""
        INSERT INTO {TABLE_NAME} (user_id, name, email, age)
        VALUES (%s, %s, %s, %s)
    """
    inserted = 0
    for row in data:
        if len(row) != 3:
            print("❌ Skipping invalid row:", row)
            continue

        name, email, age = row
        user_id = str(uuid.uuid4())

        # Check if user already exists by email
        check_query = f"SELECT COUNT(*) FROM {TABLE_NAME} WHERE email = %s"
        cursor.execute(check_query, (email,))
        (count,) = cursor.fetchone()

        if count == 0:
            cursor.execute(insert_query, (user_id, name, email, age))
            inserted += 1

    connection.commit()
    cursor.close()
    print(f"🎉 Inserted {inserted} new records into '{TABLE_NAME}'.")

def load_csv(filename):
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        return [row for row in reader if len(row) == 3]

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, "user_data.csv")

    if not os.path.exists(csv_path):
        print("❌ CSV file not found at:", csv_path)
        return

    data = load_csv(csv_path)

    conn = connect_db()
    create_database(conn)
    conn.close()

    conn = connect_to_prodev()
    create_table(conn)
    insert_data(conn, data)
    conn.close()

if __name__ == "__main__":
    main()
