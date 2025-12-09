from PySide6.QtWidgets import (
    QApplication, QWidget, QHBoxLayout, QVBoxLayout,
    QLineEdit, QPushButton, QLabel, QFrame
)
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QFont
import sys
from weather_api import get_location, get_weather

try:
    from PySide6.QtWebEngineWidgets import QWebEngineView
except:
    QWebEngineView = None


class WeatherAppGUI(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Weather App")
        self.setMinimumSize(1200, 700)

        self.apply_styles()

        # MAIN LAYOUT
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # LEFT INFO PANEL
        self.info_panel = QFrame()
        self.info_panel.setMinimumWidth(300)
        self.info_panel.setObjectName("infoPanel")

        info_layout = QVBoxLayout(self.info_panel)
        info_layout.setAlignment(Qt.AlignTop)

        self.info_title = QLabel("Weather Info")
        self.info_title.setFont(QFont("Arial", 22))
        self.info_title.setStyleSheet("color: black;")
        info_layout.addWidget(self.info_title)

        self.weather_label = QLabel("Search a city to display the weather!")
        self.weather_label.setFont(QFont("Arial", 20))
        self.weather_label.setStyleSheet("color: black;")

        # make the text wrap and have enough vertical space
        self.weather_label.setWordWrap(True)
        self.weather_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.weather_label.setMinimumHeight(260)   # adjust number if you want more/less space

        info_layout.addWidget(self.weather_label)


        # RIGHT SIDE (SEARCH + MAP)
        right_side = QVBoxLayout()
        right_side.setSpacing(20)

        # Search Bar
        top_bar = QHBoxLayout()
        top_bar.setSpacing(10)

        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search city or zip code...")
        self.search_box.setObjectName("searchBox")
        self.search_box.setStyleSheet("color: black;")
        self.search_box.setFixedHeight(45)

        search_btn = QPushButton("🔍")
        search_btn.setObjectName("searchBtn")
        search_btn.setFixedSize(45, 45)
        search_btn.clicked.connect(self.find_weather)

        menu_btn = QPushButton("☰")
        menu_btn.setObjectName("menuBtn")
        menu_btn.setFixedSize(45, 45)
        menu_btn.clicked.connect(self.toggle_side_menu)

        top_bar.addWidget(self.search_box, 1)
        top_bar.addWidget(search_btn)
        top_bar.addWidget(menu_btn)

        # Map Panel
        self.map_frame = QFrame()
        self.map_frame.setObjectName("mapFrame")

        map_layout = QVBoxLayout(self.map_frame)

        self.map_placeholder = QLabel("Map will appear here")
        self.map_placeholder.setAlignment(Qt.AlignCenter)
        self.map_placeholder.setFont(QFont("Arial", 30))
        self.map_placeholder.setStyleSheet("color: gray;")

        map_layout.addWidget(self.map_placeholder)

        right_side.addLayout(top_bar)
        right_side.addWidget(self.map_frame)

        # ====== SIDE MENU ======
        self.side_menu = QFrame()
        self.side_menu.setObjectName("sideMenu")
        self.side_menu.setMinimumWidth(220)

        side_layout = QVBoxLayout(self.side_menu)
        side_layout.setAlignment(Qt.AlignTop)
        side_layout.setSpacing(8)

        side_title = QLabel("Saved Locations")
        side_title.setFont(QFont("Arial", 18))
        side_layout.addWidget(side_title)

        # Preset locations – all use REAL API data
        self.saved_locations = [
            "San Jose, CA",
            "Los Angeles, CA",
            "Phoenix, AZ",
            "Seattle, WA",
            "New York, NY"
        ]

        for city in self.saved_locations:
            btn = self._create_location_button(city)
            side_layout.addWidget(btn)

        side_layout.addStretch(1)

        # Add panels (left, main right, side menu)
        main_layout.addWidget(self.info_panel)
        main_layout.addLayout(right_side)
        main_layout.addWidget(self.side_menu)

        self.side_menu.hide()

    def apply_styles(self):
        self.setStyleSheet(open("styles.qss", "r").read())

    def set_map_widget(self, widget):
        layout = self.map_frame.layout()
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        layout.addWidget(widget)

    # ========= WEATHER SEARCH =========
    def find_weather(self):
        city = self.search_box.text()
        if not city:
            return

        location = get_location(city)
        if location is None:
            self.weather_label.setText("City not found.")
            return

        lat = location["latitude"]
        long = location["longitude"]
        name = location["name"]

        weather = get_weather(lat, long)
        hourly = weather["hourly"]

        temp = hourly["temperature_2m"][0]
        rain_prob = hourly["precipitation_probability"][0]
        wind = hourly["wind_speed_180m"][0]
        cloud = hourly["cloud_cover"][0]

        weatherinfo = (
            f"{name}\n"
            f"Temp: {temp} degrees\n"
            f"Rain Chance: {rain_prob}%\n"
            f"Wind Speed: {wind}\n"
            f"Cloud Cover: {cloud}%"
        )
        self.weather_label.setText(weatherinfo)

    def toggle_side_menu(self):
        """Show/hide the saved-locations side menu."""
        self.side_menu.setVisible(not self.side_menu.isVisible())

    def _create_location_button(self, city: str) -> QPushButton:
        """
        Create a side-menu button that shows:
            City, ST      73°
        using live temperature from the API when possible.
        """
        label_text = city

        try:
            location = get_location(city)
            if location is not None:
                lat = location["latitude"]
                long = location["longitude"]
                weather = get_weather(lat, long)
                temp = weather["hourly"]["temperature_2m"][0]
                label_text = f"{city}    {temp:.0f}°"
        except Exception:
            # On any error (no internet, API fail, etc.), fall back to city only
            label_text = city

        btn = QPushButton(label_text)
        btn.setObjectName("locationBtn")
        btn.setMinimumHeight(32)
        btn.clicked.connect(lambda checked=False, c=city: self.search_preset_location(c))
        return btn

    def search_preset_location(self, city: str):
        """
        Called when you click a saved location in the side menu.
        It fills the search box and reuses the normal weather search.
        """
        self.search_box.setText(city)
        self.find_weather()
