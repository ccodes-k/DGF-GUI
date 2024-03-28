#!/usr/bin/env python3
import re
import time
import rospy
from geometry_msgs.msg import PoseStamped
import time

def write(x, y):
    with open('/assets/ReadFiles/tx_ty.txt', 'w') as file:
        file.write(f'{x} {y}')

def callback(data):
    # Extract translation coordinates from the PoseStamped message
    x = data.pose.position.x
    y = data.pose.position.y

# Indexes are corrected below
    tx = x # Appends second column
    ty = y  # Appends third column
    
    write(tx, ty)

def listener():
    rospy.init_node('camera_pose_listener', anonymous=True)
    
    # Subscribe to the camera pose topic
    rospy.Subscriber('/orb_slam3/camera_pose', PoseStamped, callback)

    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Script terminated by user.")

if __name__ == '__main__':
    listener()


