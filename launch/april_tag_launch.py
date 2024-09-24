'''
"ros2 run ai_deck_wrapper ai_deck_wrapper --ros-args -p period:=0.1 -r image_rect:=/cf37/image_rect -r camera_info:=/cf37/camera_info "
"ros2 run apriltag_ros apriltag_node --ros-args -r image_rect:=/cf37/image_rect -r tf:=/cf37/tf -r camera_info:=/cf37/camera_info -r detections:=/cf37/detections"
"ros2 run mission_planner mission_planner"
'''
import os

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch_ros.actions import Node

#drone_ids = ["cf01","cf08"]
#drone_ids = ["cf06","cf07","cf08","cf09","cf10","cf11"]
drone_ids = ["cf01","cf02","cf03","cf04","cf05","cf06","cf07","cf08","cf09","cf10","cf11","cf12","cf13","cf14","cf15"]
#drone_ids = ["cf04"]
#drone_ids = ["cf01"]


def generate_launch_description() -> LaunchDescription:
    nodes: list[Node] = []

    for drone_id in drone_ids:
        ai_deck_wrapper_node : Node = get_ai_deck_wrapper_node(drone_id)
        nodes.append(ai_deck_wrapper_node)

        apriltag_node : Node = get_apriltag_node(drone_id)
        nodes.append(apriltag_node)

    # MISSION PLANNER
    mission_planner_node : Node = 

    # Create the launch description and populate
    launch_description : LaunchDescription = LaunchDescription()

    for node in nodes:
        launch_description.add_action(node)

    launch_description.add_action(mission_planner_node)
    return launch_description

def get_ai_deck_wrapper_node(drone_id : str) -> Node:
    return Node(
                package='ai_deck_wrapper',
                executable='ai_deck_wrapper',
                namespace=drone_id,
                output='screen',
                parameters=[{
                    'period': 0.1,
                    'ip': f'192.168.1.1{drone_id[2:]}',
                    'name': f'{drone_id}'  
                }],
                remappings=[
                    ('/image_rect', f'/{drone_id}/image_rect'),
                    ('/camera_info', f'/{drone_id}/camera_info'),
                ])

def get_apriltag_node(drone_id: str) -> Node:
    return Node(
                package='apriltag_ros',
                executable='apriltag_node',
                namespace=f'{drone_id}',
                output='screen',
                remappings=[
                    ('/image_rect', f'/{drone_id}/image_rect'),
                    ('/camera_info', f'/{drone_id}/camera_info'),
                    ('/tf',f'/{drone_id}/tf'),
                    ('/detections',f'/{drone_id}/detections'),
                ]
                )

def get_mission_planner_node() -> Node:
    return Node(
            package='mission_planner',
            executable='mission_planner',
            output='screen',
            # parameters=[{
            #     'undetectedTags': ["tag36h11:200"]
            # }],
            )