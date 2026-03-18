from core.firebase_init import db
from services.weather_service import WeatherService
from services.gemini_service import GeminiService


class HarvestService:

    @staticmethod
    def store_session(data):

        harvest_record = {

            "userId": data.userId,

            "threeInOneTotalPieces": data.threeInOneTotalPieces,
            "fourInOneTotalPieces": data.fourInOneTotalPieces,
            "fiveInOneTotalPieces": data.fiveInOneTotalPieces,
            "sardinesTotalPieces": data.sardinesTotalPieces,

            "totalPiecesOfHarvest": data.totalPiecesOfHarvest,
            "totalWeightOfHarvest": data.totalWeightOfHarvest,

            "timestamp": data.timestamp
        }

        # Get Weather
        weather = WeatherService.get_weather()

        # AI Forecast
        forecast = GeminiService.generate_forecast(
            harvest_record, 
            weather
        )

        harvest_record["geminiForecastRemarks"] = forecast.get("forecastRemark")
        harvest_record["geminiForecastedData"] = forecast

        db.collection("users")\
          .document(data.userId)\
          .collection("harvest_data")\
          .add(harvest_record)

        return harvest_record