import firebase_admin
from firebase_admin import credentials, db
import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__, template_folder="templates")  # Replace "templates" with the actual path to your static folder
CORS(app, resources={r"/*": {"origins": "*"}})

# Get the current date and time
current_datetime = datetime.datetime.now()

# Initialize Firebase Admin SDK with service account key and your Firebase project URL
cred = credentials.Certificate("credentials.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://test-e3dc4-default-rtdb.europe-west1.firebasedatabase.app/'
})

# Get a reference to your Firebase Realtime Database
ref = db.reference('/')

# Define a route to add events to the database
@app.route('/add', methods=['POST'])
def add_events():
    # Define the Events data
    events = [
        {"Event": "Jazz konsert", "dato": current_datetime.isoformat(), "Address": "Molde", "info": "Molde vs Ålesund"},
        {"Event": "Quiz", "dato": current_datetime.isoformat(), "Address": "Molde", "info": "Molde vs Ålesund"},
        {"Event": "Football kamp", "dato": current_datetime.isoformat(), "Address": "Molde", "info": "Molde vs Ålesund"},
    ]

    # Push each Event to the database
    for event in events:
        ref.child('Events').push(event)

    return jsonify({"message": "Events added to the database."})

if __name__ == "__main__":
    app.run(port=8080, debug=True, host="0.0.0.0")
