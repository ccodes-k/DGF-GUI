#communication with raspberry pi
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

try:
        from utils.Comms import getnewlatlong, init_socket
except:
       from Comms import getnewlatlong, init_socket


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
        self.HR = 0
        self.SpO2 = 0
        self.temp = 0


    def show_img(self):
        '''
                Displaying camera feed
        '''
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


    def left(self,port='5555'):
            '''
                Communication with left camera 

                input: 
                        port = Port number of the left camera

                output: 
                        None
            '''
            count = 0
            socket = init_socket(self.IP, port)
            l=[]
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
                    
    
    def right(self, port='5556'):
            '''
                Communication with right camera 

                input: 
                        port = Port number of the right camera

                output: 
                        None
            '''
            count2 = 0
            socket2 = init_socket(self.IP, port)
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


    def show_temp(self, port='5557'):
        '''
                Communication with temperature sensor

                input:
                        port = port number of temperature sensor

                output:
                        None
        '''
        socket3 = init_socket(self.IP, port)
        while True:
                socket3.send_string('read3')
                temp = socket3.recv_string()
                temp = temp.split(":")
                self.temp = int(float(temp[1]))
                # print(temp)

    def show_IMU(self, port='5558'):
        '''
        Communication with IMU

        input:
                port = port number of IMU

        output:
                None
        '''
        socket4 = init_socket(self.IP, port)
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
                        new_coord = getnewlatlong(self.x, self.y, self.theta)
                        f2.write(str(new_coord) + '\n')
                        f2.flush()

    def show_GPS(self, port='5559'):
        '''
                Communication with GPS

                input:
                        port = port number of GPS

                output:
                        None
        '''
        socket5 = init_socket(self.IP, port)
        while True:
                socket5.send_string('read5')
                GPS = socket5.recv_string()
                print(GPS)

    def show_sonar(self, port='5560'):
        '''
                Communication with sonar

                input:
                        port = port number of sonar

                output:
                        None
        '''
        socket6 = init_socket(self.IP, port)
        while True:
                socket6.send_string('read6')
                sonar = socket6.recv_string()
                # print(sonar)

    def show_HR(self, port='5561'):
        '''
                Communication with Heart rate sensor

                input:
                        port = port number of HR sensor

                output:
                        None
        '''
        # global HR
        socket7 = init_socket(self.IP, port)
        while True:
                socket7.send_string('read7')
                data = socket7.recv_string()
                data = data.split(";")
                data[0] = data[0].split(":")
                data[1] = data[1].split(":")
                self.HR = int(float(data[0][1]))
                self.SpO2 = int(float(data[1][1]))


def Runner(image = False, temperature = False, IMU=False, GPS=False, sonar=False, heartrate=False):
        Talker_helper = Talker(IP_addr='169.254.211.41')
        
        threads = []

        if image:
                t1 = threading.Thread(target=Talker_helper.left)
                t2 = threading.Thread(target=Talker_helper.right)
                t3 = threading.Thread(target=Talker_helper.show_img)
                threads.append(t1)
                threads.append(t2)
                threads.append(t3)

        if temperature:
               t4 = threading.Thread(target=Talker_helper.show_temp)
               threads.append(t4)

        if IMU:
                t5 = threading.Thread(target=Talker_helper.show_IMU)
                threads.append(t5)
                
        if GPS:
                t6 = threading.Thread(target=Talker_helper.show_GPS)
                threads.append(t6)

        if sonar:
                t7 = threading.Thread(target=Talker_helper.show_sonar)
                threads.append(t7)

        if heartrate:
                t8 = threading.Thread(target=Talker_helper.show_HR)
                threads.append(t8)

        for i in threads:
              i.start()

        return Talker_helper, threads

             

if __name__ == "__main__":
        '''
                Setting arguments and link the threads
        '''
        parser = argparse.ArgumentParser()
        parser.add_argument("-im", "--image", action="store_true")
        parser.add_argument("-t", "--temperature", action="store_true")
        parser.add_argument("-i", "--IMU", action="store_true")
        parser.add_argument("-g", "--GPS", action="store_true")
        parser.add_argument("-s", "--sonar", action="store_true")
        parser.add_argument("-hr", "--heartrate", action="store_true")
        args = parser.parse_args()

        # print(args)

        Talker_helper = Talker(IP_addr='169.254.211.41')
        
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

        if args.heartrate:
                t8 = threading.Thread(target=Talker_helper.show_HR)
                threads.append(t8)

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