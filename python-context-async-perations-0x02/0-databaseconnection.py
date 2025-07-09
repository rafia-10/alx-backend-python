# create and populate database
import sqlite3

# Connect to (or create) a local file-based DB
conn = sqlite3.connect("example.db")
cursor = conn.cursor()

# Create 'users' table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT
    )
""")

# Insert sample data (if you want, skip this if already inserted)
cursor.execute("INSERT INTO users (name, email) VALUES ('Alice', 'alice@example.com')")
cursor.execute("INSERT INTO users (name, email) VALUES ('Bob', 'bob@example.com')")
cursor.execute("INSERT INTO users (name, email) VALUES ('Charlie', 'charlie@example.com')")

# Save & close
conn.commit()
conn.close()

print("✅ Database created and sample data inserted!")


## class-based context manager

class DatabaseConnection:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None

    def __enter__(self):
        print("🔌 Opening DB connection...")
        self.conn = sqlite3.connect(self.db_name)
        return self.conn

    def __exit__(self, exc_type, exc_value, traceback):
        if self.conn:
            self.conn.close()
            print("✅ Closing DB connection...")

# Using the context manager
with DatabaseConnection("example.db") as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    
    print("👀 Query Results:")
    for row in results:
        print(row)
