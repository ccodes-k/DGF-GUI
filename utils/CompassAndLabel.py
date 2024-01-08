# Put compass and direction label in to one container

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from utils.Compass import Compasswidget

class CompassDisplay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
    
    def initUI(self):
        container = QWidget(self)
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(5)

        # The direction label
        self.L1 = QLabel("Direction: NUll")
        self.L1.setAlignment(Qt.AlignCenter)
        self.L1.setFont(QFont("Segoe UI", 12))
        self.L1.setStyleSheet("background-color: rgba(255, 255, 255, 150); border-radius: 10px;")
        # The compass widget
        self.W1 = Compasswidget(parent=self)
        self.W1.setStyleSheet("background-color: rgba(255, 255, 255, 150); border-radius: 10px;")
        
        container_layout.addWidget(self.L1)
        container_layout.addWidget(self.W1)

        # ratio of the size
        container_layout.setStretch(0, 1)
        container_layout.setStretch(1, 7)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(container)