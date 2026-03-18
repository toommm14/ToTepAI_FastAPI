from fastapi import APIRouter
from schemas.harvest_session_schema import StartSession
from services.device_session_service import DeviceSessionService

router = APIRouter()


@router.post("/start-session")
def start_session(data: StartSession):

    result = DeviceSessionService.start_session(
        data.device_id,
        data.owner_uid
    )

    return {
        "status": "session_started",
        "data": result
    }


@router.post("/end-session/{device_id}")
def end_session(device_id: str):

    DeviceSessionService.end_session(device_id)

    return {
        "status": "session_ended",
        "device": device_id
    }