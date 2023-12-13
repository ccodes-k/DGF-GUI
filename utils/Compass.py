from PyQt5 import QtCore, QtGui, QtWidgets

class Compasswidget(QtWidgets.QLabel):

    def __init__(self, parent):
        super(Compasswidget, self).__init__(parent)
        self.setStyleSheet('QFrame {background-color:(239,100,100);}')
        self.resize(100, 100)
        self._angle = 0.0
        self._margins = 10
        self._pointText = {0: "N", 45: "NE", 90: "E", 135: "SE", 180: "S",
                           225: "SW", 270: "W", 315: "NW"}

    def paintEvent(self, event):
        painter = QtGui.QPainter()
        painter.begin(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setPen(QtGui.QColor(168, 34, 3))
        painter.fillRect(event.rect(), self.palette().brush(QtGui.QPalette.Window))
        self.drawMarkings(painter)
        self.drawNeedle(painter)
        self.drawCenterDot(painter)
        painter.end()

    def drawMarkings(self, painter):
        painter.save()
        painter.translate(self.width() / 2, self.height() / 2)
        scale = min((self.width() - self._margins) / 120.0,
                    (self.height() - self._margins) / 120.0)
        painter.scale(scale, scale)

        font = QtGui.QFont(self.font())
        font.setPixelSize(10)
        metrics = QtGui.QFontMetricsF(font)

        painter.setFont(font)
        painter.setPen(self.palette().color(QtGui.QPalette.Shadow))

        i = 0
        while i < 360:
            if i % 45 == 0:
                painter.drawLine(0, -40, 0, -50)
                painter.drawText(-int(metrics.width(self._pointText[i]) / 2.0), -52,
                                 self._pointText[i])
            else:
                painter.drawLine(0, -45, 0, -50)

            painter.rotate(15)
            i += 15

        painter.restore()

    def drawCenterDot(self, painter):
        painter.save()
        painter.translate(self.width() / 2, self.height() / 2)

        dot_size = 10

        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(QtGui.QColor(0, 0, 0))  # Black
        painter.drawEllipse(-dot_size // 2, -dot_size // 2, dot_size, dot_size)

        painter.restore()

    def drawNeedle(self, painter):
        painter.save()
        painter.translate(self.width() / 2, self.height() / 2)
        scale = min((self.width() - self._margins) / 120.0, (self.height() - self._margins) / 120.0)
        painter.scale(scale, scale)

        # Adjust the length of the needles
        needle_length = 50

        arrow_polygon_north = QtGui.QPolygon([
            QtCore.QPoint(0, -needle_length),  # Tip of the arrow
            QtCore.QPoint(-5, -25),
            QtCore.QPoint(-2, -25),
            QtCore.QPoint(-2, 0),
            QtCore.QPoint(2, 0),
            QtCore.QPoint(2, -25),
            QtCore.QPoint(5, -25)
        ])

        arrow_polygon_east = QtGui.QPolygon([
            QtCore.QPoint(0, needle_length),  # Tip of the arrow
            QtCore.QPoint(-5, 25),
            QtCore.QPoint(-2, 25),
            QtCore.QPoint(-2, 0),
            QtCore.QPoint(2, 0),
            QtCore.QPoint(2, 25),
            QtCore.QPoint(5, 25)
        ])

        # Draw the north arrow in green
        painter.save()
        painter.rotate(self._angle)
        painter.setPen(QtGui.QPen(QtCore.Qt.NoPen))
        painter.setBrush(QtGui.QColor(0, 255, 0))  # Green
        painter.drawPolygon(arrow_polygon_north)
        painter.restore()

        # Draw the east arrow (90 degrees clockwise) in red
        painter.save()
        painter.rotate(self._angle - 90)
        painter.setPen(QtGui.QPen(QtCore.Qt.NoPen))
        painter.setBrush(QtGui.QColor(255, 0, 0))  # Red
        painter.drawPolygon(arrow_polygon_east)
        painter.restore()

        painter.restore()

    def setAngle(self, angle):
        if angle != self._angle:
            self._angle = angle
            self.update()