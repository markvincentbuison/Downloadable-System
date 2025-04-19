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
# =====this below for for render connecting 24/7=====================
import threading
import time
import requests
# =====THIS IS FOR GOOGLE=====================
from flask import redirect, url_for, session, flash
from flask_dance.contrib.google import google
# ==========================
# Blueprint
# ==========================
routes = Blueprint('routes', __name__)
logging.basicConfig(level=logging.DEBUG)

# ==========================
# Helper Functions
# ==========================
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

#===============Routes===========================================================================================
@routes.route('/')
def index():
     # Check if the user is already logged in
    if 'user_id' in session:
        return redirect(url_for('routes.dashboard'))  # Redirect to dashboard if already logged in

    return render_template('index.html')
#==============Login=============================================================================================
@routes.route('/login', methods=['POST'])
def login():
      # Prevent logged-in users from going back to login page
    if 'user_id' in session:
        return redirect(url_for('routes.dashboard'))  # Redirect to dashboard if already logged in

    username = request.form['username']
    password = request.form['password']
    # Try creating a connection
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
#================Signup=========================================================================================
@routes.route('/signup', methods=['POST'])
def signup():
    username = request.form.get('username')
    password = request.form.get('password')
    email = request.form.get('email_address')
    confirmation_password = request.form.get('confirm_password')
    if not email:
        flash('Email address is required.', 'danger')
        return redirect(url_for('routes.index'))
    if (err := validate_username(username)):
        flash(err, 'danger')
        return redirect(url_for('routes.index'))
    if password != confirmation_password:
        flash('Passwords do not match.', 'danger')
        return redirect(url_for('routes.index'))

    try:
        # 🔐 Hash password using bcrypt
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        verification_token = generate_token()
        verification_expiry = datetime.utcnow() + timedelta(hours=1)
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=%s OR email_address=%s", (username, email))
        if cursor.fetchone():
            flash('Username or Email already exists.', 'danger')
            return redirect(url_for('routes.index'))
        cursor.execute("""
            INSERT INTO users (username, password, email_address, verification_token, verification_token_expiry, is_verified)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (username, hashed_password, email, verification_token, verification_expiry, False))
        conn.commit()
        send_verification_email(email, verification_token, username)
        flash('Signup successful. Check your email to verify your account.', 'success')
    except Exception as e:
        print("Signup error:", e)
        flash('An error occurred during signup. Please try again.', 'danger')
    finally:
        if cursor: cursor.close()
        if conn: conn.close()
    return redirect(url_for('routes.index'))
#=============Dashboard==============================================================================================
@routes.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('You need to login to access the system', 'warning')
        return redirect(url_for('routes.index'))
    conn = create_connection()
    cursor = conn.cursor()
    # ✅ Fetch username, is_admin, and is_verified
    cursor.execute("SELECT username, is_admin, is_verified FROM users WHERE id=%s", (session['user_id'],))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    if user:
        username, is_admin, is_verified = user
        session['is_admin'] = is_admin
        session['is_verified'] = is_verified  # ✅ Save to session for reuse if needed
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

# =============== Manage User Routes ========================

# Route to view all users (Admin only)
@routes.route('/manage-users')
def manage_users():
    if 'user_id' not in session or not session.get('is_admin'):
        flash('You do not have permission to view this page.', 'danger')
        return redirect(url_for('routes.dashboard'))
    
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, username, email_address, is_verified, is_admin FROM users")
        users = cursor.fetchall()
    except Exception as e:
        print("Error fetching users:", e)
        flash("An error occurred while fetching users.", 'danger')
        return redirect(url_for('routes.dashboard'))
    finally:
        cursor.close()
        conn.close()

    return render_template('admin_manage_users.html', users=users)

# ---------------------------------------------------------------------------------
# Route to update user role (Admin only)
@routes.route('/update-user-role/<int:user_id>', methods=['POST'])
def update_user_role(user_id):
    if 'user_id' not in session or not session.get('is_admin'):
        flash('You do not have permission to perform this action.', 'danger')
        return redirect(url_for('routes.dashboard'))

    new_role = request.form.get('new_role')  # Expected values: 'admin' or 'user'
    if new_role not in ['admin', 'user']:
        flash('Invalid role.', 'danger')
        return redirect(url_for('routes.manage_users'))

    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE users SET is_admin=%s WHERE id=%s", (1 if new_role == 'admin' else 0, user_id))
        conn.commit()
        flash(f'User role updated to {new_role}.', 'success')
    except Exception as e:
        print("Error updating user role:", e)
        flash("An error occurred while updating the user role.", 'danger')
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('routes.manage_users'))


# Route to delete a user (Admin only)
@routes.route('/delete-user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    if 'user_id' not in session or not session.get('is_admin'):
        flash('You do not have permission to perform this action.', 'danger')
        return redirect(url_for('routes.dashboard'))

    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM users WHERE id=%s", (user_id,))
        conn.commit()
        flash('User deleted successfully.', 'success')
    except Exception as e:
        print("Error deleting user:", e)
        flash("An error occurred while deleting the user.", 'danger')
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('routes.manage_users'))

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
@routes.route('/login/google')  # ✅ Matches the link in HTML
def google_login():
    if not google.authorized:
        return redirect(url_for('google.login'))

    # Fetch the user's information from Google
    response = google.get('/plus/v1/people/me')
    if response.ok:
        google_user_info = response.json()
        google_id = google_user_info['id']
        google_email = google_user_info['emails'][0]['value']
        google_name = google_user_info['displayName']

        from app.models.user_model import get_or_create_google_user
        user = get_or_create_google_user(google_id, google_email, google_name)

        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['is_admin'] = user['is_admin']
            return redirect(url_for('routes.dashboard'))
        else:
            flash('Failed to create or retrieve user.', 'danger')
            return redirect(url_for('routes.index'))

    flash('Unable to fetch your Google information.', 'danger')
    return redirect(url_for('routes.index'))

# # ===================== Google Login OAuth ==========================
# app/routes/routes.py

from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Access environment variables
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID_LOCAL" if os.getenv("FLASK_ENV") == "development" else "GOOGLE_CLIENT_ID_PROD")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET_LOCAL" if os.getenv("FLASK_ENV") == "development" else "GOOGLE_CLIENT_SECRET_PROD")

# Now you can use GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET in your routes
