from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess
import os
import xacro
from launch.actions import TimerAction

def generate_launch_description():

    pkg_path = os.path.join(
        os.getenv('HOME'),
        'Documents/Robotics/articulate2d_ws/src/articulate_2d'
    )

    xacro_file = os.path.join(pkg_path, 'urdf', 'arm.urdf.xacro')
    robot_description = xacro.process_file(xacro_file).toxml()

    return LaunchDescription([

        # Start Gazebo
        ExecuteProcess(
            cmd=['ign', 'gazebo', '-r', 'empty.sdf'],
            output='screen'
        ),

        # Robot state publisher
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[{'robot_description': robot_description}],
            output='screen'
        ),

        # Spawn robot
        Node(
            package='ros_gz_sim',
            executable='create',
            arguments=['-topic', 'robot_description'],
            output='screen'
        ),

        Node(
            package="controller_manager",
            executable="ros2_control_node",
            parameters=[{'robot_description': robot_description}],
            output="screen"
        ),
        # Node(
        #     package="controller_manager",
        #     executable="spawner",
        #     arguments=["joint_state_broadcaster"],
        # ),

        # Node(
        #     package="controller_manager",
        #     executable="spawner",
        #     arguments=["arm_controller"],
        # ),
        TimerAction(
            period=5.0,
            actions=[
                Node(
                    package="controller_manager",
                    executable="spawner",
                    arguments=["joint_state_broadcaster"],
                    output="screen",
                ),
            ],
        ),

        TimerAction(
            period=7.0,
            actions=[
                Node(
                    package="controller_manager",
                    executable="spawner",
                    arguments=["arm_controller"],
                    output="screen",
                ),
            ],
        ),

    ])