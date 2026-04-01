
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
