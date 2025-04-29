#! usr/bin/env python

import rospy
from cr_week6_test.srv import predict_robot_expression
import os

# Change the format of loginfo() to print time in readable format instead of the timestamp
os.environ['ROSCONSOLE_FORMAT'] = '[${time:%Y-%m-%d %H:%M:%S}] ${message}'

# This function is called when there is a request message to service 'predict_robot_expression'
def handle_inference(req):
    # Create Conditional Probability Table as a dictionary according to specifications
    CPT = {
        # (HE, HA, O): (p_happy, p_sad, p_neutral)
        (1, 1, 1): (0.8, 0.2, 0.0),
        (1, 1, 2): (1.0, 0.0, 0.0),
        (1, 2, 1): (0.8, 0.2, 0.0),
        (1, 2, 2): (1.0, 0.0, 0.0),
        (1, 3, 1): (0.6, 0.2, 0.2),
        (1, 3, 2): (0.8, 0.2, 0.0),
        (2, 1, 1): (0.0, 0.0, 1.0),
        (2, 1, 2): (0.0, 0.0, 1.0),
        (2, 2, 1): (0.0, 0.1, 0.9),
        (2, 2, 2): (0.1, 0.1, 0.8),
        (2, 3, 1): (0.0, 0.2, 0.8),
        (2, 3, 2): (0.2, 0.2, 0.6),
        (3, 1, 1): (0.7, 0.3, 0.0),
        (3, 1, 2): (0.8, 0.2, 0.0),
        (3, 2, 1): (0.8, 0.2, 0.0),
        (3, 2, 2): (0.9, 0.1, 0.0),
        (3, 3, 1): (0.6, 0.2, 0.2),
        (3, 3, 2): (0.7, 0.2, 0.1),
    }

    HE, HA, O = [req.human_expression], [req.human_action], [req.object_size]

    # If no value was perceived during interaction for given event HE, HA or O, then all possible values for 
    # that observation will be looked up in the CPT
    if HE == [0]: HE = [1, 2, 3]
    if HA == [0]: HA = [1, 2, 3]
    if O == [0]: O = [1, 2]

    """
    Find all values from the dictionary that correspond to the observations

    Examples:
        1) HE = 2 ; HA = 3 ; O = 0      
        matching_vales = [(0.0, 0.2, 0.8), (0.2, 0.2, 0.6)]

        2) HE = 1 ; HA = 1 ; O = 1
        matching_values = [(0.8, 0.2, 0.0)]
    """
    matching_vales = [value for key, value in CPT.items() if key[0] in HE and key[1] in HA and key[2] in O]

    # Calculate probability of each robot expression by calculating the average of matching_values
    # Calculations can be simplified thanks to the fact that HE, HA and O have uniform disctribution of possible events.
    p_happy, p_sad, p_neutral = [sum(x)/len(matching_vales) for x in zip(*matching_vales)]

    # Log and response the obtained probabilities
    rospy.loginfo(f"{rospy.get_caller_id()} \nP(happy)={p_happy} \nP(sad)={p_sad} \nP(neutral)={p_neutral}")
    return p_happy, p_sad, p_neutral

# This function declares the node 'predictor' that advertises the service 'predict_robot_expression'
def predictor():
    rospy.init_node('predictor')
    s = rospy.Service('predict_robot_expression', predict_robot_expression, handle_inference)
    rospy.loginfo("Service ready to infer likelihoods.")
    rospy.spin()

# When the script starts, predictor() function is called
if __name__ == '__main__':
    predictor()
