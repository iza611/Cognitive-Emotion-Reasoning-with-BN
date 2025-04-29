Steps to run the package:
1) Dwonload the project
2) Place the downloaded folder inside directory ~/your_ws/src 
(replace 'your_ws' with the name of the desired workspace)
3) Open a terminal and run command:  cd ~/your_ws/  
4) Run command:  catkin_make
5) Run command:  roscore
6) Open new terminal window
7) Run command: roslaunch cr_week6_test human_robot_interaction.launch
8) Open new terminal window 
9) Run command: rosrun rqt_graph rqt_graph
10) You might need to refresh the rqt_graph to see all the nodes and topics
11) Open four new terminal windows
12) In the first newly opened window run command: rostopic echo /obj_info
13) In the second newly opened window run command: rostopic echo /human_info
14) In the third newly opened window run command: rostopic echo /perceived_info
15) In the fourth newly opened window run command: rostopic echo /robot_expression
