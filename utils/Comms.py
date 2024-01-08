#initialize ethernet communication
import zmq
import math
from PyQt5 import QtCore, QtGui, QtWidgets


def getnewlatlong(x, y, theta):
    '''
        Get new coordinates with respect to diver orientation
    '''
    coord_x = x*math.cos(theta) - y*math.sin(theta)
    coord_y = x*math.sin(theta) + y*math.cos(theta)
    new_coord = [coord_x, coord_y]
    print(coord_x, coord_y)
    return new_coord


def init_socket(IP, port):
    '''
        Connect to port
        
        input:
            port number of device

        output:
            None
    '''
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect(f"tcp://{IP}:%s"% port)
    print("Connected to",f"tcp://{IP}:%s" % port)
    return socket



    
