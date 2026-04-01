import sys
import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QSlider, QLabel
from PyQt5.QtCore import Qt

JOINTS = [
    'shoulder_pan',
    'shoulder_lift',
    'elbow_flex',
    'wrist_flex',
    'wrist_roll',
    'gripper_joint'
]

class ArmGUI(Node):

    def __init__(self):
        super().__init__('arm_gui')
        self.pub = self.create_publisher(
            JointTrajectory,
            '/arm_controller/joint_trajectory',
            10
        )
        self.positions = [0.0] * len(JOINTS)

    def publish_command(self):
        msg = JointTrajectory()
        msg.joint_names = JOINTS

        point = JointTrajectoryPoint()
        point.positions = self.positions
        point.time_from_start.sec = 1

        msg.points.append(point)
        self.pub.publish(msg)


class SliderWindow(QWidget):

    def __init__(self, ros_node):
        super().__init__()
        self.node = ros_node
        self.setWindowTitle("2D Arm Controller")

        layout = QVBoxLayout()

        self.sliders = []

        for i, joint in enumerate(JOINTS):
            label = QLabel(joint)
            slider = QSlider(Qt.Horizontal)

            slider.setMinimum(-314)
            slider.setMaximum(314)
            slider.setValue(0)

            slider.valueChanged.connect(self.make_callback(i))

            layout.addWidget(label)
            layout.addWidget(slider)

            self.sliders.append(slider)

        self.setLayout(layout)

    def make_callback(self, index):
        def update(value):
            self.node.positions[index] = value / 100.0
            self.node.publish_command()
        return update


def main():
    rclpy.init()
    node = ArmGUI()

    app = QApplication(sys.argv)
    window = SliderWindow(node)
    window.show()

    # Spin ROS in background
    from threading import Thread
    def spin():
        rclpy.spin(node)

    thread = Thread(target=spin, daemon=True)
    thread.start()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
