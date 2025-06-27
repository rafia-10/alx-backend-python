# ALX ProDev Airbnb Clone Backend - Seed Script

This Python script sets up the MySQL database and populates the `user_data` table with sample user information for the Airbnb clone backend project.

---

## Features

- Creates MySQL database `ALX_prodev` if it doesn’t exist  
- Creates `user_data` table with fields:
  - `user_id` (UUID, Primary Key)  
  - `name` (VARCHAR)  
  - `email` (VARCHAR)  
  - `age` (DECIMAL)  
- Reads user data from a CSV file (`user_data.csv`) containing `name`, `email`, and `age`  
- Automatically generates UUIDs for each user  
- Prevents duplicate users by checking existing emails before insertion  
- Skips malformed or incomplete CSV rows  
- Prints progress logs for easy tracking

---

## Setup & Usage

### Prerequisites

- Python 3.6+  
- MySQL server installed and running  
- `mysql-connector-python` package installed  
  ```bash
  pip install mysql-connector-python
