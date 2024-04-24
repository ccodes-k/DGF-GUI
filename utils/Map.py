# create map from index.html
# create server so the map can fetch (read) the txt live

import math
import subprocess
import time
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings

class MapDisplay(QWidget):
    def __init__(self, parent=None):
        super(MapDisplay, self).__init__(parent)

        self.web_view = QWebEngineView()
        self.web_view.settings().setAttribute(QWebEngineSettings.LocalStorageEnabled, True)

        layout = QVBoxLayout(self)
        layout.addWidget(self.web_view)

        self.start_server()

        # the file path: utils/index.html
        url = QUrl("http://localhost:8000/utils/index.html")

        print(url.isValid())
        print(url.toLocalFile())
        self.web_view.setUrl(url)

    def start_server(self):
        # code to start server
        # if not work, try change "python" to "python3"
        self.server_process = subprocess.Popen(["python3", "-m", "http.server", "8000"])
        print("Server started successfully.")
        self.web_view.page().profile().clearAllVisitedLinks()  # Clear entire browser cache
        time.sleep(1)

    def stop_server(self):
        if hasattr(self, 'server_process') and self.server_process.poll() is None:
            self.server_process.terminate()
            self.server_process.wait()
            print("Server process terminated.")
    
    # To update LL Label & LL.txt
    # LL is lat and long
    def update_LL(self):
        r_earth = 6378137  # Earth radius

        with open('./assets/ReadFiles/LLD.txt', 'r') as f1:
            lines = f1.readlines()
            if len(lines) >= 2:
                # Latitude & Longitude
                lat_line = lines[0].strip().split()
                if len(lat_line) >= 3:
                    Lat = lat_line[0]
                    Long = lat_line[1]
        
        Lat = float(Lat)
        Long = float(Long)

        with open('./assets/ReadFiles/txty.txt', 'r') as f2:
            content = f2.read()
            # Split the content into two values using space as a delimiter
            tx, ty = content.split()
            # Convert the values to the appropriate data type
            tx = float(tx)
            ty = float(ty)

        nLat = (Lat + (tx / r_earth) * (180 / math.pi))
        nLong = (Long + (ty / r_earth) * (180 / math.pi) / math.cos(Lat * math.pi / 180))

        nLat = str(nLat)
        nLong = str(nLong)

        with open('./assets/ReadFiles/RLL.txt', 'w') as f3:
            LL_str = nLat + " " + nLong
            f3.write(LL_str)
            f3.flush
        
        self.LLL.setText("Lat: " + nLat + " | Long: " + nLong)