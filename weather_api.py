import requests
features = ["temperature_2m", "precipitation_probability", "precipitation", "rain", "showers", "snowfall", "snow_depth", "weather_code", "cloud_cover", "wind_speed_180m", "wind_direction_180m"]

def get_location(city_name: str):
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {"name": city_name, "count":1, "language": "en", "format": "json"}
    r = requests.get(url, params = params)
    data = r.json()
    return data["results"][0]
def get_weather(lat, long):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {"latitude" : lat, "longitude": long, "hourly": ",".join(features)}
    r = requests.get(url, params = params)
    return r.json()