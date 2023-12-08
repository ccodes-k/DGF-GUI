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

# converting quarternion data from IMU to euler
def euler_from_quaternion(x, y, z, w):
        """
        Convert a quaternion into euler angles (roll, pitch, yaw)
        roll is rotation around x in radians (counterclockwise)
        pitch is rotation around y in radians (counterclockwise)
        yaw is rotation around z in radians (counterclockwise)
        """
        t0 = +2.0 * (w * x + y * z)
        t1 = +1.0 - 2.0 * (x * x + y * y)
        roll_x = math.atan2(t0, t1)
     
        t2 = +2.0 * (w * y - z * x)
        t2 = +1.0 if t2 > +1.0 else t2
        t2 = -1.0 if t2 < -1.0 else t2
        pitch_y = math.asin(t2)
     
        t3 = +2.0 * (w * z + x * y)
        t4 = +1.0 - 2.0 * (y * y + z * z)
        yaw_z = math.atan2(t3, t4)
     
        return roll_x, pitch_y, yaw_z # in radians

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
    
    # start communication through ethernet
    def communication_starter():
        if "-im" == True:
                t1 = threading.Thread(target=Talker_helper.left)
                t2 = threading.Thread(target=Talker_helper.right)
                t3 = threading.Thread(target=Talker_helper.show_img)

        if "-t" == True:
                t4 = threading.Thread(target=Talker_helper.show_temp)

        if "-i" == True:
                t5 = threading.Thread(target=Talker_helper.show_IMU)
        
        if "-g" == True:
               t6 = threading.Thread(target=Talker_helper.show_GPS)
        
        if "-s" == True:
                t7 = threading.Thread(target=Talker_helper.show_sonar)


if __name__ == "__main__":

        parser = argparse.ArgumentParser()
        parser.add_argument("-im", "--image", action="store_true")
        parser.add_argument("-t", "--temperature", action="store_true")
        parser.add_argument("-i", "--IMU", action="store_true")
        parser.add_argument("-g", "--GPS", action="store_true")
        parser.add_argument("-s", "--sonar", action="store_true")
        args = parser.parse_args()

        # print(args)

        Talker_helper = Talker(IP_addr='169.254.203.72')
        
        threads = []

        if args.image:
                t1 = threading.Thread(target=Talker_helper.left)
                t2 = threading.Thread(target=Talker_helper.right)
                t3 = threading.Thread(target=Talker_helper.show_img)
                threads.append(t1)
                threads.append(t2)
                threads.append(t3)

        if args.temperature:
               t4 = threading.Thread(target=Talker_helper.show_temp)
               threads.append(t4)

        if args.IMU:
                t5 = threading.Thread(target=Talker_helper.show_IMU)
                threads.append(t5)
                
        if args.GPS:
                t6 = threading.Thread(target=Talker_helper.show_GPS)
                threads.append(t6)

        if args.sonar:
                t7 = threading.Thread(target=Talker_helper.show_sonar)
                threads.append(t7)

        for i in threads:
              i.start()

        # for i in threads:
        #       i.join()
        

        # Talker_helper = Talker(IP_addr='169.254.203.72')
        # t1 = threading.Thread(target=Talker_helper.left)
        # t2 = threading.Thread(target=Talker_helper.right)
        # t3 = threading.Thread(target=Talker_helper.show_img)
        # t4 = threading.Thread(target=Talker_helper.show_temp)
        # t5 = threading.Thread(target=Talker_helper.show_IMU)
        # t6 = threading.Thread(target=Talker_helper.show_GPS)
        # t7 = threading.Thread(target=Talker_helper.show_sonar)

        # t1.start()
        # t2.start()
        # t3.start()
        # t4.start()
        # t5.start()
        # t6.start()
        # t7.start()