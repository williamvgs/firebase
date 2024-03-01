var admin = require('firebase-admin');

// Initialize Firebase Admin SDK with service account key and your Firebase project URL
var serviceAccount = require('./credentials.json'); // Path to your service account key JSON file
admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
  databaseURL: 'https://test-e3dc4-default-rtdb.europe-west1.firebasedatabase.app/'
});

// Get a reference to your Firebase Realtime Database
const db = admin.database();
const ref = db.ref('/');

// Define the Event data
const Event = [
  { "Event": "Jazz konsert", "dato": "20-10-2025", "Addres": "Molde", "info": "Molde vs Ålesund" },
  { "Event": "Quiz", "dato": "20-10-2025", "Addres": "Molde", "info": "Molde vs Ålesund" },
  { "Event": "Football kamp", "dato": "20-10-2025", "Addres": "Molde", "info": "Molde vs Ålesund"},
];

// Push each Event to the database
Event.forEach(event => {
  ref.child('Event').push(event);
});

console.log("Event added to the database.");

// Retrieve and display events from the database
ref.child('Event').once('value', (snapshot) => {
  const events = snapshot.val();
  console.log("Retrieved Events:", events);
});
