import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

class Config:
    # MySQL Configuration for Render (Uncomment if you're still using MySQL)
    # MYSQL_HOST = os.getenv('MYSQL_HOST', 'downloadable-system.onrender.com')
    # MYSQL_PORT = os.getenv('MYSQL_PORT', 3306)
    # MYSQL_USER = os.getenv('MYSQL_USER', 'your_user')
    # MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'your_password')
    # MYSQL_DB = os.getenv('MYSQL_DB', 'downloadable_db')

    # PostgreSQL Configuration for Render
    PG_HOST = os.getenv('PG_HOST', 'dpg-d00ai0ngi27c73b38t30-a.virginia-postgres.render.com')
    PG_PORT = os.getenv('PG_PORT', '5432')
    PG_USER = os.getenv('PG_USER', 'downloadable_db_user')  # Correct PostgreSQL user
    PG_PASSWORD = os.getenv('PG_PASSWORD', 'aGeyZP2xfeIfmNnbKByHn768lILopUhT')
    PG_DB = os.getenv('PG_DB', 'downloadable_db')  # Correct database name for PostgreSQL

    # Optional: Other configurations
    SECRET_KEY = os.getenv('SECRET_KEY', 'supersecretkey')
    MAIL_USERNAME = os.getenv('MAIL_USERNAME', 'your_email@example.com')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', 'your_email_password')
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = os.getenv('MAIL_PORT', '587')
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True') == 'True'
    MAIL_USE_SSL = os.getenv('MAIL_USE_SSL', 'False') == 'True'
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', 'your_email@example.com')

