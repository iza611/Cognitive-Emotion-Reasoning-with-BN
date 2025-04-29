#! usr/bin/env python

import rospy
import os
from cr_week6_test.msg import object_info, human_info
from random import randint

# Change the format of loginfo() to print time in readable format instead of the timestamp
os.environ['ROSCONSOLE_FORMAT'] = '[${time:%Y-%m-%d %H:%M:%S}] ${message}'

# This function declares the node 'generator' that is publishing two topics: 'obj_info' and 'human_info'
def generator():
    rospy.init_node('generator')
    pub_obj = rospy.Publisher('obj_info', object_info, queue_size=10)
    pub_human = rospy.Publisher('human_info', human_info, queue_size=10)

    # Create 'id' variable to store interaction id
    id = 0

    # Define rate so that data generation and publication happens every 10 seconds
    rate = rospy.Rate(0.1)
    while not rospy.is_shutdown():
        # Increase 'id' by 1 in each interaction
        id += 1
        # Generate random observations
        obj_size = randint(1, 2)
        human_action = randint(1, 3)
        human_expression = randint(1, 3)

        # Log and publish generated information
        rospy.loginfo(f"{rospy.get_caller_id()} \nInteraction {id}: \nO={obj_size} \nHA={human_action} \nHE={human_expression}")
        pub_obj.publish(id, obj_size)
        pub_human.publish(id, human_action, human_expression)

        # Maintain desired rate
        rate.sleep()


# When the script starts, try running generator() function
# In case there is an expection thrown by rate.sleep(), handle it by catching the rospy.ROSInterruptException exception and pass.
if __name__ == '__main__':
    try:
        generator()
    except rospy.ROSInterruptException:
        pass