#!/usr/bin/env python3
import cv2
import zmq
import numpy as np
import threading
import time
import os
from pathlib import Path
import argparse
import math
import json

class Talker:
    def __init__(self,IP_addr = '169.254.163.100'):
        self.IP = IP_addr
        self.img_data = None
        self.img2_data = None
        self.got_img = False

        self.imu_data = None
        self.got_imu = False

        self.show = False


    def show_img(self):
        print("Displaying")
        while(1):
            if self.show:
                self.show = False
                cv2.imshow('left', self.img_data)
                cv2.imshow('right', self.img2_data)
                #self._out.write(self.img_data)
                #self.pub.publish(self.br.cv2_to_imgmsg(self.img_data))
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break
    
    
    def left(self):
            count = 0
            context = zmq.Context()
            socket = context.socket(zmq.REQ)
            socket.connect(f"tcp://{self.IP}:5555")
            print("Connected to",f"tcp://{self.IP}:5555")
            l = []
            while True:
                    socket.send_string('read')
                    a = time.time()
                    image = socket.recv_pyobj()['img']
                    self.img_data = cv2.imdecode(image, flags=1)
                    # cv2.imwrite("left%05d.png" % count, self.img_data)
                    # Path("left%05d.png"%count).rename("Images/left/left%05d.png"%count)
                    count += 1
                    self.show = True
                    self.got_img = True
                #     l.append(1/(time.time()-a))
                #     fps = str(1/(time.time()-a))
                #     f = open("D435i FPS.csv", "a")
                #     f.write(fps + '\n')
                    
    
    def right(self):
            count2 = 0
            context = zmq.Context()
            socket2 = context.socket(zmq.REQ)
            socket2.connect(f"tcp://{self.IP}:5556")
            print("Connected to",f"tcp://{self.IP}:5556")
            while True:
                    socket2.send_string('read2')
                    # a = time.time()
                    image = socket2.recv_pyobj()['img2']
                    self.img2_data = cv2.imdecode(image, flags=1)
                    # cv2.imwrite("right%05d.png" % count2, self.img2_data)
                    # Path("right%05d.png"%count2).rename("Images/right/right%05d.png"%count2)
                    count2 += 1
                    self.show = True
                    self.got_img = True


    def show_temp(self):
        context = zmq.Context()
        socket3 = context.socket(zmq.REQ)
        socket3.connect(f"tcp://{self.IP}:5557")
        print("Connected to",f"tcp://{self.IP}:5557")
        with open('temp.txt', 'w') as f1:
                while True:
                        print(2)
                        socket3.send_string('read3')
                        print(2)
                        self.temp = socket3.recv_string()
                        print(2)
                        print(self.temp)
                        f1.write(self.temp + '\n')
                        f1.flush()
                        time.sleep(1)

    def show_IMU(self):
        context = zmq.Context()
        socket4 = context.socket(zmq.REQ)
        socket4.connect(f"tcp://{self.IP}:5558")
        print("Connected to",f"tcp://{self.IP}:5558")
        with open('imu.txt', 'w') as f2:
                while True:
                        socket4.send_string('read4')
                        IMU = socket4.recv_string()
                        IMU = IMU.replace("'","\"") 
                        IMU = json.loads(IMU)
                        x = IMU["Orientation Data"]["Q0"]
                        y = IMU["Orientation Data"]["Q1"]
                        z = IMU["Orientation Data"]["Q2"]
                        w = IMU["Orientation Data"]["Q3"]
                        # print(x, y)
                        IMU = euler_from_quaternion(x, y, z, w)
                        self.theta = IMU[0]
                        # print(self.x, self.y)
                        self.x = 1
                        self.y = 1
                        coord_x = x*math.cos(self.theta) - y*math.sin(self.theta)
                        coord_y = x*math.sin(self.theta) + y*math.cos(self.theta)
                        new_coord = [coord_x, coord_y]
                        print(coord_x, coord_y)
                        f2.write(str(new_coord) + '\n')
                        f2.flush()

    def show_GPS(self):
        context = zmq.Context()
        socket5 = context.socket(zmq.REQ)
        socket5.connect(f"tcp://{self.IP}:5559")
        print("Connected to",f"tcp://{self.IP}:5559")
        with open('gps.txt', 'w') as f3:
                while True:
                        socket5.send_string('read5')
                        GPS = socket5.recv_string()
                        print(GPS)
                        f3.write(GPS)
                        f3.flush()

    def show_sonar(self):
        context = zmq.Context()
        socket6 = context.socket(zmq.REQ)
        socket6.connect(f"tcp://{self.IP}:5560")
        print("Connected to",f"tcp://{self.IP}:5560")
        with open('sonar.txt', 'w') as f4:
                while True:
                        socket6.send_string('read6')
                        sonar = socket6.recv_string()
                        print(sonar)
                        f4.write(sonar)
                        f4.flush()