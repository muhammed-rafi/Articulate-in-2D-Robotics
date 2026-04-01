#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint


class ArmController(Node):

    def __init__(self):
        super().__init__('arm_trajectory_publisher')

        self.publisher = self.create_publisher(
            JointTrajectory,
            '/arm_controller/joint_trajectory',
            10
        )

        # Define 5 trajectories
        self.trajectories = [
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.5, 0.5, -1.0, 0.3, 0.2, 0.1],
            [-0.5, 0.2, -0.8, 0.1, -0.2, 0.0],
            [0.3, -0.5, 0.6, -0.3, 0.4, -0.1],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        ]

        self.current_index = 0

        # Timer to send trajectory every 3 seconds
        self.timer = self.create_timer(3.0, self.send_trajectory)

    def send_trajectory(self):

        msg = JointTrajectory()

        msg.joint_names = [
            'shoulder_pan',
            'shoulder_lift',
            'elbow_flex',
            'wrist_flex',
            'wrist_roll',
            'gripper_joint'
        ]

        point = JointTrajectoryPoint()
        point.positions = self.trajectories[self.current_index]
        point.time_from_start.sec = 2

        msg.points.append(point)

        self.publisher.publish(msg)

        self.get_logger().info(f"Sent trajectory {self.current_index + 1}")

        # Move to next trajectory
        self.current_index += 1

        # Loop back after 5 trajectories
        if self.current_index >= len(self.trajectories):
            self.current_index = 0


def main(args=None):
    rclpy.init(args=args)
    node = ArmController()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
