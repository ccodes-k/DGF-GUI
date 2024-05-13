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
import socket
import warnings
import subprocess

try:
        from utils.Comms import getnewlatlong, init_socket
except:
       from Comms import getnewlatlong, init_socket

try:
       import rospy
       from sensor_msgs.msg import Image
       from cv_bridge import CvBridge
       from geometry_msgs.msg import PoseStamped
       from std_msgs.msg import Bool
       import signal
except Exception as e:
       warnings.warn(f"ROSPY not imported!!.... Error: {e}")

class ROS_Talker:
        def __init__(self) -> None:
                rospy.init_node("Stereo_py.node")
                rospy.loginfo("It has started ")

                self.publ = rospy.Publisher("/camera/left/image_raw",Image,queue_size=10)
                self.pubr = rospy.Publisher("/camera/right/image_raw",Image,queue_size=10)
                
                self.rate = rospy.Rate(20)
                self.br = CvBridge()

                self.pause = False

                signal.signal(signal.SIGINT, self.signal_handler)

        def pub_img(self, talker):
                while(talker.play):
                        if talker.show and not self.pause:
                                talker.show = False
                                self.publ.publish(self.br.cv2_to_imgmsg(talker.img_data))
                                self.pubr.publish(self.br.cv2_to_imgmsg(talker.img2_data))



        def signal_handler(self, sig, frame):
                print("Ctrl+C pressed. Terminating...")
                cv2.destroyAllWindows()
                rospy.signal_shutdown("Ctrl+C pressed")



class Talker:
    def __init__(self,IP_addr = '169.254.163.100',use_ros=False):
        self.IP = IP_addr
        self.img_data = None
        self.img2_data = None
        self.got_img = False

        self.show = False
        self.HR = 0
        self.SpO2 = 0
        self.temp = 0
        self.depth = 0
        self.Lat = 0
        self.LatD = 0
        self.Long =  0
        self.LongD = 0
        self.deg = 0
        self.x = 0
        self.y = 0

        self.use_ros = use_ros

        self.play = True

        self.slam_SS = "Null"
        self.slam_PP = True

        if self.use_ros:
               self.ros_talker = ROS_Talker()



    def show_img(self):
        '''
                Displaying camera feed
        '''
        print("Displaying")
        while(1):
            if self.show and self.showl:
                self.show = False
                self.showl = True
                # cv2.imshow('left', self.img_data)
                # cv2.imshow('right', self.img2_data)
                #self._out.write(self.img_data)
                #self.pub.publish(self.br.cv2_to_imgmsg(self.img_data))
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break

        
    def pub_img(self):
        if not self.use_ros:
              warnings.warn("ROS Library not found!")
              return
        self.ros_talker.pub_img(self)
                

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
                    cv2.imwrite("left%05d.png" % count, self.img_data)
                    Path("left%05d.png"%count).rename("Images/left/left%05d.png"%count)
                    count += 1
                    self.showl = True
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
                    cv2.imwrite("right%05d.png" % count2, self.img2_data)
                    Path("right%05d.png"%count2).rename("Images/right/right%05d.png"%count2)
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


    def show_GPS(self):
        '''
                Communication with GPS

                input:
                        port = port number of GPS

                output:
                        None
        '''
        HOST = '192.168.0.100'

        PORT = 65432

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind((HOST, PORT))
                s.listen()
                print("Server created")
                conn, addr = s.accept()
                with conn:
                        print(f"Connected by {addr}")
                        while True:
                                data = conn.recv(1024)
                                data = data.decode('utf-8')
                                data = data.replace("'","\"")
                                l_str = json.loads(data)
                                self.Lat = float(l_str[0][0:2]) # Lat
                                self.x = float(l_str[0][2:-1])
                                self.LatD = l_str[1] # Lat direction
                                self.Long = float(l_str[2][0:3]) # Long
                                self.y = float(l_str[2][3:-1])
                                self.LongD = l_str[3] # Long direction
                                self.deg = float(l_str[4]) # Direction, Ground heading (take true north as the reference datum, clockwise)
                                if not data:
                                        continue

    def show_depth(self, port='5560'):
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
                recv = socket6.recv_string()
                recv = recv.split(":")
                self.depth = float(recv[1])
                print(float(recv[1]), "m")
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

    def start_slam(self):
        '''
        Start SLAM
        '''
        self.slam_SS = "start"
        # Check if a previous process is running and terminate it
        if hasattr(self, 'ros_process') and self.ros_process is not None and self.ros_process.poll() is None:
            self.ros_process.terminate()
            self.ros_process.wait()

        # Start a new SLAM process
        self.ros_process = subprocess.Popen(["roslaunch", "orb_slam3_ros", "euroc_stereo.launch"])
    
    def stop_slam(self):
        '''
        Stop SLAM
        '''
        self.slam_SS = "stop"
        # Check if a process is running and terminate it
        if hasattr(self, 'ros_process') and self.ros_process is not None and self.ros_process.poll() is None:
            self.ros_process.terminate()
            self.ros_process.wait()


    def pause_slam(self):
           '''
                Pause SLAM
           '''
        
           self.slam_PP = not self.slam_PP
           self.pause_state = not self.pause_state

           print("out_Pause = " + str(self.pause_state))
           
           if self.use_ros and self.ros_talker:
                self.ros_talker.set_pause_state(self.pause_state)
                print("in_Pause = " + str(self.pause_state))
           else: 
                  warnings.warn("NO ROS FOUND!")

def Runner(image = False, temperature = False, GPS=False, depth=False, heartrate=False):
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
                
        if GPS:
                t6 = threading.Thread(target=Talker_helper.show_GPS)
                threads.append(t6)

        if depth:
                t7 = threading.Thread(target=Talker_helper.show_depth)
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
        parser.add_argument("-g", "--GPS", action="store_true")
        parser.add_argument("-d", "--depth", action="store_true")
        parser.add_argument("-hr", "--heartrate", action="store_true")
        parser.add_argument("-ros", "--UseROS", action="store_true")
        args = parser.parse_args()

        # print(args)
        

        # Set use_ros to True to initialize ROS publisher
        Talker_helper = Talker(IP_addr='169.254.203.72',use_ros=args.UseROS)
        
        threads = []

        if args.image:
                t1 = threading.Thread(target=Talker_helper.left)
                t2 = threading.Thread(target=Talker_helper.right)
                t3 = threading.Thread(target=Talker_helper.show_img)
                threads.append(t1)
                threads.append(t2)
                threads.append(t3)
                if args.UseROS:
                        t9 = threading.Thread(target=Talker_helper.pub_img)
                        threads.append(t9)

        if args.temperature:
               t4 = threading.Thread(target=Talker_helper.show_temp)
               threads.append(t4)
                
        if args.GPS:
                t6 = threading.Thread(target=Talker_helper.show_GPS)
                threads.append(t6)

        if args.depth:
                t7 = threading.Thread(target=Talker_helper.show_depth)
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
        # t6 = threading.Thread(target=Talker_helper.show_GPS)
        # t7 = threading.Thread(target=Talker_helper.show_sonar)

        # t1.start()
        # t2.start()
        # t3.start()
        # t4.start()
        # t5.start()
        # t6.start()
        # t7.start()