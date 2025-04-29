#! usr/bin/env python

import rospy
import os
from cr_week6_test.msg import perceived_info, object_info, human_info
from random import randint

# Change the format of loginfo() to print time in readable format instead of the timestamp
os.environ['ROSCONSOLE_FORMAT'] = '[${time:%Y-%m-%d %H:%M:%S}] ${message}'

# Define variables where received messages will be stored
obj_msg = None
human_msg = None

# This function is called by obj_callback and human_callback when message is received from 'obj_info' or 'human_info' topic
def callback(pub):
    global obj_msg, human_msg
    # Check if both messages arrived already and if so, perform the filtering
    if obj_msg and human_msg:
        obj_size = obj_msg.object_size
        human_action = human_msg.human_action
        human_expression = human_msg.human_expression

        # Filter according to given specifications
        filter_opt = randint(1, 8)
        if(filter_opt == 1): obj_size = 0
        elif(filter_opt == 2): human_action = 0
        elif(filter_opt == 3): human_expression = 0
        elif(filter_opt == 4): obj_size, human_action = 0, 0
        elif(filter_opt == 5): obj_size, human_expression = 0, 0
        elif(filter_opt == 6): human_action, human_expression = 0, 0
        elif(filter_opt == 7): obj_size, human_action, human_expression = 0, 0, 0
        elif(filter_opt == 8): pass
    
        # Log and publish modified information
        rospy.loginfo(f"{rospy.get_caller_id()} \nInteraction {obj_msg.id}, filter option={filter_opt}: \nO={obj_size} \nHA={human_action} \nHE={human_expression}")
        pub.publish(obj_msg.id, obj_size, human_action, human_expression)

        # Reset variables
        obj_msg = None
        human_msg = None

# This function is called once the message is received from the 'obj_info' topic
# Assigns received message to the 'obj_msg' variable and calls callback() function
def obj_callback(data, pub):
    global obj_msg
    obj_msg = data
    callback(pub)

# This function is called once the message is received from the 'human_info' topic
# Assigns received message to the 'human_msg' variable and calls callback() function
def human_callback(data, pub):
    global human_msg
    human_msg = data
    callback(pub)

# This function declares the node 'filter' that is publishing 'perceived_info' topic 
# and subscribes to both 'obj_info' and 'human_info' topics
def filter():
    rospy.init_node('filter')
    pub = rospy.Publisher('perceived_info', perceived_info, queue_size=10)
    rospy.Subscriber('obj_info', object_info, obj_callback, pub)
    rospy.Subscriber('human_info', human_info, human_callback, pub)
    rospy.spin()

# When the script starts, filter() function is called
if __name__ == '__main__':
    filter()

