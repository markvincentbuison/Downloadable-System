import mysql.connector

try:
    connection = mysql.connector.connect(
        host="localhost",
        user="your_mysql_user",
        password="your_mysql_password",
        database="your_mysql_database"
    )
    cursor = connection.cursor()
    cursor.execute("SELECT NOW();")
    result = cursor.fetchone()
    print(f"MySQL connection successful. Server time: {result[0]}")
except Exception as e:
    print("Error connecting to MySQL:", e)
finally:
    if connection:
        cursor.close()
        connection.close()
