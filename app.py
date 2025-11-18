import sys
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QComboBox, QLineEdit, QPushButton
from PySide6.QtGui import QPixmap
from __feature__ import snake_case, true_property
import requests

app = QApplication([])
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        vbox = QVBoxLayout()
        self.titlelabel = QLabel('QWeather')
        self.search_box = QLineEdit()
        self.button = QPushButton("Search Zip Code")
        self.button.clicked.connect(self.find)
        self.label = QLabel() # make a qlabel to turn into city name/weather info later
        vbox.add_widget(self.search_box)
        vbox.add_widget(self.button)
        vbox.add_widget(self.titlelabel)
        vbox.add_widget(self.label)
        self.set_layout(vbox)
        self.show()
    def find(self):
        zip = self.search_box.text
        apiurl = 'https://geocoding-api.open-meteo.com/v1/search'
        zipfind = requests.get(apiurl, zip, "US")
        locationdata = zipfind.json()
        lat = locationdata["results"][0]["latitude"]
        long = locationdata["results"][0]["longitude"]
        weatherapi = "https://api.open-meteo.com/v1/forecast"

