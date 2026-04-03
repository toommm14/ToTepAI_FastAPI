from fastapi import APIRouter, UploadFile, File, HTTPException
from schemas.harvest_session_schema import HarvestSession
from services.harvest_service import HarvestService
from pydantic import ValidationError
import json

router = APIRouter()


@router.post("/upload-harvest")
def upload_harvest(data: HarvestSession):

    try:
        result = HarvestService.store_session(data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {
        "status": "success",
        "message": "Harvest stored successfully",
        "data": result
    }


@router.post("/upload-harvest-file")
def upload_harvest_file(file: UploadFile = File(...)):
    if not file.filename.endswith('.json'):
        raise HTTPException(status_code=400, detail="File must be a JSON file")

    try:
        content = file.file.read().decode('utf-8')
        json_data = json.loads(content)
        harvest_data = HarvestSession(**json_data)
        try:
            result = HarvestService.store_session(harvest_data)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

        return {
            "status": "success",
            "message": "Harvest file uploaded and stored successfully",
            "data": result
        }
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format")
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=f"Validation error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    finally:
        file.file.close()