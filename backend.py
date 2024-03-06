import firebase_admin
from firebase_admin import credentials, db
import datetime
from flask import Flask, render_template, request, redirect, jsonify
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app, resources={r"/*": {"origins": "*"}})

# Initialize Firebase Admin SDK with service account key and your Firebase project URL
cred = credentials.Certificate("credentials.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://test-e3dc4-default-rtdb.europe-west1.firebasedatabase.app/'
})

# Get a reference to your Firebase Realtime Database
ref = db.reference('/')

def cleanup_database():
    # Get all items from the 'Events' node in the database
    events = ref.child('Events').get()

    # Get today's date
    today = datetime.date.today().isoformat()

    # Loop through the events and delete those with dates older than today
    for event_id, event_data in events.items():
        event_date = event_data.get('dato') or event_data.get('eventDate')

        if event_date and event_date < today:
            ref.child('Events').child(event_id).delete()

# Schedule the cleanup function to run periodically (for example, daily)


scheduler = BackgroundScheduler()
scheduler.add_job(cleanup_database, 'interval', days=1)
scheduler.start()

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/display')
def display_items():
    # Get all items from the 'Events' node in the database
    events = ref.child('Events').get()

    # Pass the events data to the HTML template for rendering
    return events

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
