# mysql_connect.py

# ✅ Shared Imports
import mysql.connector
from mysql.connector import Error
import psycopg2
from psycopg2 import OperationalError
from app.mysql_config import Config  # Import Config class to get DB credentials
import os

# ✅ Legacy/Generic MySQL Connection Function
def create_connection(): #connected to login
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
            print("Connected to MySQL")
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
        print("Connected to PostgreSQL")
        return connection
    except OperationalError as e:
        print(f"PostgreSQL Error: {e}")
    return None

# ✅ Unified Connection Function (Dynamic MySQL / PostgreSQL Selection)
def create_dynamic_connection():
    try:
        # Check if the environment is set to production (for PostgreSQL)
        if os.getenv('FLASK_ENV') == 'production':
            connection = psycopg2.connect(
                host=Config.PG_HOST,
                port=Config.PG_PORT,
                user=Config.PG_USER,
                password=Config.PG_PASSWORD,
                dbname=Config.PG_DB
            )
            print("Connected to PostgreSQL")
        else:
            # Local environment (for MySQL)
            connection = mysql.connector.connect(
                host=Config.MYSQL_HOST,
                user=Config.MYSQL_USER,
                password=Config.MYSQL_PASSWORD,
                database=Config.MYSQL_DB,
                port=Config.MYSQL_PORT
            )
            if connection.is_connected():
                print("Connected to MySQL")
        
        return connection
    
    except (Error, OperationalError) as e:
        print(f"Database Connection Error: {e}")
        return None

# ✅ Test connections when running this file directly
if __name__ == "__main__":
    create_connection()        # Legacy MySQL Connection Test
    create_mysql_connection()  # Explicit MySQL Connection Test
    create_postgres_connection()  # PostgreSQL Connection Test
    create_dynamic_connection()  # Dynamic MySQL or PostgreSQL Connection Test
