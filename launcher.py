import webbrowser
import subprocess
import threading

def run_flask():
    subprocess.call(["python", "run.py"])

# Run Flask app in a separate thread
threading.Thread(target=run_flask).start()

# Get the public ngrok URL (replace this with your actual ngrok URL)
render_url = "https://downloadable-system.onrender.com/"  # Replace with your ngrok URL

# Open the app in the default browser
webbrowser.open(render_url)
