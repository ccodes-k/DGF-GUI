from PyQt5 import QtCore, QtGui, QtWidgets
from utils.Compass import Compasswidget
from GUI.Config_GUI import ConfigWindow

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        ''' 
            It creates the base structure, which creates all the empty widgets that wait for other code to fill in function.
            input: 
                MainWindow (Which is the Whole User Interface including layouts and widgets)
            output: 
                None '''

        # The main window that contain all the widget & layout
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1103, 684)
        self.MainW = QtWidgets.QWidget(MainWindow)
        self.MainW.setObjectName("MainW")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.MainW)
        self.horizontalLayout.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")

        # Left part of the window & layout
        self.LeftW = QtWidgets.QWidget(self.MainW)
        self.LeftW.setObjectName("LeftW")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.LeftW)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(5)
        self.verticalLayout.setObjectName("verticalLayout")

        # In Left part of the window
        # From Top to Bottom, NO.1 widget
        # Option widget & layout, contains options: View, Config, Refresh, InitialStatus(only display)
        self.OptionW = QtWidgets.QWidget(self.LeftW)
        self.OptionW.setObjectName("OptionW")
        self.gridLayout = QtWidgets.QGridLayout(self.OptionW)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(5)
        self.gridLayout.setObjectName("gridLayout")
        
        # In Option widget
        # View Button, just a button in this code
        # The function (to be fill) pop out a window can let user able to choose which widget they want or don't want to see 
        self.ViewB = QtWidgets.QPushButton(self.OptionW)
        self.ViewB.setObjectName("ViewB")
        self.gridLayout.addWidget(self.ViewB, 0, 0, 1, 1)
        self.ViewB.setText("View")

        # In Option widget
        # Config Button, just a button in this code
        # The function (to be fill) pop out a window can let user to choose which signal they want or don't want to receive
        self.ConfigB = QtWidgets.QPushButton(self.OptionW)
        self.ConfigB.setObjectName("ConfigB")
        self.gridLayout.addWidget(self.ConfigB, 0, 1, 1, 1)
        self.ConfigB.setText("Config")
        # Connect the button's clicked signal to show ConfigWindow
        self.config_window = ConfigWindow()
        self.ConfigB.clicked.connect(self.config_window.show)

        # In Option widget
        # Refresh Button, just a button in this code
        # The function (to be fill) will refresh the map
        self.RefreshB = QtWidgets.QPushButton(self.OptionW)
        self.RefreshB.setObjectName("RefreshB")
        self.gridLayout.addWidget(self.RefreshB, 1, 0, 1, 1)
        self.RefreshB.setText("Refresh Map")

        # In Option widget
        # Initial Status Label, just a label in this code
        # The function (to be fill) is to display the program is Initialing / Initialize complete / Initialize fail
        self.InitialStatusL = QtWidgets.QLabel(self.OptionW)
        self.InitialStatusL.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.InitialStatusL.setFrameShadow(QtWidgets.QFrame.Plain)
        self.InitialStatusL.setObjectName("InitialStatusL")
        self.gridLayout.addWidget(self.InitialStatusL, 1, 1, 1, 1)
        self.InitialStatusL.setText("Status: undefined")
        
        # End of create Option widget
        self.verticalLayout.addWidget(self.OptionW)
        
        # In Left part of the window
        # From Top to Bottom, NO.2 widget
        # Heart Rate Widget, just empty widget in this code
        self.HRW = QtWidgets.QWidget(self.LeftW)
        self.HRW.setObjectName("HRW")
        self.verticalLayout.addWidget(self.HRW)

        # In Left part of the window
        # From Top to Bottom, NO.3 widget
        # Temperature Widget, just empty widget in this code
        self.TempW = QtWidgets.QWidget(self.LeftW)
        self.TempW.setObjectName("TempW")
        self.verticalLayout.addWidget(self.TempW)

        # In Left part of the window
        # From Top to Bottom, NO.4 widget
        # Oxygen saturation (SpO2) Widget, just empty widget in this code
        self.O2W = QtWidgets.QWidget(self.LeftW)
        self.O2W.setObjectName("O2W")
        self.verticalLayout.addWidget(self.O2W)
        
        # End of create Left widget
        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 2)
        self.verticalLayout.setStretch(2, 2)
        self.verticalLayout.setStretch(3, 2)
        self.horizontalLayout.addWidget(self.LeftW)

        # Right part of the window & layout
        self.RightW = QtWidgets.QWidget(self.MainW)
        self.RightW.setObjectName("RightW")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.RightW)
        self.verticalLayout_2.setContentsMargins(5, 0, 0, 0)
        self.verticalLayout_2.setSpacing(5)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        # In Right part of the window
        # From Top to Bottom, NO.1 widget
        # Data Widget, contains data: Lat & Long, Battery level
        self.DataW = QtWidgets.QWidget(self.RightW)
        self.DataW.setObjectName("DataW")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.DataW)
        self.horizontalLayout_2.setContentsMargins(-1, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(5)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        # In Data widget
        # From Right to Left, NO.1 Label
        # Lat & Long Label, just a label in this code
        # The function (to be fill) is to display Lat & Long get from GPS
        self.LatLongL = QtWidgets.QLabel(self.DataW)
        self.LatLongL.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.LatLongL.setFrameShadow(QtWidgets.QFrame.Plain)
        self.LatLongL.setAlignment(QtCore.Qt.AlignCenter)
        self.LatLongL.setObjectName("LatLongL")
        self.horizontalLayout_2.addWidget(self.LatLongL)
        self.LatLongL.setText("Current Location: Lat: Long:")
        
        # In Data widget
        # From Right to Left, NO.2 Label
        # Battery Label, just a label in this code
        # The function (to be fill) is to display Battery level get from Raspberry Pi
        self.BatteryL = QtWidgets.QLabel(self.DataW)
        self.BatteryL.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.BatteryL.setFrameShadow(QtWidgets.QFrame.Plain)
        self.BatteryL.setAlignment(QtCore.Qt.AlignCenter)
        self.BatteryL.setObjectName("BatteryL")
        self.horizontalLayout_2.addWidget(self.BatteryL)
        self.BatteryL.setText("Battery Level:")

        # End of create Data widget
        self.horizontalLayout_2.setStretch(0, 2)
        self.horizontalLayout_2.setStretch(1, 1)
        self.verticalLayout_2.addWidget(self.DataW)

        # In Right part of the window
        # From Top to Bottom, NO.2 widget
        # Map Widget, contains Widgets: Map (background) + Compass & Direction, DiverStatus, Buttons for SLAM (overlay on map)
        self.MapW = QtWidgets.QWidget(self.RightW)
        self.MapW.setObjectName("MapW")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.MapW)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName("gridLayout_2")

        # Spacers to push widgets to desired position, push to center and push to right corner
        spacerItem = QtWidgets.QSpacerItem(236, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 0, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 396, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        self.gridLayout_2.addItem(spacerItem1, 1, 3, 1, 1)

        # In Map Widget
        # Bottom Right corner, contain driection label and display compass
        self.CompassW_Container = QtWidgets.QWidget(self.MapW)
        self.CompassW_Container.setObjectName("CompassW_Container")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.CompassW_Container)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(5)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        
        # In CompassW_Container
        # Direction Label, just a label in this code
        # The function (to be fill) is to display Direction get from GPS
        self.DirectionL = QtWidgets.QLabel(self.CompassW_Container)
        self.DirectionL.setObjectName("DirectionL")
        self.verticalLayout_3.addWidget(self.DirectionL)
        self.DirectionL.setText("Direction: ")
        
        # In CompassW_Container
        # Compass wiget, just a widget in this code
        # The function is to display Direction (get from GPS) in Compass
        self.CompassW = Compasswidget(self.CompassW_Container)
        self.CompassW.setAngle(0) # set initial angle
        self.CompassW.setObjectName("CompassW")
        self.verticalLayout_3.addWidget(self.CompassW)
        self.verticalLayout_3.setStretch(0, 1)
        self.verticalLayout_3.setStretch(1, 3)
        self.gridLayout_2.addWidget(self.CompassW_Container, 2, 3, 1, 1)

        # In Map Widget
        # Top Center corner, contain Diver Status label and display Diver Status
        self.DiverStatusW_Container = QtWidgets.QWidget(self.MapW)
        self.DiverStatusW_Container.setObjectName("DiverStatusW_Container")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.DiverStatusW_Container)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setSpacing(5)
        self.verticalLayout_4.setObjectName("verticalLayout_4")

        # In DiverStatusW_Container
        # Diver Status Label, title, will not change
        self.DiverStatusL = QtWidgets.QLabel(self.DiverStatusW_Container)
        self.DiverStatusL.setObjectName("DiverStatusL")
        self.DiverStatusL.setAlignment(QtCore.Qt.AlignCenter)
        self.verticalLayout_4.addWidget(self.DiverStatusL)
        self.DiverStatusL.setText("Diver Status:")

        # In DiverStatusW_Container
        # Diver Status widget, just a widget in this code
        # The function (to be fill) is to display diver status like safe (in green), danger (in red)
        self.DiverStatusW = QtWidgets.QWidget(self.DiverStatusW_Container)
        self.DiverStatusW.setObjectName("DiverStatusW")
        self.verticalLayout_4.addWidget(self.DiverStatusW)
        self.verticalLayout_4.setStretch(0, 1)
        self.verticalLayout_4.setStretch(1, 2)
        self.gridLayout_2.addWidget(self.DiverStatusW_Container, 0, 1, 1, 1)
        
        # In Map Widget
        # Bottom Center corner, contain play, pause, stop buttons to contorl SLAM
        self.SLAM_W = QtWidgets.QWidget(self.MapW)
        self.SLAM_W.setObjectName("SLAM_W")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.SLAM_W)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setSpacing(5)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        
        # In SLAM Widget
        # Play button, just a widget in this code
        # The function (to be fill) is to start the SLAM
        self.PlayB = QtWidgets.QPushButton(self.SLAM_W)
        self.PlayB.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./assets/Icons/play-button-arrowhead.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.PlayB.setIcon(icon)
        self.PlayB.setObjectName("PlayB")
        self.horizontalLayout_3.addWidget(self.PlayB)
        
        # In SLAM Widget
        # Pause button, just a widget in this code
        # The function (to be fill) is to pause the SLAM
        self.PauseB = QtWidgets.QPushButton(self.SLAM_W)
        self.PauseB.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("./assets/Icons/pause.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.PauseB.setIcon(icon1)
        self.PauseB.setObjectName("PauseB")
        self.horizontalLayout_3.addWidget(self.PauseB)
        
        # In SLAM Widget
        # Stop button, just a widget in this code
        # The function (to be fill) is to stop the SLAM
        self.StopB = QtWidgets.QPushButton(self.SLAM_W)
        self.StopB.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("./assets/Icons/stop-button.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.StopB.setIcon(icon2)
        self.StopB.setObjectName("StopB")
        self.horizontalLayout_3.addWidget(self.StopB)
        self.gridLayout_2.addWidget(self.SLAM_W, 2, 1, 1, 1)

        # In Map Widget
        # Top Right corner, just widget in this code
        # The function (to be fill) is to display the frame get from cmaera (that should be wear by diver) 
        self.CameraW = QtWidgets.QWidget(self.MapW)
        self.CameraW.setObjectName("CameraW")
        self.gridLayout_2.addWidget(self.CameraW, 0, 3, 1, 1)

        # Spacers to push widgets to desired position, push to bottom and push to center
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem2, 0, 2, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem3, 2, 2, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem4, 2, 0, 1, 1)

        # End of create Map Widget
        self.gridLayout_2.setColumnStretch(0, 2)
        self.gridLayout_2.setColumnStretch(1, 1)
        self.gridLayout_2.setColumnStretch(2, 2)
        self.gridLayout_2.setColumnStretch(3, 1)
        self.gridLayout_2.setRowStretch(0, 1)
        self.gridLayout_2.setRowStretch(1, 3)
        self.gridLayout_2.setRowStretch(2, 1)
        self.verticalLayout_2.addWidget(self.MapW)

        # End of create Right Widget
        self.verticalLayout_2.setStretch(0, 1)
        self.verticalLayout_2.setStretch(1, 10)
        self.horizontalLayout.addWidget(self.RightW)

        # End of create Main Widget
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 2)
        MainWindow.setCentralWidget(self.MainW)
        MainWindow.setWindowTitle("MainWindow")

if __name__ == "__main__":
    ''' To Run the whole code
    input: None
    Output: None ''' 
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Monitor = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(Monitor)
    Monitor.showMaximized()
    sys.exit(app.exec_())