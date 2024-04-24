# overlay all the widget on map

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore

from src.View_GUI import ViewWindow
from src.Config_GUI import ConfigWindow

import src.FloatingWidgets as FloatingW

from utils.Map import MapDisplay
from utils.server1 import Talker
from utils.GPS_data import SerialDataWriter

import asyncio
import threading
from bleak import BleakClient
import bitstruct
import struct

HR_MEAS = "00002A37-0000-1000-8000-00805F9B34FB"
hrv = 0
stop_thread = False

class Overlayed_W(MapDisplay):
    def __init__(self, parent=None):
        super(Overlayed_W, self).__init__(parent)
        self.setWindowTitle("Diver Monitor")

        self.hr_val = 0

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
    
    # for GPS data
        self.data_writer = SerialDataWriter(port='/dev/ttyUSB0', baudrate=115200)
        self.data_writer.read_and_write_to_file()

    # For map server
        # Connect the closeEvent of the main window to the stop_server method
        self.closeEvent = self.closeEvent
    
    # To update data every 0.25 second
        self.timerM = QtCore.QTimer()
        self.timerM.setInterval(250)
        self.timerM.timeout.connect(self.update_data)
        self.timerM.start()

    # hide temp and depth as not using
        self.DGW.W2.hide()
        self.view_window.b10.setChecked(False)
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
        # self.PlayB.Slam_update_position_Buttons(1)
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
            global stop_thread
            stop_thread = True
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
        self.DGW.W1.updateWaveHR(hrv)
        # For SpO2
        # self.DGW.W2.setSpO2Value(self.config_window.server)
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

#Heart Rate sensor
async def hr_sensor(address, debug=False):
    async with BleakClient(address) as client:
        connected = client.is_connected  
        print("Connected: {0}".format(connected))

        def hr_val_handler(sender, data):
            """Simple notification handler for Heart Rate Measurement."""
            if stop_thread == True:
                return  # Exit the handler if stop_thread is set

            (hr_fmt,
             snsr_detect,
             snsr_cntct_spprtd,
             nrg_expnd,
             rr_int) = bitstruct.unpack("b1b1b1b1b1<", data)
            if hr_fmt:
                hr_val, = struct.unpack_from("<H", data, 1)
            else:
                hr_val, = struct.unpack_from("<B", data, 1)
            print(f"HR Value: {hr_val}")
            global hrv
            hrv = hr_val

        await client.start_notify(HR_MEAS, hr_val_handler)

        while client.is_connected and not stop_thread:  
            await asyncio.sleep(1)

def run_heart_rate_monitor(address, debug=False):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(hr_sensor(address))

if __name__ == "__main__":
    address = "a0:9e:1a:c3:53:b9"
    # Start the heart rate monitoring in a separate thread
    heart_rate_thread = threading.Thread(target=run_heart_rate_monitor, args=(address,))
    heart_rate_thread.start()

    app = QApplication([])
    window = Overlayed_W()
    window.showMaximized()
    sys.exit(app.exec_())