import random
import string
import re
import bcrypt
from flask_mail import Message
from flask import url_for
from app.extensions.mail import mail
import secrets

# ============================================
# Helper Functions
# ============================================

def generate_token(length=32):
    """Generates a secure random token of specified length."""
    return secrets.token_urlsafe(length)


def send_email(subject, body, recipient_email):
    """Sends an email with the given subject, body, and recipient."""
    msg = Message(subject=subject, recipients=[recipient_email])
    msg.body = body
    try:
        mail.send(msg)
        print(f"[✓] Email sent to {recipient_email}")
    except Exception as e:
        print(f"[!] Failed to send email to {recipient_email}: {e}")


def send_verification_email(email, token,username):
    """Sends a verification email to the user with a unique token."""
    subject = "Email Verification"
    verification_link = url_for('routes.verify_email', token=token, _external=True)
    body = f"""Hi {username},

Thanks for signing up! Please verify your email by clicking the link below:

{verification_link} 

If you did not sign up, please ignore this message.

Best regards,
TunNer Team
"""
    send_email(subject, body, email)


def send_reset_email(email, token,username):
    """Sends a password reset email with a reset token."""
    reset_link = url_for('routes.reset_password', token=token, _external=True)
    subject = "Password Reset Request"
    body = f"""Hi {username},

You requested a password reset. Click the link below to reset your password:

{reset_link}

If you did not request this, you can safely ignore this email.

Best,
TunNer Team
"""
    send_email(subject, body, email)

def validate_username(username):
    """Validates the username based on length and allowed characters."""
    if len(username) < 3 or len(username) > 11:
        return "Username must be between 3 and 11 characters."
    if not re.match("^[A-Za-z0-9]*$", username):
        return "Username can only contain letters and numbers."
    return None


def hash_password(password):
    """Hashes the password using bcrypt and returns the hashed password."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)



