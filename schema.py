import pymysql

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',  # Replace with your MySQL username
    'password': 'root',  # Replace with your MySQL password
    'port': 8000
}

def create_database():
    try:
        # Establish connection to MySQL server
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()

        # Create database if not exists
        cursor.execute("CREATE DATABASE IF NOT EXISTS demo")
        conn.commit()  # Commit changes

        print("Database created successfully!")

    except pymysql.Error as e:
        print(f"Error creating database: {e}")

    finally:
        if conn:
            conn.close()

def create_schema():
    try:
        # Connect to the database
        conn = pymysql.connect(database='demo', **db_config)
        cursor = conn.cursor()

        # Create table if not exists
        cursor.execute("CREATE TABLE IF NOT EXISTS calculations (id INT AUTO_INCREMENT PRIMARY KEY, num1 INT, num2 INT, operation VARCHAR(10), result INT)")
        conn.commit()  # Commit changes

        print("Schema created successfully!")

    except pymysql.Error as e:
        print(f"Error creating schema: {e}")

    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    create_database()
    create_schema()
