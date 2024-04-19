# overlay all the widget on map

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore

from src.View_GUI import ViewWindow
from src.Config_GUI import ConfigWindow

import src.FloatingWidgets as FloatingW

from utils.Map import MapDisplay
from utils.server1 import Talker

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
        self.SI = FloatingW.SI_Floating_Button(parent=self, text="SLAM: Null")
        
        self.talker_instatnce = Talker()

        # Start & Stop Button
        self.StartB = FloatingW.Slam_Floating_Button(parent=self, text="Start")
        self.StartB.clicked.connect(self.talker_instatnce.start_slam)

        # # Play & Pause Button - change to SLAMmtll
        # self.PlayB = FloatingW.Slam_Floating_Button(parent=self, text="mtll")
        # self.PlayB.clicked.connect(self.mtll_instance.start)
    
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

    # hide temp and depth as not using
        self.DGW.W3.hide()
        self.view_window.b2.setChecked(False)
        self.DGW.W4.hide()
        self.view_window.b3.setChecked(False)

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
        self.PlayB.Slam_update_position_Buttons(1)
        self.StartB.Slam_update_position_Buttons(0)
    
    # Data Graphs
        self.DGW.Data_update_position_Widgets()
    
    # Camera
        self.Cam.Cam_update_position_Widgets()
    
    # close event for map, to close the server
    # close event for view and config window
    # close event for SLAM
    def closeEvent(self, event):
            # Perform any additional cleanup here if needed
            self.stop_server()
            self.config_window.close()
            self.view_window.close()
            self.talker_instatnce.stop_slam()
            event.accept()  # Allow the window to close

    # To update data
    def update_data(self):
    # For SLAM
        if self.talker_instatnce.slam_SS == "start":
             self.SI.setText("SLAM: Start")
             self.StartB.setText("Stop")
             self.StartB.clicked.disconnect()
             self.StartB.clicked.connect(self.talker_instatnce.stop_slam)

        if self.talker_instatnce.slam_SS == "stop":
             self.SI.setText("SLAM: Stop")
             self.StartB.setText("Start")
             self.StartB.clicked.disconnect()
             self.StartB.clicked.connect(self.talker_instatnce.start_slam)

        # if self.talker_instatnce.slam_PP == False:
        #      self.SI.setText("SLAM: Pause")
        #      self.PlayB.setText("Play")
             
        # if self.talker_instatnce.slam_PP == True:
        #      self.PlayB.setText("Pause")

    # For Lat & Long
        MapDisplay.update_LL(self)

    # For Compass and Direction Label
        self.Compass.update_Deg()

    # For Data Graphs
        # For Heart Rate
        self.DGW.W1.updateWaveHR(self.config_window.server)
        # For SpO2
        self.DGW.W2.setSpO2Value(self.config_window.server)
        # For Temperature
        #self.DGW.W3.setTemperatureValue(self.config_window.server)
        # For Depth
        #self.DGW.W4.setDepthValue(self.config_window.server)
        # print("Data Updated")
    
    # For Diver Status
    # so the label will be Null, Safe or Danger
        self.DiverStatus.update_status(self.config_window.server)

    # For Camera
        self.Cam.Cam_update_position_Widgets()

    # For hide and show
        ViewWindow.update_view(self,self.view_window)

if __name__ == "__main__":
    app = QApplication([])
    window = Overlayed_W()
    window.showMaximized()
    sys.exit(app.exec_())