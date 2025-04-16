# run.py
from app import create_app
import os

# Create the Flask application
app = create_app()

if __name__ == "__main__":
    # Define the paths to your certificate and key
    cert_path = os.path.join(os.getcwd(), 'certs', 'server.crt')
    key_path = os.path.join(os.getcwd(), 'certs', 'server.key')

    # Ensure the certificate and key files exist
    if os.path.exists(cert_path) and os.path.exists(key_path):
        app.run(debug=True, host='0.0.0.0', port=5000, ssl_context=(cert_path, key_path))
    else:
        print("SSL certificate or key file not found.")
        app.run(debug=True, host='0.0.0.0', port=5000)
