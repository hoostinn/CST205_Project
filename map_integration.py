# Integration of Map into GUI
# map_integration.py
# Handles loading Folium maps into the Qt GUI

import io
import folium 
from PySide6.QtWebChannel import QWebChannel
from PySide6.QtWebEngineWidgets import QWebEngineView
from streamlit_folium import st_folium
import streamlit as st
from weather_api import get_weather, get_location
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import threading

def find_popup_slice(html):
    '''
    Find the starting and ending index of popup function
    '''

    pattern = "function latLngPop(e)"

    #starting index
    starting_index = html.find(pattern)

    # 
    tmp_html = html[starting_index:]

    #
    found = 0
    index = 0
    opening_found = False
    while not opening_found or found > 0:
        if tmp_html[index] == "{":
            found += 1
            opening_found = True
        elif tmp_html[index] == "}":
            found -= 1
        
        index += 1

    # determine the ending index of popup function
    ending_index = starting_index + index

    return starting_index, ending_index

def find_variable_name(html, name_start):
    variable_pattern = "var "
    pattern = variable_pattern + name_start

    starting_index = html.find(pattern) + len(variable_pattern)
    tmp_html = html[starting_index:]
    ending_index = tmp_html.find(" =") + starting_index

    return html[starting_index:ending_index]

def grab_coordinates(coords):
    # Slice latitude
    lat_start = coords.find("latitude")
    lat_start = coords.find(":", lat_start) + 1
    lat_end = coords.find(",", lat_start)

    latitude = float(coords[lat_start:lat_end])

    # Slice longitude
    long_start = coords.find("longitude")
    long_start = coords.find(":", long_start) + 1
    long_end = coords.find(",", long_start)

    longitude = float(coords[long_start:long_end])

    return latitude, longitude

def custom_code(popup_variable_name, map_variable_name, folium_port):
    return f"""
    function latLngPop(e) {{
        window._clickedLat = e.latlng.lat;
        window._clickedLng = e.latlng.lng;

        {popup_variable_name}
            .setLatLng(e.latlng)
            .setContent(`
                Display weather info
                at this location?

                <button onClick="
                    fetch('http://localhost:{folium_port}', {{
                        method: 'POST',
                        mode: 'no-cors',
                        headers: {{
                            'Content-Type': 'application/json'
                        }},
                        body: JSON.stringify({{
                            latitude: window._clickedLat,
                            longitude: window._clickedLng
                        }})
                    }});
                    L.marker([window._clickedLat, window._clickedLng]).addTo({map_variable_name});
                "> Yes </button>

            `)
            .openOn({map_variable_name});
    }}
    """

# Allows us to emit a signal to change the GUI
def create_folium_handler(signal_to_emit):
    class FoliumServer(BaseHTTPRequestHandler):
        def _set_response(self):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()

        # Decodes data from port and take in coordinates
        def do_POST(self):

            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)

            data = post_data.decode("utf-8")
            # print(data)
            coords = data
            lat, long = grab_coordinates(coords)
            # print(lat, long)

            signal_to_emit.emit(lat, long)
            self._set_response()
    return FoliumServer
            


def listen_to_folium_map(port=3001, signal = None):
    HandlerClass = create_folium_handler(signal)
    server_address = ('', port)
    httpd = HTTPServer(server_address, HandlerClass)
    print("Server Started")
    try:
        httpd.serve_forever()
    except Exception as ex:
        pass

    httpd.server_close()
    print("Server Stopped")


def load_map_into_gui(window):

    folium_port = 3001

    # HTML
    map_filepath = "folium-map.html"

    # Map of the US
    latitude, longitude = 39, -100
    map = folium.Map(location=[latitude, longitude], zoom_start=4)


    # Add Popup
    folium.LatLngPopup().add_to(map)

    # Adding marker
    folium.Marker(
        location=[latitude, longitude]
    ).add_to(map)

    # Save the mapfile
    map.save(map_filepath)

    # read ing the folium file
    html = None
    with open(map_filepath, 'r') as mapfile:
        html = mapfile.read()

    # find variable names
    map_variable_name = find_variable_name(html, "map_") 
    popup_variable_name = find_variable_name(html, "lat_lng_popup_")

    # Determine popup function indices
    pstart, pend = find_popup_slice(html)

    # inject code
    modified_html = (
        html[:pstart] + \
        custom_code(popup_variable_name, map_variable_name, folium_port) + \
        html[pend:]
    )

    # Add map to QWidget
    webView = QWebEngineView()
    webView.page().setHtml(modified_html)

    window.set_map_widget(webView)

    with open(map_filepath, "w") as f:
        f.write(modified_html)

    # run webserver that listens to sent coordinates
    # Uses threading so that the server runs in the background during QT
    threading.Thread(
        target = listen_to_folium_map,
        args=(folium_port, window.coordinates_received_signal,),
        daemon=True
    ).start()

    # Test code
    # print(html[pstart:pend])
    # print(map_variable_name)
    # print(popup_variable_name)

