# Put HR, Temp, SpO2 in to one container

from PyQt5.QtWidgets import QWidget, QVBoxLayout

from utils.HeartRate import WaveHR
from utils.Temperature import OneVerlineT
from utils.SpO2 import OneVerlineO
from utils.Depth import OneHorlineD

class DataDisplay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
    
    def initUI(self):
        container = QWidget(self)
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(20, 20, 20, 20)
        container_layout.setSpacing(5)

        container.setStyleSheet("background-color: rgba(255, 255, 255, 150); border-radius: 10px;")

        # The three widgets functions
        self.W1 = WaveHR()
        self.W2 = OneVerlineO()
        self.W3 = OneVerlineT()
        self.W4 = OneHorlineD()
        
        container_layout.addWidget(self.W1)
        container_layout.addWidget(self.W2)
        container_layout.addWidget(self.W3)
        container_layout.addWidget(self.W4)

        # ratio of the size
        container_layout.setStretch(0, 1)
        container_layout.setStretch(1, 1)
        container_layout.setStretch(2, 1)
        container_layout.setStretch(3, 1)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(container)
