from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_mail import Message
from app.mysql_connect import create_connection
from app.extensions.mail import mail
from app.utils import (generate_token, send_email, send_verification_email, send_reset_email)
import bcrypt
import re
import mysql.connector
from datetime import datetime, timedelta
import logging
import threading
import time
import requests
from flask import redirect, url_for, session, flash
from flask_dance.contrib.google import google

# Blueprint
routes = Blueprint('routes', __name__)
logging.basicConfig(level=logging.DEBUG)

# ===========================
# Helper Functions
# ===========================
def validate_username(username):
    if len(username) < 3 or len(username) > 11:
        return "Username must be between 3 and 11 characters."
    if not re.match("^[A-Za-z0-9]*$", username):
        return "Username can only contain letters and numbers."
    return None

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def send_verification_email_function(email, token):
    subject = "Email Verification"
    verification_link = url_for('routes.verify_email', token=token, _external=True)
    body = f"Please verify your email by clicking the following link: {verification_link}"
    send_email(subject, body, email)

# ===========================
# Routes
# ===========================

@routes.route('/')
def index():
    # Check if the user is already logged in
    if 'user_id' in session:
        return redirect(url_for('routes.dashboard'))  # Redirect to dashboard if already logged in
    return render_template('index.html')

@routes.route('/login', methods=['POST'])
def login():
    # Prevent logged-in users from going back to login page
    if 'user_id' in session:
        return redirect(url_for('routes.dashboard'))  # Redirect to dashboard if already logged in

    username = request.form['username']
    password = request.form['password']
    conn = create_connection()
    if conn is None:
        flash('Failed to connect to the database.', 'danger')
        return redirect(url_for('routes.index'))
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
        user = cursor.fetchone()
    except Exception as e:
        print("[DB ERROR]", e)
        flash('Database error occurred.', 'danger')
        return redirect(url_for('routes.index'))
    finally:
        if conn:
            conn.close()
    
    if user:
        try:
            stored_hash = user[2]  # Assuming 3rd column is password hash
            if stored_hash and isinstance(stored_hash, str):
                stored_hash = stored_hash.encode('utf-8')
                if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
                    session['user_id'] = user[0]
                    session['username'] = user[1]
                    session['is_admin'] = user[-2]
                    return redirect(url_for('routes.dashboard'))
                else:
                    flash('Incorrect password.', 'danger')
            else:
                flash('Invalid password format in the database.', 'danger')
        except ValueError as e:
            print("Bcrypt error:", e)
            flash('Invalid password hash. Please contact support.', 'danger')
    else:
        flash('User not found.', 'danger')

    return redirect(url_for('routes.index'))

# Continue your signup, dashboard, and other routes as you have them...
# Continue your other route definitions...

@routes.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('You need to login to access the system', 'warning')
        return redirect(url_for('routes.index'))
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT username, is_admin, is_verified FROM users WHERE id=%s", (session['user_id'],))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    if user:
        username, is_admin, is_verified = user
        session['is_admin'] = is_admin
        session['is_verified'] = is_verified  # Save to session for reuse if needed
        if is_admin:
            return render_template('admin_dashboard.html', username=username, is_verified=is_verified)
        else:
            return render_template('user_dashboard.html', username=username, is_verified=is_verified)
    flash('User not found. Please login again.', 'danger')
    return redirect(url_for('routes.logout'))


#=============Logout==============================================================================================
@routes.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('routes.index'))
#=============Verify email=========================================================================================
@routes.route('/verify-email/<token>')
def verify_email(token):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM users WHERE verification_token=%s", (token,))
        user = cursor.fetchone()
        if user:
            # Update with TRUE for the boolean field
            cursor.execute("UPDATE users SET is_verified=TRUE, verification_token=NULL WHERE verification_token=%s", (token,))
            conn.commit()
            flash("Email verified successfully.", 'success')
            return redirect(url_for('routes.dashboard'))
        flash("Invalid or expired verification link.", 'danger')
    except mysql.connector.errors.DatabaseError as e:
        print(f"Error during verification: {e}")
        conn.rollback()
        flash("An error occurred while verifying your email.", 'danger')
    finally:
        cursor.close()
        conn.close()
    return redirect(url_for('routes.index'))
#============================FORGOT PASSWORD========================================================================
@routes.route('/forgot-password', methods=['POST'])
def forgot_password():
    email = request.form.get('forgot_email')
    if not email:
        flash('Please enter your email address.', 'warning')
        return redirect(url_for('routes.index'))
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM users WHERE email_address=%s", (email,))
        user = cursor.fetchone()
        if user:
            reset_token = generate_token()
            reset_expiry = datetime.utcnow() + timedelta(hours=1)
            username = user[1]  # Adjust this index if 'username' is at a different position
            cursor.execute(
                "UPDATE users SET reset_token=%s, reset_token_expiry=%s WHERE email_address=%s",
                (reset_token, reset_expiry, email)
            )
            conn.commit()
            send_reset_email(email, reset_token, username)
            flash('A password reset link has been sent to your email.', 'info')
        else:
            flash('Email not found. Please try again.', 'danger')
    except Exception as e:
        print(f"Error during password reset request: {e}")
        conn.rollback()
        flash('An error occurred while processing your request.', 'danger')
    finally:
        cursor.close()
        conn.close()
    return redirect(url_for('routes.index'))
#========================USER RESET PASSWORD========================================================================
@routes.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if request.method == 'GET':
        return render_template('user_reset_password.html', token=token)  # ✅ updated template name
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')
    if not new_password or not confirm_password:
        flash("Please fill out both fields.", "danger")
        return redirect(url_for('routes.reset_password', token=token))
    if new_password != confirm_password:
        flash("Passwords do not match.", "danger")
        return redirect(url_for('routes.reset_password', token=token))
    hashed_password = hash_password(new_password)
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT reset_token_expiry FROM users WHERE reset_token=%s", (token,))
        result = cursor.fetchone()
        if not result:
            flash("Invalid or expired reset token.", "danger")
        else:
            expiry_time = result[0]
            if datetime.utcnow() > expiry_time:
                flash("Reset token has expired. Please request a new one.", "danger")
            else:
                cursor.execute("UPDATE users SET password=%s, reset_token=NULL, reset_token_expiry=NULL WHERE reset_token=%s",(hashed_password, token))
                conn.commit()
                flash("Your password has been reset successfully.", "success")
    except Exception as e:
        print("Reset password error:", e)
        flash("An error occurred while resetting the password.", "danger")
    finally:
        cursor.close()
        conn.close()
    return redirect(url_for('routes.index'))

#============Send Verification Email==================================================================================
@routes.route('/send-verification-email', methods=['POST'])
def send_verification_email_route_dashboard():
    user_id = session.get('user_id')
    if not user_id:
        flash('You need to be logged in to send verification email.', 'warning')
        return redirect(url_for('routes.index'))
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT email_address FROM users WHERE id=%s", (user_id,))
    user = cursor.fetchone()
    if user:
        token = generate_token()
        cursor.execute("UPDATE users SET verification_token=%s WHERE id=%s", (token, user_id))
        conn.commit()
        send_verification_email_function(user[0], token)
        flash('Verification email sent. Please check your inbox.', 'success')
    else:
        flash('User not found.', 'danger')
    cursor.close()
    conn.close()
    return redirect(url_for('routes.dashboard'))

#======================================================================================================================
# ===================== 24/7 Render Keep-Alive ==========================
def ping_self():
    while True:
        try:
            time.sleep(600)  # every 20 minutes
            requests.get("https://downloadable-system.onrender.com/")
        except Exception as e:
            print(f"[Keep-Alive Ping Error] {e}")

keep_alive_thread = threading.Thread(target=ping_self)
keep_alive_thread.daemon = True
keep_alive_thread.start()
#===================================================================================================================================
# ===================== Google OAuth ==========================
@routes.route('/google/authorized')
def google_authorized():
    if not google.authorized:
        flash("Google login failed!", "danger")
        return redirect(url_for('routes.login'))

    # Fetch user info from Google
    resp = google.get("/oauth2/v2/userinfo")
    if not resp.ok:
        flash("Failed to fetch user info.", "danger")
        return redirect(url_for('routes.login'))

    user_info = resp.json()
    email = user_info["email"]
    name = user_info.get("name", "")

    # Check if the user already exists in your database
    # This is an example, modify based on your actual database setup
    user = get_user_by_email(email)  # Replace with your actual DB query logic
    if not user:
        # If the user doesn't exist, register them
        register_new_user(email, name)  # Replace with your actual registration logic

    session['user_email'] = email
    flash(f"Welcome, {name}!", "success")
    return redirect(url_for('routes.dashboard'))

# Example helper functions
def get_user_by_email(email):
    # Query your database to check if user exists by email
    # return user if found, else return None
    pass

def register_new_user(email, name):
    # Register new user in the database
    # Store user information
    pass
# ===================== End of Google OAuth ==========================