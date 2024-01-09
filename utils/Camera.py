#Displaying camera in GUI
from PyQt5 import QtCore, QtGui, QtWidgets
from utils.server import Talker

class Camera_img():
    
    def updateimg(self,server):
        left = server.img_data
        right = server.img2_data