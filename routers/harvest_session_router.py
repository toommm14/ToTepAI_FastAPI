from fastapi import APIRouter, Depends
from core.auth import get_current_uid
from core.firebase_init import db
from datetime import datetime

router = APIRouter()

@router.post("/start-harvest-session")
def start_harvest_session(uid: str = Depends(get_current_uid)):
    db.collection("users").document(uid).set(
        {"status": 1, "started_at": datetime.utcnow()},
        merge=True
    )

    return {
        "status": "harvest_session_started",
        "user_id": uid
    }

@router.post("/end-harvest-session")
def end_harvest_session(uid: str = Depends(get_current_uid)):
    db.collection("users").document(uid).set(
        {"status": 0, "ended_at": datetime.utcnow()},
        merge=True
    )

    return {
        "status": "harvest_session_ended",
        "user_id": uid
    }
