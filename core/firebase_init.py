import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("totepai-edd0f-firebase-adminsdk-fbsvc-925bdc3e10.json")

firebase_admin.initialize_app(cred)

db = firestore.client()