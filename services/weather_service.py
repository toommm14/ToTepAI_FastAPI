import os
import requests


class WeatherService:


    @staticmethod
    def get_weather():

        url = "https://api.openweathermap.org/data/2.5/forecast"

        params = {
            "q": "Surigao,PH",
            "appid": os.getenv("OPENWEATHER_API_KEY", ""),
            "units": "metric"
        }

        try:
            response = requests.get(url, params=params, timeout=10)
            data = response.json()

            if not isinstance(data, dict) or "list" not in data:
                raise ValueError("Invalid forecast response")

            # Aggregate data from the next 5 days (40 entries, 3-hour intervals)
            forecasts = data["list"][:40]  # Limit to 5 days

            total_temp = 0
            total_humidity = 0
            total_rain = 0
            count = 0

            for forecast in forecasts:
                main = forecast.get("main", {})
                rain = forecast.get("rain", {}).get("3h", 0) or 0

                total_temp += main.get("temp", 0)
                total_humidity += main.get("humidity", 0)
                total_rain += rain
                count += 1

            if count == 0:
                raise ValueError("No forecast data")

            return {
                "temperature": round(total_temp / count, 1),  # Average temp
                "humidity": round(total_humidity / count, 1),  # Average humidity
                "rain": round(total_rain, 1)  # Total rain over 5 days
            }
        except Exception:
            pass

        return {
            "temperature": 0,
            "humidity": 0,
            "rain": 0
        }