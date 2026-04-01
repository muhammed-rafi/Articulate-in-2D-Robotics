import sys
import math
import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QSlider, QLabel
from PyQt5.QtCore import Qt

# ---- LINK LENGTHS (adjust if needed) ----
L1 = 1.0   # upper arm
L2 = 1.0   # lower arm

JOINTS = [
    'shoulder_pan',
    'shoulder_lift',
    'elbow_flex',
    'wrist_flex',
    'wrist_roll',
    'gripper_joint'
]

class IKController(Node):

    def __init__(self):
        super().__init__('ik_controller')
        self.pub = self.create_publisher(
            JointTrajectory,
            '/arm_controller/joint_trajectory',
            10
        )

    def solve_ik_2d(self, r, z):
        d = math.sqrt(r*r + z*z)

        if d > (L1 + L2):
            print("❌ Target out of reach!")
            return None

        cos_theta2 = (r*r + z*z - L1*L1 - L2*L2) / (2 * L1 * L2)

        # Clamp for safety
        cos_theta2 = max(min(cos_theta2, 1.0), -1.0)

        theta2 = math.acos(cos_theta2)   # elbow-down

        theta1 = math.atan2(z, r) - math.atan2(
            L2 * math.sin(theta2),
            L1 + L2 * math.cos(theta2)
        )

        return theta1, theta2

    def move_to(self, x, y, z):
        # Base rotation
        theta_pan = math.atan2(y, x)

        # Project to planar arm
        r = math.sqrt(x*x + y*y)

        result = self.solve_ik_2d(r, z)
        if result is None:
            return

        theta1, theta2 = result

        msg = JointTrajectory()
        msg.joint_names = JOINTS

        point = JointTrajectoryPoint()
        point.positions = [
            theta_pan,   # shoulder_pan ✅
            theta1,      # shoulder_lift ✅
            theta2,      # elbow_flex   ✅
            0.0,         # wrist_flex
            0.0,         # wrist_roll
            0.0          # gripper
        ]

        point.time_from_start.sec = 1
        msg.points.append(point)

        self.pub.publish(msg)


class IKGUI(QWidget):

    def __init__(self, node):
        super().__init__()
        self.node = node

        self.setWindowTitle("🔥 IK Controller (x, y, z)")

        layout = QVBoxLayout()

        # X slider
        self.x_slider = QSlider(Qt.Horizontal)
        self.x_slider.setMinimum(-200)
        self.x_slider.setMaximum(200)
        self.x_slider.setValue(100)

        # Y slider
        self.y_slider = QSlider(Qt.Horizontal)
        self.y_slider.setMinimum(-200)
        self.y_slider.setMaximum(200)
        self.y_slider.setValue(0)

        # Z slider
        self.z_slider = QSlider(Qt.Horizontal)
        self.z_slider.setMinimum(0)
        self.z_slider.setMaximum(200)
        self.z_slider.setValue(100)

        layout.addWidget(QLabel("X Position"))
        layout.addWidget(self.x_slider)

        layout.addWidget(QLabel("Y Position"))
        layout.addWidget(self.y_slider)

        layout.addWidget(QLabel("Z Position"))
        layout.addWidget(self.z_slider)

        # Connect sliders
        self.x_slider.valueChanged.connect(self.update_position)
        self.y_slider.valueChanged.connect(self.update_position)
        self.z_slider.valueChanged.connect(self.update_position)

        self.setLayout(layout)

    def update_position(self):
        x = self.x_slider.value() / 100.0
        y = self.y_slider.value() / 100.0
        z = self.z_slider.value() / 100.0

        self.node.move_to(x, y, z)


def main():
    rclpy.init()
    node = IKController()

    app = QApplication(sys.argv)
    window = IKGUI(node)
    window.show()

    from threading import Thread
    def spin():
        rclpy.spin(node)

    thread = Thread(target=spin, daemon=True)
    thread.start()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
