import time
import sqlite3
import functools

query_cache = {}

# --- with_db_connection decorator ---
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            result = func(conn, *args, **kwargs)
            return result
        finally:
            conn.close()
            print("✅ Connection closed automatically")
    return wrapper

# --- cache_query decorator ---
def cache_query(func):
    @functools.wraps(func)
    def wrapper(conn, query, *args, **kwargs):
        if query in query_cache:
            print("⚡ Returning cached result for:", query)
            return query_cache[query]
        print("💾 Caching result for:", query)
        result = func(conn, query, *args, **kwargs)
        query_cache[query] = result
        return result
    return wrapper

# --- Function using decorators ---
@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# --- First call: queries DB and caches ---
users = fetch_users_with_cache(query="SELECT * FROM users")
print(users)

# --- Second call: uses cached result ---
users_again = fetch_users_with_cache(query="SELECT * FROM users")
print(users_again)
