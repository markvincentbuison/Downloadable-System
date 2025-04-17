import mysql.connector
from mysql.connector import Error
from app.mysql_config import Config  # Import Config class to get MySQL details

def create_connection():
    try:
        # Use the Config class to get connection details
        connection = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DB
        )

        if connection.is_connected():
            print("Successfully connected to MySQL Render database")
            return connection
        else:
            print("Failed to connect to the database Render")
            return None

    except Error as e:
        print(f"Error: {e}")
        return None

#-----------------------------------------
import mysql.connector
from mysql.connector import Error
from app.mysql_config import Config

import psycopg2
from psycopg2 import OperationalError

# ✅ MySQL Connection
def create_mysql_connection():
    try:
        connection = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DB
        )
        if connection.is_connected():
            print("✅ Connected to MySQL")
            return connection
    except Error as e:
        print(f"MySQL Error: {e}")
    return None

# ✅ PostgreSQL Connection
def create_postgres_connection():
    try:
        connection = psycopg2.connect(
            host=Config.PG_HOST,
            port=Config.PG_PORT,
            user=Config.PG_USER,
            password=Config.PG_PASSWORD,
            dbname=Config.PG_DB
        )
        print("✅ Connected to PostgreSQL")
        return connection
    except OperationalError as e:
        print(f"PostgreSQL Error: {e}")
    return None

# Optional: Run directly to test connection
if __name__ == "__main__":
    create_mysql_connection()
    create_postgres_connection()
