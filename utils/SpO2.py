# plot the graph with one vertical line
# for SPO2

import pyqtgraph as pg
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from utils.server import Talker

class OneVerlineO(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        # Label for SpO2
        self.label = QLabel("SpO2: ", self)
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
        self.plotWidget.setXRange(90, 100, padding=0)

        # Hide left axis
        self.plotWidget.getPlotItem().hideAxis('left')

        # Initialize SpO2 value
        self.Ov = 98.5

        # Add the initial line
        self.line = pg.InfiniteLine(self.Ov, pen='b')
        self.plotWidget.addItem(self.line)

    def updateVerticalLine(self):
        # Update the existing line with the current SpO2 value
        self.line.setValue(self.Ov)

    def setSpO2Value(self, server):
        # Set a new SpO2 value and update the vertical line
        if server is None:
           new_value = 0
        else: 
            new_value = server.SpO2
        #Label
        self.label.setText(f"SpO2: {new_value} %")
        #Graph
        self.updateVerticalLine()

# # Example usage:
# # Create a parent widget
# parent_widget = QWidget()

# # Create an instance of OneVerlineO and pass the parent widget
# W2 = OneVerlineO(parent_widget)

# # Add the widget to the layout of the parent widget
# mainWindowLayout = QVBoxLayout(parent_widget)
# mainWindowLayout.addWidget(W2)

# # Change the SpO2 value
# new_SpO2_value = 97.5
# W2.setSpO2Value(new_SpO2_value)