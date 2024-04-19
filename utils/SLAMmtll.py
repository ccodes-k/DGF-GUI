#!/usr/bin/env python3
import rospy
import sys
from geometry_msgs.msg import PoseStamped

def write(x, y):
    with open('/home/rp123/abc_GUI/Deep-Water-Diver-Tracker/assets/ReadFiles/txty.txt', 'w') as file:
        file.write(f'{x} {y}')

def callback(data):
    # Extract translation coordinates from the PoseStamped message
    x = data.pose.position.x
    y = data.pose.position.y

    tx = x  # Appends second column
    ty = y  # Appends third column
    
    write(tx, ty)

def listener():
    rospy.init_node('camera_pose_listener', anonymous=True)
    
    # Subscribe to the camera pose topic
    rospy.Subscriber('/orb_slam3/camera_pose', PoseStamped, callback)

    try:
        while not rospy.is_shutdown():
            # Check for keyboard input
            print("Press 's' to stop the program:")
            user_input = input("Input: ")
            if user_input == "s":
                print("Program stopped by user.")
                break
            
            rospy.sleep(0.1)  # Sleep for a short duration to avoid busy loop
            
    except rospy.ROSInterruptException:
        pass

if __name__ == '__main__':
    listener()
