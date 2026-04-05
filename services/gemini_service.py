import requests
import os
import json
import time
import logging


class GeminiService:

    @staticmethod
    def generate_forecast(harvest_data):

        prompt = (
            "You are an aquaculture AI assistant.\n\n"
            "Analyze the following bangus harvest data\n"
            "then generate a short forecast about the next harvest cycle.\n\n"
            "Harvest Data:\n"
            "2-1 pieces: " + str(harvest_data['twoInOneTotalPieces']) + "\n"
            "3-1 pieces: " + str(harvest_data['threeInOneTotalPieces']) + "\n"
            "4-1 pieces: " + str(harvest_data['fourInOneTotalPieces']) + "\n"
            "Sardines: " + str(harvest_data['sardinesTotalPieces']) + "\n"
            "Total Pieces: " + str(harvest_data['totalPiecesOfHarvest']) + "\n"
            "Total Weight: " + str(harvest_data['totalWeightOfHarvest']) + "\n\n"
            "Provide a short harvest prediction and recommendation.\n"
            "Also provide a weather advisory based on upcoming months weather conditions in the Philippines Surigao Del Sur to help farmers prepare for the next harvest cycle.\n"
            "Respond in JSON format:\n\n"
            "{\n"
            ' "forecastRemark": "...",\n'
            ' "weatherAdvisory": "...",\n'
            ' "predictedHarvestData": "Harvest Data:\\n'
            '2-1 pieces: \\n'
            '3-1 pieces: \\n'
            '4-1 pieces: \\n'
            'Sardines: \\n'
            'Total Pieces: \\n'
            'Total Weight: \\n'
            '",\n'
            ' "confidence": 0.0\n'
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
