import firebase_admin
from firebase_admin import credentials, db
import datetime
from flask import Flask, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

current_datetime = datetime.datetime.now()

# Initialize Firebase Admin SDK with service account key and your Firebase project URL
cred = credentials.Certificate("credentials.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://test-e3dc4-default-rtdb.europe-west1.firebasedatabase.app/'
})

# Get a reference to your Firebase Realtime Database
ref = db.reference('/')

@app.route('/')
def hello_world():
    return 'Working'


@app.route('/display')
def display_items():
    # Get all items from the 'Events' node in the database
    events = ref.child('Events').get()

    # Pass the events data to the HTML template for rendering
    return events

if __name__ == '__main__':
    app.run(debug=True)
