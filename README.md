# Weather App Project - Team 12475 CST 205

## Overview  
Our final project is a desktop weather application built with Python + PySide6 (Qt) that lets users view current weather and forecast information. The QtApplication can take in a location (via zip code or city/city, state) to get real time weather information for that location, including the temperature, percepitation information, etc. There is also an interactive map which users can click on a location and receive that location's weather information. ⛅

## Resources leveraged:
- PySide6 (Qt) for the GUI  
- Folium for an interactive map
- OpenStreetMap to get location information
- Open-Meteo API for weather data  
- Custom made images, icons, and other interactive features for a clean experience

## Features  
- Fetch current weather conditions (temperature, humidity, wind, etc.) for a given location
- Display interactive map to show location/weather using Folium  
- GUI using PySide6 (Qt)
- Custom styling and UI themes  
- Clean file separation between API logic, UI, and data handling

## How To Install
- Make sure you have Python 3.9+ installed on your system.  
- Clone the repository and create a virtual environment:  
git clone https://github.com/hoostinn/CST205_Project.git  
cd CST205_Project  
python -m venv venv  
- Activate your virtual environment:  
*Windows:*  
venv\Scripts\activate  
*macOS:*  
source venv/bin/activate  
- Install project libraries  
pip install -r requirements.txt  
- Now that you have set up the venv and installed dependencies, you can run the main.py file  
python main.py  

## Future Features
- Adding a feature to save locations locally
- Implement Fahrenheit and Celsius option as well as implementing a formula to calculate
- Add audio when things are clicked, closed, interacted with, etc.
