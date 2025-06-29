import sqlite3
import functools

def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Assume the SQL query is passed as a named arg "query"
        query = kwargs.get('query') if 'query' in kwargs else (args[0] if args else None)
        if query:
            print(f"[QUERY LOG] Executing SQL: {query}")
        else:
            print("[QUERY LOG] No query found to log.")
        return func(*args, **kwargs)
    return wrapper


@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


users = fetch_all_users(query="SELECT * FROM users")
