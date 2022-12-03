import os
import requests
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

def getWeatherDetails(lat, lon):
    if lat == "TBD" or lon == "TBD":
        weather_details = {
            "temperature_f": "N/A",
            "temperature_min_f": "N/A",
            "temperature_max_f": "N/A",
            "temperature_c": "N/A",
            "temperature_min_c": "N/A",
            "temperature_max_c": "N/A",
            "weather_icon": "N/A",
            "weather_description": "N/A",
            "humidity": "N/A",
            "wind": "N/A",
        }

        return weather_details

    OPENWEATHERMAP_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")

    url = (
        "https://api.openweathermap.org/data/2.5/weather?lat="
        + lat
        + "&lon="
        + lon
        + "&appid="
        + OPENWEATHERMAP_API_KEY
    )

    openweathermap_request = requests.get(url=url)

    openweathermap_response_json = openweathermap_request.json()

    try:
        temperature_f = round((openweathermap_response_json["main"]["temp"] - 273.15) * 9 / 5 + 32, 2)
        temperature_c = round(openweathermap_response_json["main"]["temp"] - 273.15, 2)
    except KeyError as e:
        temperature_f = "N/A"
        temperature_c = "N/A"

    try:
        temperature_min_f = round((openweathermap_response_json["main"]["temp_min"] - 273.15) * 9 / 5 + 32, 2)
        temperature_min_c = round(openweathermap_response_json["main"]["temp_min"] - 273.15, 2)
    except KeyError as e:
        temperature_min_f = "N/A"
        temperature_min_c = "N/A"

    try:
        temperature_max_f = round((openweathermap_response_json["main"]["temp_max"] - 273.15) * 9 / 5 + 32, 2)
        temperature_max_c = round(openweathermap_response_json["main"]["temp_max"] - 273.15, 2)
    except KeyError as e:
        temperature_max_f = "N/A"
        temperature_max_c = "N/A"

    try:
        weather_icon = openweathermap_response_json["weather"][0]["icon"]
    except KeyError as e:
        weather_icon = "N/A"

    try:
        weather_description = openweathermap_response_json["weather"][0]["description"]
    except KeyError as e:
        weather_description = "N/A"

    try:
        humidity = openweathermap_response_json["main"]["humidity"]
    except KeyError as e:
        humidity = "N/A"

    try:
        wind = openweathermap_response_json["wind"]["speed"]
    except KeyError as e:
        wind = "N/A"

    weather_details = {
        "temperature_f": temperature_f,
        "temperature_min_f": temperature_min_f,
        "temperature_max_f": temperature_max_f,
        "temperature_c": temperature_c,
        "temperature_min_c": temperature_min_c,
        "temperature_max_c": temperature_max_c,
        "weather_icon": weather_icon,
        "weather_description": weather_description,
        "humidity": humidity,
        "wind": wind
    }

    return weather_details