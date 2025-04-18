from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_mail import Message
from flask_dance.contrib.google import google
from app.mysql_connect import create_connection
from app.extensions.mail import mail
from app.utils import (generate_token, send_email, send_verification_email, send_reset_email)
import bcrypt
import re
import mysql.connector
from datetime import datetime, timedelta
import logging
from app.mysql_connect import create_mysql_connection, create_postgres_connection
import logging
from flask import Blueprint
from app.mysql_connect import create_mysql_connection, create_postgres_connection
# =======show all table===================
from flask import Blueprint, render_template
# ==========================
# ======================
# Blueprint

# ==========================
routes = Blueprint('routes', __name__)
logging.basicConfig(level=logging.DEBUG)

# ==========================
# Helper Functions
# ==========================
def validate_username(username):
    # Validate the format and length of the username
    if len(username) < 3 or len(username) > 11:
        return "Username must be between 3 and 11 characters."
    if not re.match("^[A-Za-z0-9]*$", username):
        return "Username can only contain letters and numbers."
    return None

def hash_password(password):
    # Hash a password using bcrypt
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)

def send_verification_email_function(email, token):
    # Send a simple verification email
    subject = "Email Verification"
    verification_link = url_for('routes.verify_email', token=token, _external=True)
    body = f"Please verify your email by clicking the following link: {verification_link}"
    send_email(subject, body, email)

# ==========================
# Routes
# ==========================

@routes.route('/')
def index():
    # Render the landing page (login/signup page)
    return render_template('index.html')

# ==========================
@routes.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    conn_mysql = create_mysql_connection()
    conn_postgres = create_postgres_connection()

    if not conn_mysql and not conn_postgres:
        flash('Database connection failed (LOGIN). Please try again later.', 'danger')
        return redirect(url_for('routes.index'))

    try:
        conn = conn_mysql if conn_mysql else conn_postgres
        cursor = conn.cursor()

        # PostgreSQL uses %s, MySQL also uses %s in most connectors (e.g., mysql-connector)
        cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user and bcrypt.checkpw(password.encode('utf-8'), user[2].encode('utf-8')):
            session['user_id'] = user[0]
            session['username'] = user[1]
            session['is_admin'] = user[-1]  # assuming is_admin is last column
            return redirect(url_for('routes.dashboard'))

        flash('Invalid credentials, please try again.', 'danger')
        return redirect(url_for('routes.index'))

    except Exception as e:
        app.logger.error(f"Login error: {e}")
        flash('An error occurred during login. Please try again later.', 'danger')
        return redirect(url_for('routes.index'))

# =========================================
# Dashboard Route Login (Admin/User Based)
# =========================================
@routes.route('/dashboard')
def dashboard():
    # Check if the user is logged in
    if 'user_id' not in session:
        flash('You need to login to access the system', 'warning')
        return redirect(url_for('routes.index'))

    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT username, is_verified, is_admin FROM users WHERE id=%s", (session['user_id'],))
    user = cursor.fetchone()
    
    cursor.close()
    conn.close()

    if user:
        session['is_admin'] = user[2]  # ensure session is always synced
        if user[2]:  # Admin
            # Render admin dashboard if the user is an admin
            return render_template('admin_dashboard.html', username=user[0], is_verified=user[1])
        else:  # Regular user
            # Render regular user dashboard
            return render_template('dashboard.html', username=user[0], is_verified=user[1])

    flash('User not found. Please login again.', 'danger')
    return redirect(url_for('routes.logout'))

@routes.route('/logout')
def logout():
    # Clear the session and log out the user
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('routes.index'))

@routes.route('/signup', methods=['POST'])
def signup():
    username = request.form.get('username')
    password = request.form.get('password')
    email = request.form.get('email_address')
    confirmation_password = request.form.get('confirm_password')

    # Debugging log
    logging.debug(f"Received signup data: username={username}, email={email}")
    
    if not email:
        flash('Email address is required.', 'danger')
        return redirect(url_for('routes.index'))

    if (err := validate_username(username)):
        flash(err, 'danger')
        return redirect(url_for('routes.index'))

    if password != confirmation_password:
        flash('Passwords do not match.', 'danger')
        return redirect(url_for('routes.index'))

    hashed_password = hash_password(password)
    verification_token = generate_token()
    verification_expiry = datetime.utcnow() + timedelta(hours=1)

    try:
        conn = create_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username=%s OR email_address=%s", (username, email))
        if cursor.fetchone():
            flash('Username or Email already exists.', 'danger')
            return redirect(url_for('routes.index'))

        cursor.execute(""" 
            INSERT INTO users (username, password, email_address, verification_token, verification_token_expiry, is_verified)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (username, hashed_password, email, verification_token, verification_expiry, 0))
        conn.commit()

        send_verification_email(email, verification_token, username)
        flash('Signup successful. Check your email to verify your account.', 'success')

    except Exception as e:
        logging.error(f"Signup error: {e}")
        flash('An error occurred during signup. Please try again.', 'danger')
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('routes.index'))

@routes.route('/verify-email/<token>')
def verify_email(token):
    # Handle email verification
    conn = create_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM users WHERE verification_token=%s", (token,))
        user = cursor.fetchone()

        if user:
            cursor.execute(
                "UPDATE users SET is_verified=1, verification_token=NULL WHERE verification_token=%s",
                (token,)
            )
            conn.commit()
            flash("Email verified successfully.", "success")
            return redirect(url_for('routes.dashboard'))
        else:
            flash("Invalid or expired verification link.", "danger")

    except mysql.connector.Error as e:
        print(f"Error during email verification: {e}")
        conn.rollback()
        flash("An error occurred while verifying your email.", "danger")

    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('routes.index'))


@routes.route('/forgot-password', methods=['POST'])
def forgot_password():
    # Handle forgot password functionality
    email = request.form.get('forgot_email')
    if not email:
        flash('Please enter your email address.', 'warning')
        return redirect(url_for('routes.index'))
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email_address=%s", (email,))
    user = cursor.fetchone()
    cursor.fetchall()
    if user:
        reset_token = generate_token()
        reset_expiry = datetime.utcnow() + timedelta(hours=1)
        cursor.execute("UPDATE users SET reset_token=%s, reset_token_expiry=%s WHERE email_address=%s",(reset_token, reset_expiry, email))
        conn.commit()
        send_reset_email(email, reset_token, user[1])  # Pass username (user[1] is the username)
        flash('A password reset link has been sent to your email.', 'info')
    else:
        flash('Email not found. Please try again.', 'danger')
    cursor.close()
    conn.close()
    return redirect(url_for('routes.index'))

@routes.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    # Handle GET request - show password reset form
    if request.method == 'GET':
        return render_template('user_reset_password.html', token=token)

    # Handle POST request - process password reset
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')

    if not new_password or not confirm_password:
        flash("Please fill out both fields.", "danger")
        return redirect(url_for('routes.user_reset_password', token=token))

    if new_password != confirm_password:
        flash("Passwords do not match.", "danger")
        return redirect(url_for('routes.user_reset_password', token=token))

    hashed_password = hash_password(new_password)

    conn = create_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "SELECT reset_token_expiry FROM users WHERE reset_token=%s", (token,)
        )

        if not (result := cursor.fetchone()):
            flash("Invalid or expired reset token.", "danger")
        else:
            expiry_time = result[0]
            if datetime.utcnow() > expiry_time:
                flash("Reset token has expired. Please request a new one.", "danger")
            else:
                cursor.execute(
                    """
                    UPDATE users
                    SET password=%s, reset_token=NULL, reset_token_expiry=NULL
                    WHERE reset_token=%s
                    """,
                    (hashed_password, token)
                )
                conn.commit()
                flash("Your password has been reset successfully.", "success")

    except Exception as e:
        print("Reset password error:", e)
        flash("An error occurred while resetting the password.", "danger")

    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('routes.index'))


@routes.route('/send-verification-email', methods=['POST'])
def send_verification_email_route_dashboard():
    # Ensure user is logged in
    user_id = session.get('user_id')
    if not user_id:
        flash('You need to be logged in to send a verification email.', 'warning')
        return redirect(url_for('routes.index'))

    conn = create_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT email_address FROM users WHERE id=%s", (user_id,))
        user = cursor.fetchone()

        if user:
            token = generate_token()
            cursor.execute(
                "UPDATE users SET verification_token=%s WHERE id=%s",
                (token, user_id)
            )
            conn.commit()
            send_verification_email_function(user[0], token)
            flash('Verification email sent. Please check your inbox.', 'success')
        else:
            flash('User not found.', 'danger')

    except Exception as e:
        print("Email verification error:", e)
        flash('An error occurred while sending the verification email.', 'danger')

    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('routes.dashboard'))


# ==========================
# Google OAuth Routes
# ==========================
@routes.route("/login/google")
def google_login():
    # Google OAuth login route
    return redirect(url_for("google.login"))

@routes.route("/google_login/authorized")
def google_authorized():
    # Google OAuth authorization
    if google.authorized:
        resp = google.get("/oauth2/v2/userinfo")
        if resp.ok:
            user_data = resp.json()
            session['user_data'] = user_data
            flash(f"Welcome {user_data['email']}! Logged in with Google.", "success")
            return redirect(url_for("routes.user_dashboard"))
        else:
            flash("Failed to fetch user info from Google.", "danger")
    else:
        flash("Authorization failed or denied.", "danger")
    return redirect(url_for("routes.index"))

#===============call the browser name system_config.html==================#
@routes.route("/manage-user")
def system_configuration():
    # Render system configuration page (admin)
    return render_template("admin_manage_user.html")

@routes.route("/view-stats")
def system_view_stats():
    # Render system configuration page (admin)
    return render_template("admin_view_stats.html")

@routes.route("/activity-logs")
def activity_logs():
    # Render system configuration page (admin)
    return render_template("admin_activity_logs.html")

 

#===================function fo modal show all databases==============#

#===================function fo modal show all databases==============#
# ==========================
# System Configuration Panel
# ==========================

@routes.route('/system-config', methods=['GET', 'POST'])
def system_config():
    if 'user_id' not in session or not session.get('is_admin'):
        flash('Admin access required to view this page.', 'danger')
        return redirect(url_for('routes.index'))

    search_query = request.args.get('search_query', '')
    try:
        conn = create_connection()
        cursor = conn.cursor()

        if search_query:
            # Use a LIKE query for partial matching (id or email)
            query = """ 
                SELECT id, username, password, email_address, verification_token,
                       verification_token_expiry, is_verified, google_id, reset_token,
                       reset_token_expiry, is_admin, created_at
                FROM downloadable_apps.users
                WHERE id LIKE %s OR email_address LIKE %s;
            """
            cursor.execute(query, (f"%{search_query}%", f"%{search_query}%"))
        else:
            # If no search query, retrieve all users
            cursor.execute("""SELECT id, username, password, email_address, verification_token,verification_token_expiry, is_verified, google_id, reset_token,reset_token_expiry, is_admin, created_at FROM downloadable_apps.users;""")
        users_data = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template("admin_system_config.html", users=users_data, search_query=search_query)
    except Exception as e:
        print("Error loading system config:", e)
        flash("Failed to load system configuration.", "danger")
        return redirect(url_for('routes.admin_system_config'))
#-----------------------------------------------#



#-------------TEST---------------#

def create_users_table():
    conn = psycopg2.connect(
        dbname="downloadable_app",
        user="root",
        password="rVIIDKOozMHH8LPqHT0dC3EfPxwFN2nP",
        host="dpg-d00ihffgi27c73bb4afg-a.virginia-postgres.render.com",
        port="5432"
    )
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(100) NOT NULL UNIQUE,
            email VARCHAR(255) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL,
            is_verified BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    cur.close()
    conn.close()
    print("✅ Users table created.")

@routes.route('/initdb')
def initdb():
    try:
        create_users_table()
        return "Users table created successfully!"
    except Exception as e:
        return f" Error creating table: {e}"
