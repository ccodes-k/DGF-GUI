# overlay all the widget on map

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore

from src.View_GUI import ViewWindow
from src.Config_GUI import ConfigWindow

import src.FloatingWidgets as FloatingW

from utils.Map import MapDisplay

class Overlayed_W(MapDisplay):
    def __init__(self, parent=None):
        super(Overlayed_W, self).__init__(parent)
        self.setWindowTitle("Diver Monitor")

    # Option Buttons:

        # Config Button
        self.ConfigB = FloatingW.Ob_Floating_Button(parent=self, text="Config")
        # Connect the button's clicked signal to show ConfigWindow
        self.config_window = ConfigWindow()
        self.ConfigB.clicked.connect(self.config_window.show)

        # View Button
        self.ViewB = FloatingW.Ob_Floating_Button(parent=self, text="View")
        # Connect the button's clicked signal to show ViewWindow
        self.view_window = ViewWindow()
        self.ViewB.clicked.connect(self.view_window.show)

    # Diver Status:
        self.DiverStatus = FloatingW.Ds_Floating_Widget(parent=self)

    # Lat & Long Label:
        self.LLL = FloatingW.LL_Floating_Widget(parent=self, text="Lat: Null | Long: Null")

    # Compass:
        self.Compass = FloatingW.Com_Floating_Widget(parent=self)

    # SLAM Buttons:
        # SLAM indicator
        self.SI = FloatingW.SI_Floating_Button(parent=self, text="SLAM: Stop")
        
        # Start & Stop Button
        self.StartB = FloatingW.Slam_Floating_Button(parent=self, text="Start")

        # Play & Pause Button
        self.PlayB = FloatingW.Slam_Floating_Button(parent=self, text="Play")
    
    # Data Graphs
        self.DGW = FloatingW.Data_Floating_Widget(parent=self)
    
    # Camera
        self.Cam = FloatingW.Cam_Floating_Widget(parent=self, server =self.config_window)

    # For map server
        # Connect the closeEvent of the main window to the stop_server method
        self.closeEvent = self.closeEvent
    
    # To update data every 0.25 second
        self.timerM = QtCore.QTimer()
        self.timerM.setInterval(250)
        self.timerM.timeout.connect(self.update_data)
        self.timerM.start()

    def resizeEvent(self, event):
        super().resizeEvent(event)

    # Option Buttons
        self.ConfigB.Ob_update_position_Buttons(0)
        self.ViewB.Ob_update_position_Buttons(1)

    # Diver Status
        self.DiverStatus.Ds_update_position_Widgets()
    
    # Lat & Long Label:
        self.LLL.LL_update_position_Widgets()

    # Compass
        self.Compass.Com_update_position_Widgets()

    # SLAM Buttons
        self.SI.SI_update_position_Buttons()
        self.PlayB.Slam_update_position_Buttons(0)
        self.StartB.Slam_update_position_Buttons(1)
    
    # Data Graphs
        self.DGW.Data_update_position_Widgets()
    
    # Camera
        self.Cam.Cam_update_position_Widgets()
    
    # close event for map, to close the server
    def closeEvent(self, event):
            # Perform any additional cleanup here if needed
            self.stop_server()
            event.accept()  # Allow the window to close

    # To update data
    def update_data(self):

    # For Lat & Long
        Lat = str(1.446188)
        Long = str(103.784179)
        self.LLL.setText("Lat: " + Lat + " | Long: " + Long)

    # For Compass and Direction Label
        x=str(47)
        y=47
        self.Compass.L1.setText("Direction: " + x)
        self.Compass.W1.setAngle(y)

    # For Data Graphs
        # For Heart Rate
        self.DGW.W1.updateWaveHR(self.config_window.server)
        # For SpO2
        self.DGW.W2.setSpO2Value(self.config_window.server)
        # For Temperature
        self.DGW.W3.setTemperatureValue(self.config_window.server)
        # For Depth
        self.DGW.W4.setDepthValue(self.config_window.server)
        # print("Data Updated")
    
    # For Diver Status
    # so the label will be Null, Safe or Danger
        self.DiverStatus.update_status(self.config_window.server)

    # For SLAM indicator
    # Some if else for SLAM start or stop or pause
        self.SI.setText("SLAM: Null")

    #For Camera
        self.Cam.Cam_update_position_Widgets()

if __name__ == "__main__":
    app = QApplication([])
    window = Overlayed_W()
    window.showMaximized()
    sys.exit(app.exec_())