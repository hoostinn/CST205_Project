from PySide6.QtWidgets import (
    QApplication, QWidget, QHBoxLayout, QVBoxLayout,
    QLineEdit, QPushButton, QLabel, QFrame, QGridLayout
)
from PySide6.QtCore import Qt, QUrl, Signal, Slot, QEvent
from PySide6.QtGui import QFont, QPixmap
import sys
from weather_api import get_location, get_weather, coord_location

try:
    from PySide6.QtWebEngineWidgets import QWebEngineView
except:
    QWebEngineView = None


class WeatherAppGUI(QWidget):

    # Getting signal from map_integration.py
    coordinates_received_signal = Signal(float, float)

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Weather App")
        self.setMinimumSize(1200, 700)

        self.apply_styles()

        # MAIN LAYOUT
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # Send lat and long to the method
        self.coordinates_received_signal.connect(self.weather_from_map)

        # LEFT INFO PANEL
        self.info_panel = QFrame()
        self.info_panel.setFixedWidth(300)
        self.info_panel.setObjectName("infoPanel")

        #Default BG for left panel
        self.info_bg = QLabel(self.info_panel)
        self.info_bg.setPixmap(QPixmap("Images/BACKGROUNDS/loading.png"))
        self.info_bg.setScaledContents(True)
        self.info_bg.lower()

        info_layout = QVBoxLayout(self.info_panel)
        info_layout.setAlignment(Qt.AlignTop)

        self.info_title = QLabel("Weather Information")
        self.info_title.setFont(QFont("Arial", 22))
        self.info_title.setStyleSheet("color: black;")
        info_layout.addWidget(self.info_title)

        # Icon 
        self.icon_label = QLabel()
        self.icon_label.setFixedSize(96, 96)
        self.icon_label.setAlignment(Qt.AlignCenter)
        info_layout.addWidget(self.icon_label, alignment=Qt.AlignHCenter)
        self.icon_label.setScaledContents(True)
        self.icon_label.setPixmap(QPixmap("Images/ICONS/Loading.png").scaled(96,96, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        info_layout.addSpacing(40)


        # Location line
        self.location_label = QLabel("No location selected")
        self.location_label.setFont(QFont("Arial", 18))
        self.location_label.setStyleSheet("color: black;")
        self.location_label.setWordWrap(True)
        info_layout.addWidget(self.location_label)

        # Stats grid (2x2)
        stats_widget = QFrame()
        stats_layout = QGridLayout(stats_widget)
        stats_layout.setSpacing(8)

        self.temp_label = QLabel("Temp: --")
        self.rain_label = QLabel("Rain Chance: --")
        self.wind_label = QLabel("Wind: --")
        self.cloud_label = QLabel("Cloud Cover: --")

        for lbl in (self.temp_label, self.rain_label, self.wind_label, self.cloud_label):
            lbl.setFont(QFont("Arial", 16))
            lbl.setStyleSheet("color: black;")

        stats_layout.addWidget(self.temp_label, 0, 0)
        stats_layout.addWidget(self.rain_label, 0, 1)
        stats_layout.addWidget(self.wind_label, 1, 0)
        stats_layout.addWidget(self.cloud_label, 1, 1)

        info_layout.addWidget(stats_widget)

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

        #  Map Panel 
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

        self.side_menu = QFrame()
        self.side_menu.setFixedWidth(220)
        self.side_menu.setObjectName("sideMenu")
        self.side_menu.setStyleSheet("background-color: #333333; border-radius: 20px;")

        side_layout = QVBoxLayout(self.side_menu)
        side_layout.setContentsMargins(15, 15, 15, 15)
        side_layout.setSpacing(10)

        side_title = QLabel("Saved Locations")
        side_title.setStyleSheet("color: white; font-size: 20px; font-wieight: bold;")
        side_layout.addWidget(side_title)

        preset_cities = [
            "San Jose, CA",
            "Los Angeles, CA",
            "Phoenix, AZ",
            "Seattle, WA",
            "New York, NY",
        ]
        for city in preset_cities:
            btn = QPushButton(city)
            btn.setObjectName("presetBtn")
            btn.setFixedHeight(40)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet(
                "background-color: #555555;"
                "border-radius: 18px;"
                "padding-left: 14px;"
                "padding-right: 10px;"
                "text-align: left;"
                "color: white;"
                "font-size: 14px;"
            )
            btn.clicked.connect(self.make_city_button(city))
            side_layout.addWidget(btn)
            side_layout.addSpacing(8)

        side_layout.addStretch()

        self.side_menu.hide()

        # Add panels
        main_layout.addWidget(self.info_panel)
        main_layout.addLayout(right_side)
        main_layout.addWidget(self.side_menu)

        #Locked window so it doesn't resize
        self.setFixedSize(self.size())

        # Make background cover the entire info_panel and keeps it updated
        self.info_bg.setGeometry(self.info_panel.rect())
        self.info_panel.installEventFilter(self)

    def toggle_side_menu(self): #toggle off and on the side menu
        # Show if hidden, hide if visible
        self.side_menu.setVisible(not self.side_menu.isVisible())

    def make_city_button(self, city): #allows the location to be called and show info
        def handler():
            self.load_city_weather(city)
        return handler


    def apply_styles(self):
        self.setStyleSheet(open("styles.qss", "r").read())

    def set_map_widget(self, widget):
        layout = self.map_frame.layout()
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        layout.addWidget(widget)

    def load_city_weather(self, city: str): #for preset locations
        if not city:
            return
        location = get_location(city)
        lat = location["latitude"]
        long = location["longitude"]
        name = location["name"]
        weather = get_weather(lat, long)
        hourly = weather["hourly"]
        temp = hourly["temperature_2m"][0]
        rain_prob = hourly["precipitation_probability"][0]
        wind = hourly["wind_speed_180m"][0]
        cloud = hourly["cloud_cover"][0]
        self.update_weather_display(name, temp, rain_prob, wind, cloud)

    def find_weather(self):
        city = self.search_box.text()
        location = get_location(city)
        lat = location["latitude"]
        long = location["longitude"]
        name = location["name"]
        weather = get_weather(lat, long)
        hourly = weather["hourly"]
        temp = hourly["temperature_2m"][0]
        rain_prob = hourly["precipitation_probability"][0]
        wind = hourly["wind_speed_180m"][0]
        cloud = hourly["cloud_cover"][0]
        weatherinfo = f"{name}\nTemp: {temp} degrees\nRain Chance: {rain_prob}%\nWind Speed: {wind}\nCloud Cover: {cloud}%"
        self.update_weather_display(name, temp, rain_prob, wind, cloud)
    def weather_from_map(self, newLat, newLong): # weather from map click
        lat = newLat
        long = newLong
        name = coord_location(lat, long)
        weather = get_weather(lat, long)
        hourly = weather["hourly"]
        temp = hourly["temperature_2m"][0]
        rain_prob = hourly["precipitation_probability"][0]
        wind = hourly["wind_speed_180m"][0]
        cloud = hourly["cloud_cover"][0]
        weatherinfo = f"{name}\nTemp: {temp} degrees\nRain: {rain_prob}%\nWind: {wind}\nCloud: {cloud}%"
        self.update_weather_display(name, temp, rain_prob, wind, cloud)

    def eventFilter(self, watched, event):
        if watched is self.info_panel and event.type() == QEvent.Resize:
            # keep background covering the whole panel
            self.info_bg.setGeometry(self.info_panel.rect())
        return super().eventFilter(watched, event)
    

    def update_weather_display(self, name, temp, rain_prob, wind, cloud):
        self.location_label.setText(str(name))
        self.temp_label.setText(f"Temp: {temp:.1f} °")
        self.rain_label.setText(f"Rain: {rain_prob}%")
        self.wind_label.setText(f"Wind: {wind}")
        self.cloud_label.setText(f"Cloud: {cloud}%")

        if temp <= 0:
            if rain_prob >= 30:
                state = "Snowing"
            else:
                state = "Freezing"
        elif rain_prob >= 50:
            state = "Rainy"
        elif wind >= 15:
            state = "Windy"
        elif cloud >= 70:
            state = "Cloudy"
        elif cloud >= 40:
            state = "PartlyCloudy"
        else:
            state = "Sunny"

        # Map states -> (icon, background)
        icon_bg_map = {
            "Sunny":        ("Images/ICONS/Sunny.png",
                             "Images/BACKGROUNDS/sunnyday.png"),
            "Cloudy":       ("Images/ICONS/Cloudy.png",
                             "Images/BACKGROUNDS/cloudy.png"),
            "PartlyCloudy": ("Images/ICONS/PartlyCloudy.png",
                             "Images/BACKGROUNDS/partiallyCloudy.png"),
            "Rainy":        ("Images/ICONS/Rainy.png",
                             "Images/BACKGROUNDS/rainy.png"),
            "Windy":        ("Images/ICONS/Windy.png",
                             "Images/BACKGROUNDS/windy.png"),
            "Freezing":     ("Images/ICONS/Freezing.png",
                             "Images/BACKGROUNDS/Winter.png"),
            "Snowing":      ("Images/ICONS/Snowing.png",
                             "Images/BACKGROUNDS/Winter.png"),
        }

        icon_path, bg_path = icon_bg_map.get(state, icon_bg_map["Sunny"])

        # Update icon
        icon_pix = QPixmap(icon_path)
        if not icon_pix.isNull():
            self.icon_label.setPixmap(
                icon_pix.scaled(96, 96, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            )

        # Update background
        bg_pix = QPixmap(bg_path)
        if not bg_pix.isNull():
            self.info_bg.setPixmap(bg_pix)
