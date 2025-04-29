#! usr/bin/env python

import rospy
import os
from cr_week6_test.msg import perceived_info, robot_info
from cr_week6_test.srv import predict_robot_expression

# Change the format of loginfo() to print time in readable format instead of the timestamp
os.environ['ROSCONSOLE_FORMAT'] = '[${time:%Y-%m-%d %H:%M:%S}] ${message}'

# This function is called once the message is received from the 'perceived_info' topic
def callback(data, pub):
    # It requests to compute probabilities from service 'predict_robot_expression' 
    rospy.wait_for_service('predict_robot_expression')
    try:
        service1_proxy = rospy.ServiceProxy('predict_robot_expression', predict_robot_expression)
        resp = service1_proxy(data.object_size, data.human_action, data.human_expression)

        # Once it gets the response, it logs info and publishes the results to the 'robot_expression' topic
        rospy.loginfo(f"{rospy.get_caller_id()} \nInteraction {data.id}: \nP(happy)={resp.p_happy} \nP(sad)={resp.p_sad} \nP(neutral)={resp.p_neutral}")
        pub.publish(data.id, resp.p_happy, resp.p_sad, resp.p_neutral)

    except rospy.ServiceException as e:
        rospy.logerr("Service call failed: {}".format(e))

# This function declares the node 'controller' that is subscribing to 'perceived_info' topic and publishes to the 'robot_expression' topic
def controller():
    rospy.init_node('controller')
    pub = rospy.Publisher('robot_expression', robot_info, queue_size=10)
    rospy.Subscriber('perceived_info', perceived_info, callback, pub)
    rospy.spin()

# When the script starts, controller() function is called
if __name__ == '__main__':
    controller()
