from core.firebase_init import db
from services.weather_service import WeatherService
from services.gemini_service import GeminiService


class HarvestService:


    @staticmethod
    def _resolve_owner_user_id(user_id: str | None):
        if user_id:
            return user_id

        active_users = list(db.collection("users").where("status", "==", 1).limit(2).stream())
        if len(active_users) == 1:
            return active_users[0].id
        if len(active_users) > 1:
            return active_users[0].id

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
            "totalWeightOfHarvest": data.totalWeightOfHarvest,

            "timestamp": data.timestamp,
        }

        # Get Weather
        weather = WeatherService.get_weather()

        # AI Forecast
        forecast = GeminiService.generate_forecast(
            harvest_record, 
            weather
        )

        if isinstance(forecast, dict):
            harvest_record["geminiForecastRemarks"] = forecast.get("forecastRemark")
            harvest_record["geminiForecastedData"] = forecast
        else:
            harvest_record["geminiForecastRemarks"] = None
            harvest_record["geminiForecastedData"] = {"rawText": str(forecast)}

        db.collection("users")\
          .document(owner_user_id)\
          .collection("harvest_data")\
          .add(harvest_record)

        return harvest_record