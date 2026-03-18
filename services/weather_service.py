import requests


class WeatherService:

    @staticmethod
    def get_weather():

        url = "https://api.openweathermap.org/data/2.5/weather"

        params = {
            "q": "Surigao,PH",
            "appid": "YOUR_WEATHER_API_KEY",
            "units": "metric"
        }

        response = requests.get(url, params=params)

        data = response.json()

        return {

            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "rain": data.get("rain", {}).get("1h", 0)
        }