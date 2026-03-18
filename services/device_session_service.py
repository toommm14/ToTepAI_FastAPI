from core.firebase_init import db
from datetime import datetime


class DeviceSessionService:

    @staticmethod
    def start_session(device_id: str, owner_uid: str):

        session_data = {
            "owner_uid": owner_uid,
            "started_at": datetime.utcnow()
        }

        db.collection("device_sessions").document(device_id).set(session_data)

        return session_data


    @staticmethod
    def end_session(device_id: str):

        db.collection("device_sessions").document(device_id).delete()


    @staticmethod
    def get_active_owner(device_id: str):

        doc = db.collection("device_sessions").document(device_id).get()

        if doc.exists:
            return doc.to_dict()["owner_uid"]

        return None