import firebase_admin
from firebase_admin import credentials, auth

cred = credentials.Certificate("totepai-edd0f-firebase-adminsdk-fbsvc-925bdc3e10.json")

firebase_admin.initialize_app(cred)


class FirebaseAuthService:

    @staticmethod
    def verify_token(token: str):

        try:
            decoded_token = auth.verify_id_token(token)
            return decoded_token

        except Exception:
            return None