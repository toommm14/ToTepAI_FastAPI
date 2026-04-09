import time
from core.firebase_init import db
from services.gemini_service import GeminiService
from google.cloud.firestore import FieldFilter


class HarvestService:


    @staticmethod
    def _resolve_owner_user_id(user_id: str | None):
        if user_id:
            return user_id

        try:
            start_time = time.time()
            active_users = list(db.collection("users").where(filter=FieldFilter("status", "==", 1)).limit(2).stream())
            elapsed = time.time() - start_time
            if elapsed > 5:
                print(f"Warning: Firestore active user query took {elapsed:.2f}s")
            
            if len(active_users) == 1:
                return active_users[0].id
            if len(active_users) > 1:
                return active_users[0].id
        except Exception as e:
            print(f"Error resolving active user: {e}")
            raise ValueError("Failed to resolve active user. Please try again.")

        raise ValueError("No active harvest session. Start harvest in the mobile app first.")


    @staticmethod
    def store_session(data):

        owner_user_id = HarvestService._resolve_owner_user_id(data.userId)

        harvest_record = {

            "userId": owner_user_id,

            "monthOfHarvest": data.timestamp.strftime("%B"),
            "yearOfHarvest": data.timestamp.year,

            "threeInOneTotalPieces": data.threeInOneTotalPieces,
            "fourInOneTotalPieces": data.fourInOneTotalPieces,
            "twoInOneTotalPieces": data.twoInOneTotalPieces,
            "sardinesTotalPieces": data.sardinesTotalPieces,

            "totalPiecesOfHarvest": data.totalPiecesOfHarvest,
            "totalWeightOfHarvest": data.totalWeightOfHarvest * 1000,

            "timestamp": data.timestamp,
        }

        # AI Forecast
        print("DEBUG: Generating AI forecast...")
        forecast = GeminiService.generate_forecast(harvest_record)
        print(f"DEBUG: Forecast result: {forecast}")

        if isinstance(forecast, dict):
            # Extract forecastRemark from rawText if available
            raw_text = forecast.get("rawText", "")
            if raw_text:
                try:
                    # Parse JSON from rawText (which contains the actual AI response)
                    import json
                    # Remove markdown code blocks if present
                    clean_text = raw_text.replace("```json", "").replace("```", "").strip()
                    parsed_forecast = json.loads(clean_text)
                    harvest_record["geminiForecastRemarks"] = parsed_forecast.get("forecastRemark")
                    harvest_record["weatherAdvisory"] = parsed_forecast.get("weatherAdvisory")
                    # Remove forecastRemark from the data to avoid duplication
                    forecast_data = {
                        k: v for k, v in parsed_forecast.items()
                        if k not in ["forecastRemark", "weatherAdvisory"]
                    }
                    harvest_record["geminiForecastedData"] = forecast_data
                except (json.JSONDecodeError, KeyError):
                    harvest_record["geminiForecastRemarks"] = raw_text
                    harvest_record["weatherAdvisory"] = raw_text
                    
                    forecast_copy = {
                        k: v for k, v in forecast.items()
                        if k != "weatherAdvisory"
                    }

                    harvest_record["geminiForecastedData"] = forecast_copy
            else:
                harvest_record["geminiForecastRemarks"] = forecast.get("forecastRemark")
                harvest_record["weatherAdvisory"] = forecast.get("weatherAdvisory")
                harvest_record["geminiForecastedData"] = forecast
        else:
            harvest_record["geminiForecastRemarks"] = None
            harvest_record["weatherAdvisory"] = None
            harvest_record["geminiForecastedData"] = {"rawText": str(forecast)}

        db.collection("users")\
          .document(owner_user_id)\
          .collection("harvest_data")\
          .add(harvest_record)

        return harvest_record
