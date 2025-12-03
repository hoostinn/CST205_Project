# Matteo Part 
# Integration of Map into GUI
# map_integration.py
# Handles loading Folium maps into the Qt GUI

import os
from PySide6.QtCore import QUrl
from PySide6.QtWebEngineWidgets import QWebEngineView

def load_map_into_gui(window):
    map_path = os.path.abspath("maps/map.html")

    if not os.path.exists(map_path):
        raise FileNotFoundError("maps/map.html not found")

    view = QWebEngineView()
    view.load(QUrl.fromLocalFile(map_path))

    window.set_map_widget(view)
