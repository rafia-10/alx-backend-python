import mysql.connector

def stream_users():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="your_password_here",  # replace with your MySQL password
        database="ALX_prodev"
    )
    cursor = conn.cursor(dictionary=True)  # dictionary=True returns rows as dicts (optional)

    cursor.execute("SELECT * FROM user_data")

    for row in cursor:
        yield row  # yields one row at a time

    cursor.close()
    conn.close()
