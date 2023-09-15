cmake_minimum_required(VERSION 3.0.2)
project(voice_commands)

find_package(catkin REQUIRED COMPONENTS
  rospy
  std_msgs
  message_generation
)

add_service_files(
   FILES
   Dashboard.srv
)

generate_messages(
  DEPENDENCIES
  std_msgs
)
