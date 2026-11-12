import requests

url = "https://geocoding-api.open-meteo.com/v1/search"

url2 = "https://api.open-meteo.com/v1/forecast"


def get_weather_status(city):
    try:
        parameters = {
            "name": city,
            "count": 1,
            "language": "fa"
        }

        response = requests.get(url, params=parameters,
                                timeout=10, proxies=None)

        print(response.text)
        print(response.status_code)

        response.raise_for_status()

        data = response.json()
        print(11111111111111111111111111)
        print(data)

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
                "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,apparent_temperature,weather_code,is_day",
                "timezone": "auto"
            }

            response2 = requests.get(
                url2, params=parameters2, timeout=10, proxies=None)

            print(response2.text)
            print(response2.status_code)

            response2.raise_for_status()

            data2 = response2.json()

            current_weather = data2["current"]
            weather_code = current_weather["weather_code"]

            if weather_code == 0:
                description = "آسمان صاف ☀️"
            elif weather_code == 1:
                description = "عمدتاً صاف 🌤️"
            elif weather_code == 2:
                description = "نیمه ابری ⛅"
            elif weather_code == 3:
                description = "ابری ☁️"
            elif weather_code in [45, 48]:
                description = "مه آلود 🌫️"
            elif weather_code in [61, 63, 65]:
                description = "بارانی 🌧️"
            elif weather_code in [71, 73, 75]:
                description = "برفی ❄️"
            elif weather_code == 95:
                description = "رعد و برق ⛈️"
            else:
                description = "❌وضعیت نامشخص"

            is_day = current_weather["is_day"]

            if is_day == 0:
                day_or_night = "شب🌙"
            elif is_day == 1:
                day_or_night = "روز☀️"

            weather_status = f"""
            📰 وضعیت آب و هوای امروز: 
            
                {description}  |  {day_or_night}
                
            🌡️ دما: {current_weather["temperature_2m"]}°C
            💧 رطوبت هوا: {current_weather["relative_humidity_2m"]}%
            💨 سرعت باد: {current_weather["wind_speed_10m"]}Km/h
            """

            return weather_status

    except requests.exceptions.RequestException as error:
        print("Request failed:", error)
