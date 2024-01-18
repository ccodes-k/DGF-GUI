# UI for view window

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QWidget

class ViewWindow(QWidget):
    
    def __init__(self):
        '''
            Setting up the window
        '''
        super(ViewWindow, self).__init__()
        self.resize(250, 250)
        self.setWindowTitle("View")
        self.initUI()

    def initUI(self):

        # checkboxes
        self.b1 = QtWidgets.QCheckBox("Heart Rate and SpO2",self)
        self.b1.move(30, 10)
        self.b1.setChecked(True)

        self.b2 = QtWidgets.QCheckBox("Temperature",self)
        self.b2.move(30, 50)
        self.b2.setChecked(True)

        self.b3 = QtWidgets.QCheckBox("Depth",self)
        self.b3.move(30, 90)
        self.b3.setChecked(True)

        self.b4 = QtWidgets.QCheckBox("Lat and Long",self)
        self.b4.move(30, 130)
        self.b4.setChecked(True)

        self.b5 = QtWidgets.QCheckBox("Direction",self)
        self.b5.move(30, 170)
        self.b5.setChecked(True)

        self.b6 = QtWidgets.QCheckBox("Camera",self)
        self.b6.move(30, 210)
        self.b6.setChecked(True)

        self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, False)
        self.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, False)