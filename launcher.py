import webbrowser
import subprocess
import threading

def run_flask():
    subprocess.call(["python", "run.py"])

# Run Flask app in a separate thread
threading.Thread(target=run_flask).start()

# Open the app in the default browser
webbrowser.open("http://192.168.0.100:5000")
