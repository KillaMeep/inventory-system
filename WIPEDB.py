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

# Function to drop all tables in the database
def drop_all_tables():
    connection = connect_to_database()
    cursor = connection.cursor()

    try:
        # Get the list of table names in the database
        
        cursor.execute("SHOW TABLES")
        tables = [table[0] for table in cursor.fetchall()]
        print(status.OK,"SHOW TABLES")
        print(tables)
        # Drop all tables
        for table_name in tables:
            print(status.INFO,f"DROP TABLE {table_name}",end='\r')
            cursor.execute(f"DROP TABLE {table_name}")
            print(status.OK,f"DROP TABLE {table_name}")
        # Commit the changes to the database
        connection.commit()
        print(status.OK,"All tables dropped from the database.")

    except mysql.connector.Error as e:
        print(status.ERROR,e)
    finally:
        connection.close()

if __name__ == "__main__":
    try:
     drop_all_tables()
    except Exception as e:
        print(status.ERROR,e)
