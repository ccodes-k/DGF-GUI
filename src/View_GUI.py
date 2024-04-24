# UI for view window

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QWidget

class ViewWindow(QWidget):
    
    def __init__(self):
        '''
            Setting up the window
        '''
        super(ViewWindow, self).__init__()
        self.resize(250, 290)
        self.setWindowTitle("View")
        self.initUI()

    def initUI(self):

        # checkboxes
        self.b1 = QtWidgets.QCheckBox("Heart Rate",self)
        self.b1.move(30, 10)
        self.b1.setChecked(True)

        self.b10 = QtWidgets.QCheckBox("SpO2",self)
        self.b10.move(30, 50)
        self.b10.setChecked(True)

        self.b2 = QtWidgets.QCheckBox("Temperature",self)
        self.b2.move(30, 90)
        self.b2.setChecked(True)

        self.b3 = QtWidgets.QCheckBox("Depth",self)
        self.b3.move(30, 130)
        self.b3.setChecked(True)

        self.b4 = QtWidgets.QCheckBox("Lat and Long",self)
        self.b4.move(30, 170)
        self.b4.setChecked(True)

        self.b5 = QtWidgets.QCheckBox("Direction and Compass",self)
        self.b5.move(30, 210)
        self.b5.setChecked(True)

        self.b6 = QtWidgets.QCheckBox("Camera",self)
        self.b6.move(30, 250)
        self.b6.setChecked(True)

        self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, False)
        self.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, False)
    
    def update_view(self,view):

    # For Data Graphs
        
        # For Heart Rate
        if view.b1.isChecked():
            self.DGW.W1.show()
        elif not view.b1.isChecked():
            self.DGW.W1.hide()
        
        # For SpO2
        if view.b10.isChecked():
            self.DGW.W2.show()
        elif not view.b10.isChecked():
            self.DGW.W2.hide()

        # For Temperature
        if view.b2.isChecked():
            self.DGW.W3.show()
        elif not view.b2.isChecked():
            self.DGW.W3.hide()

        # For Depth
        if view.b3.isChecked():
            self.DGW.W4.show()
        elif not view.b3.isChecked():
            self.DGW.W4.hide()

        # For the whole Data Graphs
        if view.b1.isChecked() or view.b10.isChecked() or view.b2.isChecked() or view.b3.isChecked():
            self.DGW.show()
        elif not view.b1.isChecked() and not view.b10.isChecked() and not view.b2.isChecked() and not view.b3.isChecked():
            self.DGW.hide()
    
    # For GPS
        
        # For Lat and Long
        if view.b4.isChecked():
            self.LLL.show()
        elif not view.b4.isChecked():
            self.LLL.hide()
        
        # For Compass and Direction Label
        if view.b5.isChecked():
            self.Compass.show()
        elif not view.b5.isChecked():
            self.Compass.hide()
    
    # For Camera
        if view.b6.isChecked():
            self.Cam.show()
        elif not view.b6.isChecked():
            self.Cam.hide()