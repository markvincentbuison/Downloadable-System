# mysql_connect.py

import os
import mysql.connector
from mysql.connector import Error as MySQLError
import psycopg2
from psycopg2 import OperationalError as PostgresError
from app.mysql_config import Config  # Ensure Config class has both MySQL and PostgreSQL details
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

USE_DB = os.getenv('USE_DB', 'mysql').lower()  # Choose between 'mysql' or 'postgres'

# ✅ MySQL Connection
def create_mysql_connection():
    try:
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
    except MySQLError as e:
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
    except PostgresError as e:
        print(f"PostgreSQL Error: {e}")
    return None

# ✅ Unified DB Connector
def create_connection():
    try:
        if USE_DB == 'postgres':
            return create_postgres_connection()
        else:
            return create_mysql_connection()
    except (MySQLError, PostgresError) as e:
        print(f"Database Connection Error: {e}")
        return None

# ✅ Optional: Manual test
if __name__ == "__main__":
    conn = create_connection()
    if conn:
        print("Connection test successful!")
        conn.close()
    else:
        print("Connection test failed.")

