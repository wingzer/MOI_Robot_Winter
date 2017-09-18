#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
from geometry_msgs.msg import Twist, Point, Quaternion,PoseStamped
from sensor_msgs.msg import LaserScan
from math import radians, copysign, sqrt, pow, pi,cos
from nav_msgs.msg import Path
import PyKDL
import tf
import math
import PathFilter

NewPath=False
isForwardObstacle=False
POSES=[]
FrameID=""
def PathCallback(path):
		global POSES
		global FrameID
		global NewPath
		newpath=PathFilter.newPathFromAStar(path)
		
		#两次滤波对路径进行规整
		newpath=PathFilter.Lvbo(newpath,0.5)
		newpath=PathFilter.Lvbo(newpath,0.8)
		#mPath2.publish(newpath)
		newpath=PathFilter.Lvbo(newpath,1.0)
		#最后的滤波　选择长距离点
		newpath=PathFilter.ChooseMainPath(newpath)
		mPath.publish(newpath)	
		
		poses=newpath.poses
		FrameID=newpath.header.frame_id
		POSES=poses[:]
		NewPath=True
rospy.init_node('pathlistener', anonymous=False)
rospy.Subscriber('/planner/planner/plan',Path,PathCallback)
mPath=rospy.Publisher('/mplannerplan',Path,queue_size=5)
mLocalGoal=rospy.Publisher('/globalGoal',PoseStamped,queue_size=5)
rate=rospy.Rate(1)
if __name__ == '__main__':
	while not rospy.is_shutdown():
		if NewPath:
			localGoal=PoseStamped()
			localGoal.header.frame_id=FrameID
			localGoal.pose=POSES[1].pose
			mLocalGoal.publish(localGoal)
		rate.sleep()

	
