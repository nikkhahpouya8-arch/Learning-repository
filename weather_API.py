import requests

url = "https://geocoding-api.open-meteo.com/v1/search"

url2 = "https://api.open-meteo.com/v1/forecast"


def get_weather_status(city):
    try:
        parameters = {
            "name": city,
            "count": 1
        }
        
        
        response = requests.get(url, params=parameters, timeout=10)

        response.raise_for_status()

        data = response.json()

        if "results" not in data or not data["results"]:
            return False
        else:
            print(data["results"][0]["latitude"])
            print(data["results"][0]["longitude"])

            latitude = data["results"][0]["latitude"]
            longitude = data["results"][0]["longitude"]

            parameters2 = {
                "latitude": latitude,
                "longitude": longitude,
                "cuurent": "temperature_2m,relative_humidity_2m,wind_speed_10m",
                "timezone": "auto"
            }
            
            response2 = requests.get(url2, params=parameters2, timeout=10)
            
            response2.raise_for_status()
            
            data2 = response2.json()
            
            current_weather = data2["current"]
            
            weather_status = f"""
                        🌡️ Temperature: {current_weather["temperature_2m"]}°C
                        💧 Humidity: {current_weather["relative_humidity_2m"]}%
                        💨 Wind Speed: {current_weather["wind_speed_10m"]}Km/h
            """
            
            return weather_status

    except requests.exceptions.RequestException as error:
        print("Request failed:", error)
