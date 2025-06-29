import time
import sqlite3
import functools

# --- with_db_connection ---
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

# --- retry_on_failure ---
def retry_on_failure(retries=3, delay=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, retries + 1):
                try:
                    print(f"⚡ Attempt {attempt}")
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"❌ Attempt {attempt} failed: {e}")
                    last_exception = e
                    if attempt < retries:
                        print(f"⏳ Retrying in {delay} seconds...")
                        time.sleep(delay)
            print("💥 All retries failed.")
            raise last_exception
        return wrapper
    return decorator

# --- Function using both decorators ---
@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

# --- Try it ---
users = fetch_users_with_retry()
print(users)
