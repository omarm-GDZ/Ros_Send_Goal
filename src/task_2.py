#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math
current_pose=Pose()
def call_back(data):
    global current_pose
    current_pose = data
    
def move_to_goal(x,y):
    rospy.init_node('move_to_goal',anonymous=True)
    pub=rospy.Publisher('/turtle1/cmd_vel',Twist,queue_size=10)
    rospy.Subscriber('/turtle1/pose',Pose,call_back)
    rate=rospy.Rate(10)
    goal_pose=Pose()
    goal_pose.x=x
    goal_pose.y=y
    vel_msg=Twist()
    
    while not rospy.is_shutdown():
             
        D=math.sqrt(math.pow(goal_pose.x-current_pose.x,2)+math.pow(goal_pose.y-current_pose.y,2))
        vel_msg.linear.x=1.5*D
        angle_to_goal=math.atan2((goal_pose.y-current_pose.y),(goal_pose.x-current_pose.x))
        angle_diff=angle_to_goal-current_pose.theta
        vel_msg.angular.z=4*angle_diff
        if D<0.01:
            vel_msg.linear.x=0
            vel_msg.angular=0
            pub.publish(vel_msg)
            break
        pub.publish(vel_msg)
        rate.sleep() 
        
if __name__=='__main__':
    rospy.loginfo("xxx")
    x=float(input("Enter x coordinates (<11): "))
    y=float(input("Enter y coordinates (<11): "))
    move_to_goal(x,y) 