from PySide6.QtWidgets import (
    QApplication, QWidget, QHBoxLayout, QVBoxLayout,
    QLineEdit, QPushButton, QLabel, QFrame
)
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QFont
import sys

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
        info_layout.addWidget(self.info_title)

        # RIGHT SIDE (SEARCH + MAP)
        right_side = QVBoxLayout()
        right_side.setSpacing(20)

        # Search Bar 
        top_bar = QHBoxLayout()
        top_bar.setSpacing(10)

        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search city...")
        self.search_box.setObjectName("searchBox")
        self.search_box.setFixedHeight(45)

        search_btn = QPushButton("🔍")
        search_btn.setObjectName("searchBtn")
        search_btn.setFixedSize(45, 45)

        menu_btn = QPushButton("☰")
        menu_btn.setObjectName("menuBtn")
        menu_btn.setFixedSize(45, 45)

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

        # Add panels
        main_layout.addWidget(self.info_panel)
        main_layout.addLayout(right_side)

    def apply_styles(self):
        self.setStyleSheet(open("styles.qss", "r").read())

    def set_map_widget(self, widget):
        layout = self.map_frame.layout()
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        layout.addWidget(widget)
