cmake_minimum_required(VERSION 3.0.2)
project(cr_week6_test)

find_package(catkin REQUIRED COMPONENTS
  rospy
  std_msgs
  message_generation
)

################################################
## Declare ROS messages, services and actions ##
################################################

# Generate messages in the 'msg' folder
add_message_files(
  FILES
  human_info.msg
  object_info.msg
  perceived_info.msg
  robot_info.msg
)

# Generate services in the 'srv' folder
add_service_files(
  FILES
  predict_robot_expression.srv
)

# Generate added messages and services with any dependencies listed here
generate_messages(
  DEPENDENCIES
  std_msgs
)

###################################
## catkin specific configuration ##
###################################

catkin_package(
 CATKIN_DEPENDS message_runtime
)

###########
## Build ##
###########

include_directories(
# include
  ${catkin_INCLUDE_DIRS}
)

#############
## Install ##
#############

catkin_install_python(PROGRAMS
  scripts/interaction_generator.py scripts/perception_filter.py
  scripts/robot_controller.py scripts/robot_expression_prediction.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)