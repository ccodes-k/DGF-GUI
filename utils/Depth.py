# plot the graph with one horizontal line
# for Depth

import pyqtgraph as pg
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from utils.server import Talker

class OneHorlineD(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        # Label for Depth
        self.label = QLabel("Depth: ", self)
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
        self.plotWidget.setYRange(10, -30, padding=0)

        # Hide left axis
        self.plotWidget.getPlotItem().hideAxis('bottom')

        # Initialize Depth value
        self.Dv = -1.5

        # Add the initial line
        self.line = pg.InfiniteLine(self.Dv, angle=0, pen='b')
        self.plotWidget.addItem(self.line)

    def updateHorizontalLine(self):
        # Update the existing line with the current Depth value
        mDV = float(self.Dv) * -1
        self.line.setValue(mDV)

    def setDepthValue(self, server):
        # Set a new Depth value and update the vertical line
        if server.depth < 0:
           new_value = 0
        else:
            new_value = server.depth
        #Label
        self.label.setText(f"Depth: {new_value} m")
        #Graph
        self.updateHorizontalLine()

# # Example usage:
# # Create a parent widget
# parent_widget = QWidget()

# # Create an instance of OneVerlineD and pass the parent widget
# W2 = OneVerlineD(parent_widget)

# # Add the widget to the layout of the parent widget
# mainWindowLayout = QVBoxLayout(parent_widget)
# mainWindowLayout.addWidget(W2)

# # Change the Depth value
# new_Depth_value = 97.5
# W2.setDepthValue(new_Depth_value)