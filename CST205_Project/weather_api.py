import requests
features = ["temperature_2m", "precipitation_probability", "precipitation", "rain", "showers", "snowfall", "snow_depth", "weather_code", "cloud_cover", "wind_speed_180m", "wind_direction_180m"]

def get_location(search_text: str):
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": search_text, "format": "json", "limit": 1, "countrycodes": "us"}
    headers = {"User-Agent": "weather-app"}
    r = requests.get(url, params=params, headers=headers)
    data = r.json()
    if not data:
        return None
    return {"latitude": float(data[0]["lat"]), "longitude": float(data[0]["lon"]), "name": data[0]["display_name"]}
def get_weather(lat, long):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {"latitude" : lat, "longitude": long, "hourly": ",".join(features)}
    r = requests.get(url, params = params)
    return r.json()