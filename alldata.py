import mysql.connector
from utils.status import status
import os
from dotenv import load_dotenv


# Function to connect to the MariaDB database
def connect_to_database():
    load_dotenv()
    host = os.getenv("DB_HOST")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    database = os.getenv("DB_DATABASE")
    return mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
# Function to retrieve and display data from all tables in the database
def display_data_from_all_tables():
    connection = connect_to_database()
    cursor = connection.cursor()

    try:
        # Get the list of table names in the database
        cursor.execute("SHOW TABLES")
        print(status.OK, "SHOW TABLES")
        tables = [table[0] for table in cursor.fetchall()]
        print(tables)
        # Display data from all tables
        for table_name in tables:
            # Modify the SELECT query to exclude the id column
            print(status.INFO, f"SELECT * FROM {table_name} WHERE id != ''", end='\r')
            cursor.execute(f"SELECT * FROM {table_name} WHERE id != ''")
            data = cursor.fetchall()
            print(status.OK, f"SELECT * FROM {table_name} WHERE id != ''")
            # Display the data
            if data:
                print(status.INFO, f"Data from the {table_name} table:")
                for row in data:
                    # Exclude the id column from the row
                    row_without_id = row[1:]  # Exclude the first element (id)
                    print(status.INFO, row_without_id)
            else:
                print(status.INFO, f"No data found in the {table_name} table.")

    except mysql.connector.Error as e:
        print(status.ERROR, e)
    finally:
        connection.close()

if __name__ == "__main__":
    try:
        display_data_from_all_tables()
    except Exception as e:
        print(status.ERROR,e)
