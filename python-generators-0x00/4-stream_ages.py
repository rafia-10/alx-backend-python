import mysql.connector
import seed  # assuming your seed.py has connect_to_prodev()

def stream_user_ages():
    conn = seed.connect_to_prodev()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT age FROM user_data")
    for row in cursor:
        yield float(row['age'])  # yield one age at a time
    cursor.close()
    conn.close()

def calculate_average_age():
    total_age = 0
    count = 0
    # Loop 1: iterate over generator
    for age in stream_user_ages():
        total_age += age
        count += 1
    average = total_age / count if count else 0
    print(f"Average age of users: {average:.2f}")

if __name__ == "__main__":
    calculate_average_age()
