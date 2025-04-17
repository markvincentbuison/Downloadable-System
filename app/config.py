import os
from dotenv import load_dotenv

load_dotenv()  # This will load environment variables from your .env file

class Config:
    # MySQL Configuration (from environment variables)
    MYSQL_HOST = os.getenv('MYSQL_HOST')
    MYSQL_PORT = os.getenv('MYSQL_PORT', 3306)  # Default to 3306 if not set
    MYSQL_USER = os.getenv('MYSQL_USER')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
    MYSQL_DB = os.getenv('MYSQL_DB')

    # Construct the SQLAlchemy database URI using the environment variables
    SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}'

    # Disable SQLAlchemy modifications tracking (can be enabled if needed)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
