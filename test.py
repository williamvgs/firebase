import firebase_admin
from firebase_admin import credentials, db

# Initialize Firebase Admin SDK with service account key and your Firebase project URL
cred = credentials.Certificate("credentials.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://test-e3dc4-default-rtdb.europe-west1.firebasedatabase.app/'
})

# Get a reference to your Firebase Realtime Database
ref = db.reference('/')

# Define the person data
persons = [
    {"name": "John", "age": 30},
    {"name": "Alice", "age": 25},
    {"name": "Bob", "age": 35}
]

# Push each person to the database
for person in persons:
    ref.child('persons').push(person)

print("Persons added to the database.")
