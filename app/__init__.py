import os
from flask import Flask
from flask_dance.contrib.google import make_google_blueprint
from dotenv import load_dotenv
from app.routes.routes import routes
from app.extensions.mail import mail
from datetime import timedelta

# --------------------------------------------------------------------------------------------------------------#
# Load environment variables from .env at the root
load_dotenv()

# --------------------------------------------------------------------------------------------------------------#
def create_app():
    app = Flask(__name__)

    # --------------------------------------------------------------------------------------------------------------#
    # Secret Key - used for session signing and security
    app.secret_key = os.getenv("SECRET_KEY", "fallback_secret")
    
    # --------------------------------------------------------------------------------------------------------------#
    # Session and Remember Me Settings
    app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=30)  # Remember user for 30 days
    app.config['SESSION_PROTECTION'] = 'strong'  # Strong session protection

    # ----------------------------------------------------------------------------------------------------------#
    # Mail Configuration (to be used for password reset and email verification)
    app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER")
    app.config["MAIL_PORT"] = int(os.getenv("MAIL_PORT", 587))
    app.config["MAIL_USE_TLS"] = os.getenv("MAIL_USE_TLS", "True") == "True"
    app.config["MAIL_USE_SSL"] = os.getenv("MAIL_USE_SSL", "False") == "True"
    app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
    app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
    app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL_DEFAULT_SENDER")

    # ----------------------------------------------------------------------------------------------------------#
    # Google OAuth Configuration
    use_production = os.getenv("USE_DB") == "postgres"

    if use_production:
        client_id = os.getenv("GOOGLE_CLIENT_ID_PROD")
        client_secret = os.getenv("GOOGLE_CLIENT_SECRET_PROD")
        redirect_uri = os.getenv("GOOGLE_REDIRECT_URI_PROD")
    else:
        client_id = os.getenv("GOOGLE_CLIENT_ID_LOCAL")
        client_secret = os.getenv("GOOGLE_CLIENT_SECRET_LOCAL")
        redirect_uri = os.getenv("GOOGLE_REDIRECT_URI_LOCAL")

    # Debug prints to help diagnose
    if not client_id or not client_secret:
        print("⚠️ Missing Google OAuth credentials in .env")

    # Create the Google OAuth blueprint
    google_bp = make_google_blueprint(
        client_id=client_id,
        client_secret=client_secret,
        redirect_to='google_login'  # Make sure this route exists in your `routes.py`
    )

    # Register the blueprint with the Flask app
    app.register_blueprint(google_bp, url_prefix='/google_login')

    # ----------------------------------------------------------------------------------------------------------#
    # Initialize Mail
    mail.init_app(app)

    # ----------------------------------------------------------------------------------------------------------#
    # Register routes from routes.py
    app.register_blueprint(routes)

    return app
