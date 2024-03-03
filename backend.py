# app.py
import firebase_admin
from firebase_admin import credentials, db
import datetime
from flask import Flask, render_template, request, redirect, jsonify
from flask_cors import CORS

app = Flask(__name__, template_folder='templates')
CORS(app, resources={r"/*": {"origins": "*"}})

# Initialize Firebase Admin SDK with service account key and your Firebase project URL
cred = credentials.Certificate("credentials.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://test-e3dc4-default-rtdb.europe-west1.firebasedatabase.app/'
})

# Get a reference to your Firebase Realtime Database
ref = db.reference('/')

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/display')
def display_items():
    # Get all items from the 'Events' node in the database
    events_data = ref.child('Events').get()

    # Format the data similar to your second code snippet
    formatted_events = []
    for event_id, event_data in events_data.items():
        formatted_event = {
            'event_id': event_id,
            'dato': event_data.get('dato', ''),
            'event': event_data.get('Event', ''),
            'info': event_data.get('info', ''),
            'klokkeslett': event_data.get('klokkeslett', ''),
            'sted': event_data.get('Address', ''),
        }
        formatted_events.append(formatted_event)

    return render_template('display.html', events=formatted_events)

@app.route('/form_page')
def form_page():
    return render_template('form_page.html')

@app.route('/submit', methods=['POST'])
def submit_form():
    try:
        # Get form data from the request
        form_data = request.get_json()

        # Add the current timestamp to the form data
        form_data['timestamp'] = datetime.datetime.now().isoformat()

        # Push the form data to the 'Events' node in the database
        new_event_ref = ref.child('Events').push(form_data)

        return jsonify({'success': True, 'event_id': new_event_ref.key})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
