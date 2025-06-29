import sqlite3
import functools

# --- Copying the with_db_connection decorator from before ---
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

# --- New transactional decorator as per instruction ---
def transactional(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()
            print("✅ Transaction committed")
            return result
        except Exception as e:
            conn.rollback()
            print("❌ Transaction rolled back due to error:", e)
            raise
    return wrapper

# --- Your function using both decorators ---
@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))

# --- Running it ---
update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
