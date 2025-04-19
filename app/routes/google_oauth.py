# app/routes/google_oauth.py
from flask import redirect, url_for
from flask_dance.contrib.google import google
from flask_login import login_user
from app.models import User  # Assuming you have a User model for storing user info

def login_with_google():
    if not google.authorized:
        return redirect(url_for('google.login'))  # This will redirect to Google's OAuth
    # The user is already authorized, now you can fetch their info
    google_info = google.get('/plus/v1/people/me')
    if google_info.ok:
        user_info = google_info.json()
        # Logic for creating or logging in a user from the Google data
        user = User.get_by_email(user_info['emails'][0]['value'])  # Example: match by email
        if user:
            login_user(user)
            return redirect(url_for('dashboard'))  # Redirect to your dashboard or wherever
    return redirect(url_for('google.login'))  # In case of any error, redirect to login again

def google_authorized():
    if google.authorized:
        return redirect(url_for('dashboard'))  # Where to redirect after successful OAuth
    return redirect(url_for('google.login'))  # If unauthorized, redirect back to Google login
