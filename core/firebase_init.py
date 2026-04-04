import os
import json
import firebase_admin
from firebase_admin import credentials, firestore

# Load credentials from ENV
firebase_creds = json.loads(os.getenv("FIREBASE_CREDENTIALS"))

cred = credentials.Certificate(firebase_creds)

# Initialize app (only once)
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)
  
db = firestore.client()
