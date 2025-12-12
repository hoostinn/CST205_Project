import requests
features = ["temperature_2m,precipitation_probability,precipitation,rain,showers,snowfall,snow_depth,weather_code,cloud_cover,wind_speed_180m,wind_direction_180m"]

def get_location(search_text: str):
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": search_text, "format": "json", "limit": 1, "countrycodes": "us"}
    headers = {"User-Agent": "weather-app"} # nominatim requires a user-agent, got http request error otherwise
    r = requests.get(url, params=params, headers=headers)
    data = r.json()
    return {"latitude": float(data[0]["lat"]), "longitude": float(data[0]["lon"]), "name": data[0]["display_name"]} # find latitude and longitude from openstreetmap based on entered city/zip
def get_weather(lat, long):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {"latitude" : lat, "longitude": long, "hourly": features} # use openmeteo to get weather details from the latitude/longitude
    r = requests.get(url, params = params)
    return r.json()
def coord_location(lat, long):
    url = "https://nominatim.openstreetmap.org/reverse"
    params = {"lat": lat, "lon": long, "format": "json", "addressdetails": 1} # use the lat and long from the map coordinates to get details of that address
    headers = {"User-Agent": "weather-app"}
    r = requests.get(url, params=params, headers=headers)
    data = r.json()
    addy = data["address"]
    city = addy.get("city") # parse the json address to get the city name
    state = addy.get("state") # get state name
    return f"{city}, {state}" # return a string to display City, State
