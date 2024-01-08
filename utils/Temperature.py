# plot the graph with one vertical line
# for Temperature

import pyqtgraph as pg
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from utils.server import Talker

class OneVerlineT(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        # Label for Temp
        self.label = QLabel("Temperature: ", self)
        self.label.setFont(QFont("Segoe UI", 12))
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        # Create a PlotWidget
        self.plotWidget = pg.PlotWidget(self)
        layout.addWidget(self.plotWidget)

        # Ratio of size
        layout.setStretch(0, 1)
        layout.setStretch(1, 7)

        self.customizePlotWidget()

    def customizePlotWidget(self):
        # Set background color
        self.plotWidget.setBackground('default')

        # Set x-axis range
        self.plotWidget.setXRange(30, 40, padding=0)

        # Hide left axis
        self.plotWidget.getPlotItem().hideAxis('left')

        # Initialize temperature value
        self.Tv = 35.6

        # Add the initial line
        self.line = pg.InfiniteLine(self.Tv, pen='b')
        self.plotWidget.addItem(self.line)

    def updateVerticalLine(self, new_value):
        # Update the existing line with the new temperature value
        self.line.setValue(new_value)

    def setTemperatureValue(self, server):
        # Set a new temperature value and update the vertical line
        if server is None:
           new_value = 0
        else: 
            new_value = server.temp
        #Label
        self.label.setText(f"Temperature: {new_value}")
        #Graph
        self.updateVerticalLine(new_value)

# # Example usage:
# # Create a parent widget
# parent_widget = QWidget()

# # Create an instance of OneVerlineT and pass the parent widget
# W1 = OneVerlineT(parent_widget)

# # Add the widget to the layout of the parent widget
# mainWindowLayout = QVBoxLayout(parent_widget)
# mainWindowLayout.addWidget(W1)

# # Change the temperature value
# new_temperature_value = 37
# W1.setTemperatureValue(new_temperature_value)
