import os
import json
from firebase_admin import credentials, initialize_app

firebase_creds = json.loads(os.getenv("FIREBASE_CREDENTIALS"))

cred = credentials.Certificate(firebase_creds)
initialize_app(cred)
