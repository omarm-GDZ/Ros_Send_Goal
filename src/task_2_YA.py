#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math

# Initialize global variables
current_pose = Pose()

def pose_callback(data):
    global current_pose
    current_pose = data

def move_to_goal(x_goal, y_goal):
    global current_pose

    rospy.init_node('turtle_move_to_goal', anonymous=True)
    pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    sub = rospy.Subscriber('/turtle1/pose', Pose, pose_callback)
    rate = rospy.Rate(10)

    goal_pose = Pose()
    goal_pose.x = x_goal
    goal_pose.y = y_goal

    vel_msg = Twist()

    while not rospy.is_shutdown():
        # Calculate the distance to the goal
        distance = math.sqrt((goal_pose.x - current_pose.x)*2 + (goal_pose.y - current_pose.y)*2)

        # Calculate the linear velocity (Proportional control)
        vel_msg.linear.x = 1 * distance

        # Calculate the angle to the goal
        angle_to_goal = math.atan2(goal_pose.y - current_pose.y, goal_pose.x - current_pose.x)
        angle_diff = angle_to_goal - current_pose.theta

        # Normalize the angle difference to [-pi, pi]
        angle_diff = (angle_diff + math.pi) % (2 * math.pi) - math.pi

        # Calculate the angular velocity (Proportional control)
        vel_msg.angular.z = 4.0 * angle_diff

        # Stop the turtle when it reaches the goal
        if distance < 0.01:
            vel_msg.linear.x = 0
            vel_msg.angular.z = 0
            pub.publish(vel_msg)
            break

        # Publish the velocity message
        pub.publish(vel_msg)
        rate.sleep()

if __name__ == '__main__':
    try:
        while True:
            x_goal = float(input("Enter the x goal to move (<= 11): "))
            y_goal = float(input("Enter the y goal to move (<= 11): "))

            if x_goal > 11 or y_goal > 11:
                print("Both x and y goals must be less than or equal to 11. Please try again.")
            else:
                move_to_goal(x_goal, y_goal)
                break
    except rospy.ROSInterruptException:
        pass