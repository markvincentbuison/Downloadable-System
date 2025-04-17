import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

class Config:
    # Optional: Other configurations for your app
    SECRET_KEY = os.getenv('SECRET_KEY', 'supersecretkey')
    MAIL_USERNAME = os.getenv('MAIL_USERNAME', 'your_email@example.com')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', 'your_email_password')
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = os.getenv('MAIL_PORT', '587')
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True') == 'True'
    MAIL_USE_SSL = os.getenv('MAIL_USE_SSL', 'False') == 'True'
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', 'your_email@example.com')

    # MySQL Configuration for Local Development
    MYSQL_HOST = os.getenv('DB_HOST_LOCAL', 'localhost')  # Host of your MySQL DB (default to localhost for local)
    MYSQL_PORT = os.getenv('DB_PORT_LOCAL', 3306)  # Default MySQL port
    MYSQL_USER = os.getenv('DB_USER_LOCAL', 'root')  # Your MySQL username
    MYSQL_PASSWORD = os.getenv('DB_PASSWORD_LOCAL', 'tunnerskylitQ1@3')  # Your MySQL password
    MYSQL_DB = os.getenv('DB_NAME_LOCAL', 'downloadable_apps')  # Your MySQL database name

    # PostgreSQL Configuration for Production
    PG_HOST = os.getenv('DB_HOST_PROD', 'dpg-d00ihffgi27c73bb4afg-a.virginia-postgres.render.com')  # Host of your PostgreSQL DB
    PG_PORT = os.getenv('DB_PORT_PROD', '5432')  # PostgreSQL port
    PG_USER = os.getenv('DB_USER_PROD', 'root')  # PostgreSQL username
    PG_PASSWORD = os.getenv('DB_PASSWORD_PROD', 'rVIIDKOozMHH8LPqHT0dC3EfPxwFN2nP')  # PostgreSQL password
    PG_DB = os.getenv('DB_NAME_PROD', 'downloadable_db')  # PostgreSQL database name


