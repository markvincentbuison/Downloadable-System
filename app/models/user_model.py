from mysql_connect import create_connection

def get_or_create_google_user(google_id, email, username):
    conn = create_connection()
    if conn is None:
        print("[ERROR] Failed DB connection.")
        return None

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE google_id = %s", (google_id,))
        user = cursor.fetchone()

        if user:
            return {
                'id': user['id'],
                'username': user['username'],
                'is_admin': user['is_admin']
            }

        # If user does not exist, insert new one
        cursor.execute("""
            INSERT INTO users (google_id, email, username, is_admin)
            VALUES (%s, %s, %s, %s)
        """, (google_id, email, username, 0))
        conn.commit()

        return {
            'id': cursor.lastrowid,
            'username': username,
            'is_admin': 0
        }
    except Exception as e:
        print("[DB ERROR]", e)
        return None
    finally:
        cursor.close()
        conn.close()
