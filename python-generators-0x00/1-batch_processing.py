import mysql.connector

def stream_users_in_batches(batch_size):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="your_password_here",  # update this
        database="ALX_prodev"
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")

    while True:
        batch = cursor.fetchmany(batch_size)
        if not batch:
            break
        yield batch

    cursor.close()
    conn.close()


def batch_processing(batch_size):
    # Loop 1: over batches
    for batch in stream_users_in_batches(batch_size):
        # Loop 2: filter users in batch
        filtered = (user for user in batch if float(user['age']) > 25)
        # Loop 3: yield each filtered user one by one
        for user in filtered:
            print(user)
