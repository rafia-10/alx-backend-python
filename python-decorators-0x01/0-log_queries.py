import sqlite3
import functools

# For demonstration purposes, let's create a dummy users.db and table
def setup_dummy_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT
        )
    ''')
    # Insert some dummy data if the table is empty
    cursor.execute("INSERT OR IGNORE INTO users (id, name, email) VALUES (1, 'Alice', 'alice@example.com')")
    cursor.execute("INSERT OR IGNORE INTO users (id, name, email) VALUES (2, 'Bob', 'bob@example.com')")
    conn.commit()
    conn.close()

setup_dummy_db()

#### decorator to log SQL queries

def log_queries(func):
    """
    A decorator that logs the SQL query string before the decorated function
    (expected to execute a database query) is called.

    Args:
        func (callable): The function to be decorated. This function is
                        expected to take the SQL query as its first positional
                        argument.

    Returns:
        callable: The wrapper function that includes the logging logic.
    """
    @functools.wraps(func) # Preserves the original function's metadata (e.g., __name__, __doc__)
    def wrapper(*args, **kwargs):
        # The query is expected to be the first positional argument.
        query = None
        if args:
            query = args[0] 
        elif 'query' in kwargs:
            query = kwargs['query']

        if query:
            print(f"Logging SQL Query: {query}")
        else:
            print("Warning: No query argument found for logging.")

        return func(*args, **kwargs)
    return wrapper

@log_queries
def fetch_all_users(query):
    """
    Fetches all users from the users.db database.
    This function will have its SQL query logged by the @log_queries decorator.
    """
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

#### fetch users while logging the query
print("\n--- Testing fetch_all_users ---")
users = fetch_all_users(query="SELECT * FROM users")
print(f"Fetched users: {users}")

print("\n--- Testing fetch_all_users with a WHERE clause ---")
specific_users = fetch_all_users("SELECT * FROM users WHERE name = 'Alice'")
print(f"Fetched specific users: {specific_users}")

# Example of a function that might not have 'query' as first arg (decorator needs adjustment for this)
@log_queries
def execute_update(sql_command, data=None):
    """
    Executes a SQL update command.
    """
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    if data:
        cursor.execute(sql_command, data)
    else:
        cursor.execute(sql_command)
    conn.commit()
    conn.close()
    print("Update executed.")

print("\n--- Testing execute_update ---")
execute_update("UPDATE users SET email = ? WHERE name = ?", ('alice.updated@example.com', 'Alice'))

print("\n--- Fetching users again after update ---")
users_after_update = fetch_all_users("SELECT * FROM users")
print(f"Users after update: {users_after_update}")

