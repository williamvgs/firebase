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

    # Get today's date in ISO format
    today = datetime.date.today().isoformat()

    # Loop through the events and delete those with dates older than today
    for event_id, event_data in events.items():
        event_date = event_data.get('dato') or event_data.get('eventDate')

        if event_date:
            # Convert event date to ISO format for proper comparison
            event_date_iso = datetime.datetime.strptime(event_date, '%Y-%m-%dT%H:%M:%S').isoformat()
            
            if event_date_iso < today:
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

        # Separate 'eventDate', 'startTime', and 'finishTime'
        event_date = form_data.get('eventDate')
        start_time = form_data.get('startTime')
        finish_time = form_data.get('finishTime')

        if event_date and start_time and finish_time:
            # Format 'start_time' and 'finish_time' fields
            form_data['start_time'] = f"{event_date} {start_time}"
            form_data['finish_time'] = f"{event_date} {finish_time}"
        else:
            return jsonify({'success': False, 'error': 'Invalid date or time fields'})

        # Remove unnecessary fields
        form_data.pop('eventDate', None)
        form_data.pop('startTime', None)
        form_data.pop('finishTime', None)

        # Push the form data to the 'Events' node in the database
        new_event_ref = ref.child('Events').push(form_data)

        return jsonify({'success': True, 'event_id': new_event_ref.key})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})





if __name__ == '__main__':
    app.run(debug=True)
