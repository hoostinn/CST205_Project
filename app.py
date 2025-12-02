import sys
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QComboBox, QLineEdit, QPushButton
from PySide6.QtGui import QPixmap
from __feature__ import snake_case, true_property
import requests
features = ["temperature_2m", "precipitation_probability", "precipitation", "rain", "showers", "snowfall", "snow_depth", "weather_code", "cloud_cover", "wind_speed_180m", "wind_direction_180m"]

app = QApplication([])
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        vbox = QVBoxLayout()
        self.titlelabel = QLabel('QWeather')
        self.search_box = QLineEdit()
        self.button = QPushButton("Search Zip Code")
        self.button.clicked.connect(self.find)
        self.label = QLabel("") # make a qlabel to turn into city name/weather info later
        vbox.add_widget(self.search_box)
        vbox.add_widget(self.button)
        vbox.add_widget(self.titlelabel)
        vbox.add_widget(self.label)
        self.set_layout(vbox)
        self.show()

    def get_location(self, zip_code: str):
        url = "https://geocoding-api.open-meteo.com/v1/search"
        params = {"name": zip_code, "count": 1, "language": "en", "format": "json"}
        r = requests.get(url, params=params)
        data = r.json()
        return data["results"][0]

    def get_data(self, type, locationdata):
        return locationdata[type]

    def find(self):
        zip = self.search_box.text()
        locationdata = self.get_location(zip)
        self.lat = locationdata["latitude"]
        self.long = locationdata["longitude"]
        self.name = locationdata["name"]
        hourly = locationdata["hourly"]
        self.time = hourly["time"]
        self.temperature_2m = hourly["temperature_2m"]
        self.precipitation_probability = hourly["precipitation_probability"]
        self.precipitation = hourly["precipitation"]
        self.rain = hourly["rain"]
        self.showers = hourly["showers"]
        self.snowfall = hourly["snowfall"]
        self.snow_depth = hourly["snow_depth"]
        self.weather_code = hourly["weather_code"]
        self.cloud_cover = hourly["cloud_cover"]
        self.wind_speed_180m = hourly["wind_speed_180m"]
        self.wind_direction_180m = hourly["wind_direction_180m"]
        self.label.set_text(f"{self.name}\nLat: {self.lat}\nLong: {self.long}\nRain: {self.precipitation_probability}")
window = MainWindow()
sys.exit(app.exec())
