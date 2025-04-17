import os
from dotenv import load_dotenv

load_dotenv()  # This will load environment variables from your .env file

class Config:
    SECRET_KEY = 'your_secret_key_here'

    # MySQL Configuration
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'your-render-mysql-host')
    MYSQL_PORT = os.getenv('MYSQL_PORT', 3306)
    MYSQL_USER = os.getenv('MYSQL_USER', 'your-database-user')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'your-database-password')
    MYSQL_DB = os.getenv('MYSQL_DB', 'your-database-name')

    # SQLAlchemy configuration (if using SQLAlchemy)
    SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
