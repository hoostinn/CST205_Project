# Integration of Map into GUI
# map_integration.py
# Handles loading Folium maps into the Qt GUI

import io
import folium 
from PySide6.QtWebEngineWidgets import QWebEngineView

def load_map_into_gui(window):
    # Map of the US
    latitude, longitude = 39, -100
    map = folium.Map(location=[latitude, longitude], zoom_start=4)

    # Convert to HTML
    data = io.BytesIO()
    map.save(data, close_file=False)

    # Add map to QWidget
    webView = QWebEngineView()
    webView.page().setHtml(data.getvalue().decode())

    window.set_map_widget(webView)
