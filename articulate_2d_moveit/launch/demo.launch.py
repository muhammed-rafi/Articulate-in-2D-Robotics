# from moveit_configs_utils import MoveItConfigsBuilder
# from moveit_configs_utils.launches import generate_demo_launch


# def generate_launch_description():
#     moveit_config = MoveItConfigsBuilder("so_arm100", package_name="articulate_2d_moveit").to_moveit_configs()
#     return generate_demo_launch(moveit_config)
from launch import LaunchDescription
from launch_ros.actions import Node
import xacro
import yaml

def generate_launch_description():

    urdf_file = "/home/rafi/Documents/Robotics/articulate2d_ws/src/articulate_2d/urdf/arm.urdf.xacro"
    srdf_file = "/home/rafi/Documents/Robotics/articulate2d_ws/src/articulate_2d_moveit/config/so_arm100.srdf"

    ompl_config = yaml.safe_load(open(
        "/home/rafi/Documents/Robotics/articulate2d_ws/src/articulate_2d_moveit/config/ompl_planning.yaml"
    ))

    kinematics_config = yaml.safe_load(open(
        "/home/rafi/Documents/Robotics/articulate2d_ws/src/articulate_2d_moveit/config/kinematics.yaml"
    ))

    controllers_config = yaml.safe_load(open(
        "/home/rafi/Documents/Robotics/articulate2d_ws/src/articulate_2d_moveit/config/moveit_controllers.yaml"
    ))

    robot_description = xacro.process_file(urdf_file).toxml()
    robot_description_semantic = open(srdf_file).read()

    return LaunchDescription([

        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[
                {'robot_description': robot_description},
                {'use_sim_time': True}
            ],
            output='screen'
        ),

        Node(
            package="joint_state_publisher_gui",
            executable="joint_state_publisher_gui",
            output="screen",
        ),

        Node(
            package="moveit_ros_move_group",
            executable="move_group",
            output="screen",
            parameters=[
                {"robot_description": robot_description},
                {"robot_description_semantic": robot_description_semantic},

                {"publish_robot_description": True},
                {"publish_robot_description_semantic": True},

                {"planning_plugin": "ompl_interface/OMPLPlanner"},
                {"planning_pipelines": ["ompl"]},
                {"moveit_manage_controllers": True},
                {"start_state_max_bounds_error": 0.1},

                ompl_config,
                kinematics_config,
                {"moveit_simple_controller_manager": controllers_config},

                {"use_sim_time": True},
            ],
        ),

        Node(
            package="rviz2",
            executable="rviz2",
            output="screen",
            parameters=[{"use_sim_time": True}],
        ),
    ])

# from moveit_configs_utils import MoveItConfigsBuilder
# from moveit_configs_utils.launches import (
#     generate_move_group_launch,
#     generate_moveit_rviz_launch,
# )

# from launch import LaunchDescription


# def generate_launch_description():

#     moveit_config = (
#         MoveItConfigsBuilder("so_arm100", package_name="articulate_2d_moveit")
#         .robot_description_semantic(file_path="config/so_arm100.srdf")
#         .trajectory_execution(file_path="config/moveit_controllers.yaml")
#         .planning_pipelines(pipelines=["ompl"])
#         .robot_description_kinematics(file_path="config/kinematics.yaml")
#         .to_moveit_configs()
#     )

#     return LaunchDescription([
#         generate_move_group_launch(moveit_config),
#         generate_moveit_rviz_launch(moveit_config),
#     ])