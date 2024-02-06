# create map from index.html
# create server so the map can fetch (read) the txt live

import math
import subprocess
import time
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from utils.server1 import Talker

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
    def update_LL(self, server):
            r_earth = 6378137  # Earth radius

            if server is None:
                Lat = 0
                Long = 0
                LatD = 0
                LongD = 0
            else: 
                Lat = float(server.Lat[0-1]) + ( float(server.Lat[2-8]) / 60)
                Long = float(server.Long[0-2]) + ( float(server.Long[3-9]) / 60)
                LatD = server.LatD
                LongD = server.LongD

                with open('/assets/ReadFiles/tx_ty.txt', 'r') as f1:
                    content = f1.read()
                    # Split the content into two values using space as a delimiter
                    tx, ty = content.split()
                    # Convert the values to the appropriate data type
                    tx = float(tx)
                    ty = float(ty)

                nLat = (Lat + (tx / r_earth) * (180 / math.pi))
                nLong = (Long + (ty / r_earth) * (180 / math.pi) / math.cos(Lat * math.pi / 180))

                with open('/assets/ReadFiles/lat_long.txt', 'w') as f2:
                    LL_str = nLat + " " + nLong
                    f2.write(LL_str)
                    f2.flush
                
                self.LLL.setText("Lat: " + nLat + " " + LatD + " | Long: " + nLong + " " + LongD)