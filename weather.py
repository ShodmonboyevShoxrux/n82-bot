from datetime import datetime
import requests

from environs import Env

from constants import CITIES

env = Env()
env.read_env()

API_TOKEN = env.str("WEATHER_TOKEN")


def get_weather_data(city_name: str) -> str:
    # OpenWeather API xizmatiga so'rov yuborish
    response = requests.get(url=f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_TOKEN}&units=metric")

    # Status kodni tekshirish
    if response.status_code == 200:
        weather_data = response.json()  # { ... }
        flag = CITIES.get(weather_data.get("sys").get("country"))

        sunrise_seconds = weather_data.get("sys").get("sunrise")
        sunset_seconds = weather_data.get("sys").get("sunset")

        sunrise = datetime.fromtimestamp(timestamp=sunrise_seconds).strftime("%H:%M:%S")
        sunset = datetime.fromtimestamp(timestamp=sunset_seconds).strftime("%H:%M:%S")

        result = f"""
🌆 Bugun {flag if flag else ' '}{city_name} da

🌤️ Harorat: {weather_data.get('main').get('temp')} C
🌤️ Minimal harorat: {weather_data.get('main').get('temp_min')} C
🌤️ Maksimal harorat: {weather_data.get('main').get('temp_max')} C

䷮ Bosim: {weather_data.get('main').get('pressure')} Pa
💧 Namlik: {weather_data.get('main').get('humidity')} %

🌅 Quyosh chiqish vaqti: {sunrise} da
🌆 Quyosh botish vaqti: {sunset} da
"""
        return result, True

    else:
        return f"\"{city_name}\" bo'yicha shahar topilmadi", False
