# create map from index.html
# create server so the map can fetch (read) the txt live

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
        
    def update_LL(self, server):
        if server is None:
            Lat = 0
            Long = 0
        else: 
            Lat = float(server.Lat[0-1]) + ( float(server.Lat[2-8]) / 60)
            Long = float(server.Long[0-2]) + ( float(server.Long[3-9]) / 60)
            LatD = server.LatD
            LongD = server.LongD

            with open('/assets/ReadFiles/lat_long.txt', 'w') as f:
                LL_str = Lat + " " + Long
                f.write(LL_str)
                f.flush
            
            self.LLL.setText("Lat: " + Lat + " " + LatD + " | Long: " + Long + " " + LongD)