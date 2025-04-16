from flask import Flask, redirect, url_for, session
from app.routes.routes import routes
from app.extensions.mail import mail
from flask_dance.contrib.google import make_google_blueprint, google
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def create_app():
    app = Flask(__name__)

    # Secret key (move this to your .env file as well for security)
    app.secret_key = os.getenv('SECRET_KEY', 'fallback_secret')  # Fallback for dev

    # Flask-Mail config using environment variables
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME')

    # Google OAuth config (Flask-Dance)
    app.config['GOOGLE_OAUTH_CLIENT_ID'] = os.getenv('GOOGLE_OAUTH_CLIENT_ID')
    app.config['GOOGLE_OAUTH_CLIENT_SECRET'] = os.getenv('GOOGLE_OAUTH_CLIENT_SECRET')

    # Initialize Flask-Mail
    mail.init_app(app)

    # Create Google OAuth blueprint
    google_bp = make_google_blueprint(
        client_id=app.config['GOOGLE_OAUTH_CLIENT_ID'],
        client_secret=app.config['GOOGLE_OAUTH_CLIENT_SECRET'],
        redirect_to='routes.google_authorized'  # Make sure this matches the route in routes.py
    )
    app.register_blueprint(google_bp, url_prefix='/google_login')

    # Register main blueprint
    app.register_blueprint(routes)

    return app