# main.py
# Starter point for the App

import sys
from PySide6.QtWidgets import QApplication
from starter_gui import WeatherAppGUI
from map_integration import load_map_into_gui

def main():
    app = QApplication(sys.argv)

    window = WeatherAppGUI()
    window.show()

    # Load map on startup
    try:
        load_map_into_gui(window)
    except Exception as e:
        print("Map not loaded:", e)

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
