from flask import render_template
from app.mysql_connect import create_connection  # Import the connection function

def index():
    print("Rendering index.html")  # This will print in your console
    
    # Create a connection to MySQL
    conn = create_connection()
    
    if conn is None:
        return "Failed to connect to the database.", 500
    
    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    # Execute a sample query (replace with your actual query)
    cursor.execute("SELECT * FROM user_data")
    
    # Fetch all results from the query
    results = cursor.fetchall()

    # Close the cursor and connection
    cursor.close()
    conn.close()

    # Return the results to the template
    return render_template('index.html', data=results)
