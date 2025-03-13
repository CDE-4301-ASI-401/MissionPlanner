'''
"ros2 run ai_deck_wrapper ai_deck_wrapper --ros-args -p period:=0.1 -r image_rect:=/cf37/image_rect -r camera_info:=/cf37/camera_info "
"ros2 run apriltag_ros apriltag_node --ros-args -r image_rect:=/cf37/image_rect -r tf:=/cf37/tf -r camera_info:=/cf37/camera_info -r detections:=/cf37/detections"
"ros2 run mission_planner mission_planner"
'''
import os

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch_ros.actions import Node

# drone_ids = ["cf02","cf03","cf04","cf05",
# "cf06","cf07","cf08","cf09","cf10",
# "cf11","cf12","cf13","cf14","cf15",
# "cf16","cf18","cf19","cf20"]
# drone_ids = ["cf19"]
# drone_ids = ["cf11","cf12","cf14","cf17","cf20"]
# drone_ids = ["cf10","cf11","cf12","cf13","cf14", "cf15", "cf18","cf20"]
# drone_ids = ["cf16","cf37","cf18","cf19"]
drone_ids = ["cf01","cf02","cf33","cf11","cf20"]
# drone_ids = ["cf10",
# "cf11","cf12","cf13","cf14","cf15",
# "cf17","cf20"]


def generate_launch_description():
    nodes = []
    for i in drone_ids:
        namespace = i
        ai_deck_wrapper = Node(
                package='ai_deck_wrapper',
                executable='ai_deck_wrapper',
                namespace=namespace,
                output='screen',
                parameters=[{
                    'period': 0.1,  
                    'ip': f'192.168.50.1{namespace[2:]}',
                    # 'ip': f'192.168.10.149',
                    # 'ip': f'192.168.50.120',
                    'name': f'{namespace}'  
                }],
                remappings=[
                    ('/image_rect', f'/{namespace}/image_rect'),
                    ('/camera_info', f'/{namespace}/camera_info'),
                ])
        nodes.append(ai_deck_wrapper)
        apriltag_node = Node(
                package='apriltag_ros',
                executable='apriltag_node',
                namespace=f'{namespace}',
                output='screen',
                remappings=[
                    ('/image_rect', f'/{namespace}/image_rect'),
                    ('/camera_info', f'/{namespace}/camera_info'),
                    ('/tf',f'/{namespace}/tf'),
                    ('/detections',f'/{namespace}/detections'),
                ]
                )
        nodes.append(apriltag_node)

    # MISSION PLANNER
    mission_planner = Node(
            package='mission_planner',
            executable='mission_planner',
            output='screen',
            # parameters=[{
            #     'undetectedTags': ["tag36h11:200"]
            # }],
            )

    # Create the launch description and populate
    ld = LaunchDescription()

    for i in nodes:
        ld.add_action(i)
    ld.add_action(mission_planner)

    return ld
