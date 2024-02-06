# plot the wave graph
# for Heart Rate

import pyqtgraph as pg
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from utils.server1 import Talker
import time 

class WaveHR(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        # Label for HR
        self.label = QLabel("Heart Rate: ", self)
        self.label.setFont(QFont("Segoe UI", 12))
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        # Create a PlotWidget for Heart Rate waveform
        self.plotWidget = pg.PlotWidget(self)
        layout.addWidget(self.plotWidget)

        # Ratio of size
        layout.setStretch(0, 1)
        layout.setStretch(1, 7)

        self.customizePlotWidget()

    def customizePlotWidget(self):
        # Set background color
        self.plotWidget.setBackground("default")

        # Hide bottom axis
        self.plotWidget.getPlotItem().hideAxis("bottom")

        # Initialize empty lists with a fixed buffer size of 100
        self.buffer_size = 100
        self.x1 = list(range(-self.buffer_size + 1, 1))
        self.y1 = [0] * self.buffer_size

        # Create a red waveform
        pen = pg.mkPen(color=(255, 0, 0))
        self.data_line = self.plotWidget.plot(self.x1, self.y1, pen=pen)

    def updateWaveHR(self,server):
        if server is None:
           new_value = 0
        else:
            new_value = server.HR

        # Label
        self.label.setText(f"Heart Rate: {new_value} BPM")

        # Graph
        self.x1 = self.x1[1:]
        self.x1.append(self.x1[-1] + 1)
        self.y1 = self.y1[1:]
        self.y1.append(int(new_value))
        
        # Update the data of the plotted waveform
        self.data_line.setData(self.x1, self.y1)
        
        # Adjust the y-axis range of the plot widget to focus on the latest heart rate value
        self.plotWidget.setYRange(min(self.y1) - 5, max(self.y1) + 5, padding=0)

# Example usage:
# parent_widget = QWidget()
# wave_hr_widget = WaveHR(parent_widget)
# main_layout = QVBoxLayout(parent_widget)
# main_layout.addWidget(wave_hr_widget)
# new_value = 100
# wave_hr_widget.updateWaveHR(new_value)  # Call this method to update the waveform
