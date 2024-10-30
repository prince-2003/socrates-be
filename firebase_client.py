from firebase_admin import credentials, firestore, initialize_app

# Initialize Firebase Admin SDK
cred = credentials.Certificate('./socratic.json')  # Correct path to your service account key
initialize_app(cred)

# Initialize Firestore
db = firestore.client()

# Export the Firestore client
__all__ = ['db']