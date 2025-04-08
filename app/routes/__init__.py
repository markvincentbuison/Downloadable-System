from flask import Flask
from app.routes.routes import index  # Import the route function

def create_app():
    app = Flask(__name__)

    # Register routes
    app.add_url_rule('/', 'index', index)

    return app
