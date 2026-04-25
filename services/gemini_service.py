import requests
import os
import json
import time
import logging
from core.firebase_init import db
from google.cloud.firestore import FieldFilter


class GeminiService:

    @staticmethod
    def get_historical_harvest_data(user_id):
        harvest_data_ref = db.collection('users').document(user_id).collection('harvest_data').order_by('timestamp', direction='DESCENDING').limit(5)
        harvest_data_docs = harvest_data_ref.stream()
        historical_harvest_data = []
        for doc in harvest_data_docs:
            historical_harvest_data.append(doc.to_dict())
        return historical_harvest_data

    @staticmethod
    def get_active_user_id():
        active_users = list(db.collection("users").where(filter=FieldFilter("status", "==", 1)).limit(2).stream())
        if len(active_users) == 1:
            return active_users[0].id
        if len(active_users) > 1:
            return active_users[0].id
        return None

    @staticmethod
    def generate_forecast(harvest_data):

        user_id = GeminiService.get_active_user_id()
        if not user_id:
            return {"rawText": "No active harvest session found. Please start harvest session first."}

        historical_harvest_data = GeminiService.get_historical_harvest_data(user_id)

        prompt = (
            "You are an expert data scientist specializing in aquaculture time-series forecasting and aquaculture yield analysis.\n\n"
            "Analyze the following bangus harvest data along with historical trends\n"
            "then generate a comprehensive forecast about the next harvest cycle.\n\n"
            "Current Harvest Data:\n"
            "2-1 pieces: " + str(harvest_data['twoInOneTotalPieces']) + "\n"
            "3-1 pieces: " + str(harvest_data['threeInOneTotalPieces']) + "\n"
            "4-1 pieces: " + str(harvest_data['fourInOneTotalPieces']) + "\n"
            "Sardines: " + str(harvest_data['sardinesTotalPieces']) + "\n"
            "Total Pieces: " + str(harvest_data['totalPiecesOfHarvest']) + "\n"
            "Total Weight: " + str(harvest_data['totalWeightOfHarvest']) + " " + str(harvest_data.get('weightUnit', 'kg')) + "\n\n"
            "Historical Harvest Data (last 5 harvests):\n"
        )
        
        # Add historical data to prompt
        for i, hist_data in enumerate(historical_harvest_data, 1):
            prompt += (
                f"Harvest {i}:\n"
                f"2-1 pieces: {hist_data.get('twoInOneTotalPieces', 'N/A')}\n"
                f"3-1 pieces: {hist_data.get('threeInOneTotalPieces', 'N/A')}\n"
                f"4-1 pieces: {hist_data.get('fourInOneTotalPieces', 'N/A')}\n"
                f"Sardines: {hist_data.get('sardinesTotalPieces', 'N/A')}\n"
                f"Total Pieces: {hist_data.get('totalPiecesOfHarvest', 'N/A')}\n"
                f"Total Weight: {hist_data.get('totalWeightOfHarvest', 'N/A')} {hist_data.get('weightUnit', 'kg')}\n\n"
            )
        
        prompt += (
            "Analyze the historical and current harvest data patterns and select the most appropriate forecasting model (e.g., SARIMA, Holt-Winters, Prophet, Exponential Smoothing, Linear Regression, Seasonal Decomposition) based on the data characteristics.\n\n"
            "Provide a comprehensive harvest prediction and recommendation for the harvest.\n"
           
            "Respond in JSON format:\n\n"
            "{\n"
            ' "forecastingModel": "Selected forecasting model name",\n'
            ' "modelRationale": "Why this model was chosen",\n'
            ' "forecastRemark": "...",\n'
            ' "predictedHarvestData": "Forecasted Harvest Data for next harvest:\\n'
            '2-1 pieces: \\n'
            '3-1 pieces: \\n'
            '4-1 pieces: \\n'
            'Sardines: \\n'
            'Total Pieces: \\n'
            'Total Weight: \\n'
            '",\n'
            ' "MAPE": (in percentage)%,\n'
            "}\n"
        )

        ollama_url = os.getenv("OLLAMA_URL", "https://ollama.com")
        model = os.getenv("OLLAMA_MODEL", "gemini-3-flash-preview:cloud")

        api_key = os.getenv("OLLAMA_API_KEY", "")
        headers = {}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False
        }

        try:
            start_time = time.time()
            response = requests.post(
                f"{ollama_url}/api/generate",
                json=payload,
                headers=headers,
                timeout=60
            )
            elapsed = time.time() - start_time
            if elapsed > 8:
                logging.warning(f"Ollama API took {elapsed:.2f}s")
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
            if hasattr(e, "response") and e.response is not None:
                try:
                    return {"rawText": f"Error generating forecast: {e.response.status_code} {e.response.text}"}
                except Exception:
                    pass
            return {"rawText": f"Error generating forecast: {str(e)}"}
