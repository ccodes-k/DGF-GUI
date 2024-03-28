# create map from index.html
# create server so the map can fetch (read) the txt live

import math
import subprocess
import time
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from utils.GPS_data import SerialDataWriter

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

        # for GPS data
        self.data_writer = SerialDataWriter()

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
        # get GPS data
        self.data_writer.read_and_write_to_file()

        r_earth = 6378137  # Earth radius

        with open('/assets/ReadFiles/LLD.txt', 'r') as f1:
            content = f1.read()
            # Extract values from the content
            if len(content) >= 3:
                # Latitude
                lat_line = content[0].strip().split()
                Lat = lat_line[0]
                LatD = lat_line[1]
                
                # Longitude
                long_line = content[1].strip().split()
                Long = long_line[0]
                LongD = long_line[1]          

        with open('/assets/ReadFiles/txty.txt', 'r') as f2:
            content = f2.read()
            # Split the content into two values using space as a delimiter
            tx, ty = content.split()
            # Convert the values to the appropriate data type
            tx = float(tx)
            ty = float(ty)

        nLat = (Lat + (tx / r_earth) * (180 / math.pi))
        nLong = (Long + (ty / r_earth) * (180 / math.pi) / math.cos(Lat * math.pi / 180))

        with open('/assets/ReadFiles/RLL.txt', 'w') as f3:
            LL_str = nLat + " " + nLong
            f3.write(LL_str)
            f3.flush
        
        self.LLL.setText("Lat: " + nLat + " " + LatD + " | Long: " + nLong + " " + LongD)