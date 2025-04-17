# mysql_connect.py

# ✅ Shared Imports
import mysql.connector
from mysql.connector import Error
import psycopg2
from psycopg2 import OperationalError
from app.mysql_config import Config  # Import Config class to get DB credentials

# ✅ Legacy/Generic MySQL Connection Function
def create_connection():
    try:
        connection = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DB
        )

        if connection.is_connected():
            print("Successfully connected to MySQL")
            return connection
        else:
            print("Failed to connect to the database")
            return None

    except Error as e:
        print(f"Error: {e}")
        return None

# ✅ Named MySQL Connection (same functionality, more explicit)
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

# ✅ Test connections when running this file directly
if __name__ == "__main__":
    create_connection()
    create_mysql_connection()
    create_postgres_connection()
