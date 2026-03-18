from fastapi import APIRouter
from schemas.harvest_session_schema import HarvestSession
from services.harvest_service import HarvestService

router = APIRouter()


@router.post("/upload-harvest")
def upload_harvest(data: HarvestSession):

    result = HarvestService.store_session(data)

    return {
        "status": "success",
        "message": "Harvest stored successfully",
        "data": result
    }