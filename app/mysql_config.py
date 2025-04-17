import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # MySQL Configuration for Render
    MYSQL_HOST = os.getenv('DB_HOST', 'dpg-cj3gnl65m9wdoas91k6g-a.virginia-mysql.render.com')  # Correct MySQL host for Render
    MYSQL_USER = os.getenv('DB_USER', 'downloadable_db_user')  # Your MySQL username
    MYSQL_PASSWORD = os.getenv('DB_PASSWORD', 'aGeyZP2xfeIfmNnbKByHn768lILopUhT')  # Your MySQL password
    MYSQL_DB = os.getenv('DB_NAME', 'downloadable_db')  # Your MySQL database name

    # PostgreSQL Configuration (if needed)
    PG_HOST = os.getenv('PG_HOST', 'dpg-d00ai0ngi27c73b38t30-a.virginia-postgres.render.com')
    PG_PORT = os.getenv('PG_PORT', '5432')
    PG_USER = os.getenv('PG_USER', 'downloadable_db_user')
    PG_PASSWORD = os.getenv('PG_PASSWORD', 'aGeyZP2xfeIfmNnbKByHn768lILopUhT')
    PG_DB = os.getenv('PG_NAME', 'downloadable_db')

    # Optional: Other configurations for your app
    SECRET_KEY = os.getenv('SECRET_KEY', 'supersecretkey')  # Your Flask secret key
    MAIL_USERNAME = os.getenv('MAIL_USERNAME', 'your_email@example.com')  # Email username
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', 'your_email_password')  # Email password
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')  # Email SMTP server
    MAIL_PORT = os.getenv('MAIL_PORT', '587')  # Email SMTP port
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True') == 'True'  # Whether to use TLS encryption
    MAIL_USE_SSL = os.getenv('MAIL_USE_SSL', 'False') == 'True'  # Whether to use SSL encryption
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', 'your_email@example.com')  # Default sender email
