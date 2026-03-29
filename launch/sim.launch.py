from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess, TimerAction
import os
import xacro

def generate_launch_description():
    pkg_path = os.path.join(
        os.getenv('HOME'),
        'Documents/Robotics/articulate2d_ws/src/articulate_2d'
    )
    xacro_file = os.path.join(pkg_path, 'urdf', 'arm.urdf.xacro')
    robot_description = xacro.process_file(xacro_file).toxml()

    return LaunchDescription([

        # 1. robot_state_publisher FIRST — ign_ros2_control plugin
        #    calls /robot_description service at spawn time and
        #    crashes Ignition if RSP is not already running
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[{'robot_description': robot_description}],
            output='screen'
        ),

        # 2. Clock bridge — Fortress uses ignition.msgs not gz.msgs
        Node(
            package='ros_ign_bridge',
            executable='parameter_bridge',
            arguments=['/clock@rosgraph_msgs/msg/Clock[ignition.msgs.Clock'],
            output='screen'
        ),

        # 3. Ignition Fortress — starts after RSP is up
        TimerAction(
            period=2.0,
            actions=[
                ExecuteProcess(
                    cmd=['ign', 'gazebo', '-r', 'empty.sdf'],
                    output='screen'
                ),
            ]
        ),

        # 4. Spawn robot — RSP already running so plugin won't crash
        TimerAction(
            period=12.0,
            actions=[
                Node(
                    package='ros_ign_gazebo',
                    executable='create',
                    arguments=[
                        '-topic', 'robot_description',
                        '-name', 'articulate_2d',
                        '-world', 'empty',
                        '-z', '0.05'
                    ],
                    output='screen'
                ),
            ]
        ),

        # 5. joint_state_broadcaster
        TimerAction(
            period=18.0,
            actions=[
                Node(
                    package='controller_manager',
                    executable='spawner',
                    arguments=['joint_state_broadcaster'],
                    output='screen'
                ),
            ]
        ),

        # 6. arm_controller
        TimerAction(
            period=22.0,
            actions=[
                Node(
                    package='controller_manager',
                    executable='spawner',
                    arguments=['arm_controller'],
                    output='screen'
                ),
            ]
        ),
    ])