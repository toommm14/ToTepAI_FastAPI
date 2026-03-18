import google.generativeai as genai
import os


genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-pro")


class GeminiService:

    @staticmethod
    def generate_forecast(harvest_data, weather_data):

        prompt = f"""
You are an aquaculture AI assistant.

Analyze the following bangus harvest data and weather forecast
then generate a short forecast about the next harvest cycle.

Harvest Data:
3-1 pieces: {harvest_data['threeInOneTotalPieces']}
4-1 pieces: {harvest_data['fourInOneTotalPieces']}
5-1 pieces: {harvest_data['fiveInOneTotalPieces']}
Sardines: {harvest_data['sardinesTotalPieces']}
Total Pieces: {harvest_data['totalPiecesOfHarvest']}
Total Weight: {harvest_data['totalWeightOfHarvest']}

Weather Forecast:
Temperature: {weather_data['temperature']}°C
Humidity: {weather_data['humidity']}%
Rainfall: {weather_data['rain']} mm

Provide a short harvest prediction and recommendation.
Respond in JSON format:

{{
 "forecastRemark": "...",
 "predictedHarvestData": "Harvest Data:
3-1 pieces: 
4-1 pieces: 
5-1 pieces: 
Sardines: 
Total Pieces: 
Total Weight: 
",
 "confidence": 0.0

}}
"""

        response = model.generate_content(prompt)

        return response.text