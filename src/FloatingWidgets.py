# All the floating widgets that are going to overlay on map

from PyQt5.QtWidgets import QPushButton, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from utils.DiverStatus import StatusLabel
from utils.CompassAndLabel import CompassDisplay

from utils.DataGraphs import DataDisplay

from utils.Camera import CameraW

# Option Buttons
class Ob_Floating_Button(QPushButton):
    def __init__(self, parent, text=""):
        super().__init__(text, parent)
        self.paddingTop = 30
        self.paddingRight = 100

        self.setStyleSheet("background-color: rgba(255, 255, 255, 200); border-radius: 10px;")
        self.setFont(QFont("Segoe UI", 12))

    # Top Left
    def Ob_update_position_Buttons(self, index):
        x = self.paddingRight + index * (self.width() + 10)
        y = self.paddingTop
        self.setGeometry(x, y, self.width(), self.height())
    
    # Override the hover enter event
    def enterEvent(self, event):
        # Change the background color when mouse enters
        self.setStyleSheet("background-color: rgba(255, 255, 255, 255); border-radius: 10px;")

    # Override the hover leave event
    def leaveEvent(self, event):
        # Revert to the default background color when mouse leaves
        self.setStyleSheet("background-color: rgba(255, 255, 255, 200); border-radius: 10px;")

# Diver Status
class Ds_Floating_Widget(StatusLabel): 
    def __init__(self, parent=None):
        super().__init__(parent)
        self.paddingTop = 30

    # Top Center
    def Ds_update_position_Widgets(self):
        parent_width = self.parent().width()
        x = (parent_width - self.width()) // 2
        y = self.paddingTop
        self.setGeometry(x, y, 300, 120)

# Lat & Long Label
class LL_Floating_Widget(QLabel): 
    def __init__(self, parent, text=""):
        super().__init__(text, parent)
        self.paddingTop = 40
        self.paddingRight = 30

        self.setStyleSheet("background-color: rgba(255, 255, 255, 150); border-radius: 10px;")
        self.setFont(QFont("Segoe UI", 12))
        self.setAlignment(Qt.AlignCenter)

    # Top Center-Right
    def LL_update_position_Widgets(self):
        parent_width = self.parent().width()
        x = ((parent_width - self.width()) // 4) * 3
        y = self.paddingTop
        self.setGeometry(x, y, 360, 40)

# Compass
class Com_Floating_Widget(CompassDisplay): 
    def __init__(self, parent=None):
        super().__init__(parent)
        self.paddingTop = 30
        self.paddingRight = 30
        self._margins = 30

    # Top Right
    def Com_update_position_Widgets(self):
        parent_width = self.parent().width()
        x = parent_width - self.width() - self.paddingRight
        y = self.paddingTop
        self.setGeometry(x, y, 220, 240)

# SLAM Buttons
class Slam_Floating_Button(QPushButton):
    def __init__(self, parent, text=""):
        super().__init__(text, parent)
        self.paddingBottom = 30

        self.setStyleSheet("background-color: rgba(255, 255, 255, 200); border-radius: 10px;")
        self.setFont(QFont("Segoe UI", 12))

    # Bottom Center
    def Slam_update_position_Buttons(self, index):
        parent_width = self.parent().width()
        total_width = 2 * self.width() + 10  # Total width of all three buttons
        x = (parent_width - total_width) // 2 + index * (self.width() + 5)
        y = self.parent().height() - self.height() - self.paddingBottom  
        self.setGeometry(x, y, self.width() + 2, self.height() + 2)
    
    # Override the hover enter event
    def enterEvent(self, event):
        # Change the background color when mouse enters
        self.setStyleSheet("background-color: rgba(255, 255, 255, 255); border-radius: 10px;")

    # Override the hover leave event
    def leaveEvent(self, event):
        # Revert to the default background color when mouse leaves
        self.setStyleSheet("background-color: rgba(255, 255, 255, 200); border-radius: 10px;")

# SLAM indicator
class SI_Floating_Button(QLabel):
    def __init__(self, parent, text=""):
        super().__init__(text, parent)
        self.paddingBottom = 70

        self.setStyleSheet("background-color: rgba(255, 255, 255, 150); border-radius: 10px;")
        self.setFont(QFont("Segoe UI", 12))
        self.setAlignment(Qt.AlignCenter)

    # Bottom Center - upper than buttons
    def SI_update_position_Buttons(self):
        parent_width = self.parent().width()
        parent_height = self.parent().height()
        x = (parent_width - self.width()) // 2
        y = int(parent_height - self.height() - self.paddingBottom)
        self.setGeometry(x, y, 150, 30)

# Data Graphs
class Data_Floating_Widget(DataDisplay): 
    def __init__(self, parent=None):
        super().__init__(parent)
        self.paddingLeft = 30

    # Middle Left
    def Data_update_position_Widgets(self):
        parent_height = self.parent().height()
        x = self.paddingLeft  # Adjust this value if needed
        y = int(parent_height / 2 - self.height() / 2 + 50)  # + or - for the desired shift
        self.setGeometry(x, y, 500, 850)

# Camera
class Cam_Floating_Widget(CameraW):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.paddingRight = 30
        self.paddingBottom = 45
        self.setStyleSheet("background-color: rgba(255, 255, 255, 150); border-radius: 10px;")

    # Bottom Right
    def Cam_update_position_Widgets(self):
        parent_width = self.parent().width()
        parent_height = self.parent().height()
        x = int(parent_width - self.width() - self.paddingRight)
        y = int(parent_height - self.height() - self.paddingBottom)
        self.setGeometry(x, y, 320, 240)