import requests
import os
import json


class GeminiService:

    @staticmethod
    def generate_forecast(harvest_data, weather_data):

        prompt = f"""
You are an aquaculture AI assistant.

Analyze the following bangus harvest data and weather forecast
then generate a short forecast about the next harvest cycle.

Harvest Data:
2-1 pieces: {harvest_data['twoInOneTotalPieces']}
3-1 pieces: {harvest_data['threeInOneTotalPieces']}
4-1 pieces: {harvest_data['fourInOneTotalPieces']}
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
2-1 pieces: 
3-1 pieces: 
4-1 pieces: 
Sardines: 
Total Pieces: 
Total Weight: 
",
 "confidence": 0.0

}}
"""

        ollama_url = os.getenv("OLLAMA_URL", "https://ollama.com")
        model = "gemini-3-flash-preview:cloud"  

        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False
        }

        try:
            response = requests.post(f"{ollama_url}/api/generate", json=payload, timeout=30)
            response.raise_for_status()
            result = response.json()
            raw_text = result.get("response", "")

            # Try to parse JSON from response
            try:
                parsed = json.loads(raw_text)
                if isinstance(parsed, dict):
                    parsed["rawText"] = raw_text
                    return parsed
            except json.JSONDecodeError:
                pass

            return {"rawText": raw_text}

        except requests.RequestException as e:
            print(f"Ollama API error: {e}")
            return {"rawText": f"Error generating forecast: {str(e)}"}