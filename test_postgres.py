# test_postgres.py

import psycopg2

try:
    connection = psycopg2.connect(
        dbname="downloadable_app",
        user="root",
        password="rVIIDKOozMHH8LPqHT0dC3EfPxwFN2nP",
        host="dpg-d00ihffgi27c73bb4afg-a.virginia-postgres.render.com",
        port="5432"
    )
    cursor = connection.cursor()
    cursor.execute("SELECT NOW();")
    result = cursor.fetchone()
    print(f"PostgreSQL connection successful. Server time: {result[0]}")
except Exception as e:
    print("Error connecting to PostgreSQL:", e)
finally:
    if connection:
        cursor.close()
        connection.close()
