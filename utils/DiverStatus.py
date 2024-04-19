# display different text in different color
# for Diver Status

from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from utils.server import Talker

class StatusLabel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Create a layout for the widget
        layout = QVBoxLayout(self)

        # Add the constant label "Diver Status:"
        self.diver_status_label = QLabel("Diver Status:")
        # Set initial color for the status label
        self.diver_status_label.setStyleSheet(
            "background-color: rgba(255, 255, 255, 150); border-radius: 10px;"
        )
        self.diver_status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.diver_status_label)

        # Add the status label below the constant label
        self.status_label = QLabel("Safe")
        layout.addWidget(self.status_label)

        # Set initial color for the status label
        self.status_label.setStyleSheet(
            "color: lightgreen; background-color: rgba(255, 255, 255, 150); border-radius: 10px;"
        )

        self.status_label.setAlignment(Qt.AlignCenter)  # Align text to the center

        self.diver_status_label.setFont(QFont("Segoe UI", 12))
        self.status_label.setFont(QFont("Segoe UI", 30))

        # Ratio of size
        layout.setStretch(0, 1)
        layout.setStretch(1, 5)

    def set_status(self, status):
        if status == "N":
            self.status_label.setStyleSheet(
                "color: grey; background-color: rgba(255, 255, 255, 150); border-radius: 10px;"
            )
            self.status_label.setText("Null")
        elif status == "S":
            self.status_label.setStyleSheet(
                "color: lightgreen; background-color: rgba(255, 255, 255, 150); border-radius: 10px;"
            )
            self.status_label.setText("Safe")
        elif status == "D":
            self.status_label.setStyleSheet(
                "color: red; background-color: rgba(255, 255, 255, 150); border-radius: 10px;"
            )
            self.status_label.setText("!!! Danger !!!")

    def update_status(self,server):
        if server is None:
            hr = 0
            temp = 0
            spo2 = 0
            self.set_status("N")
            # print("server is None")
        else:
            # Heart Rate
            hr = server.HR
            # Temperature
            #temp = server.temp
            # SpO2
            spo2 = server.SpO2

            if 60 <= hr <= 120 and 95 <= spo2 <= 100:
                # print("hr"+str(hr)+"spo2"+str(spo2))
                self.set_status("S")  # Safe
            else:
                # print("hr"+str(hr)+"spo2"+str(spo2))
                self.set_status("D")  # Dangerous