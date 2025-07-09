import sqlite3

# create db n fill it
conn = sqlite3.connect("example.db")
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS users")
# Create 'users' table with age column
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        age INTEGER
    )
""")

# Insert some sample users with ages
users_data = [
    ('Alice', 'alice@example.com', 40),
    ('Bob', 'bob@example.com', 22),
    ('Charlie', 'charlie@example.com', 27),
    ('Diana', 'diana@example.com', 44),
    ('Eve', 'eve@example.com', 35)
]
cursor.execute("DELETE FROM users")
cursor.executemany("INSERT INTO users (name, email, age) VALUES (?, ?, ?)", users_data)

conn.commit()
conn.close()

print("✅ Database setup done! 'users' table created and sample data inserted.")


class ExecuteQuery:
    def __init__(self, query, params=()):
        self.query = query
        self.params = params
        self.conn = None
        self.results = None

    def __enter__(self):
        self.conn = sqlite3.connect("example.db")
        cursor = self.conn.cursor()
        cursor.execute(self.query, self.params)
        self.results = cursor.fetchall()
        return self.results  # Return results to the with-block

    def __exit__(self, exc_type, exc_value, traceback):
        if self.conn:
            self.conn.close()



# Usage example
query = "SELECT * FROM users WHERE age > ?"
params = (25,)

with ExecuteQuery(query, params) as results:
    print("Users older than 25:")
    for row in results:
        print(row)
