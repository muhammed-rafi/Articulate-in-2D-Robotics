# 🤖 Articulate 2D Robotic Arm Control using ROS 2

This project demonstrates the simulation and control of a multi-joint robotic arm using **ROS 2 Humble**, **Gazebo (Ignition)**, and **ros2_control**. The system allows direct trajectory-based control of the arm without relying on MoveIt, ensuring a stable and lightweight workflow.

---

## 📌 Features

- 🚀 ROS 2 Humble based robotic simulation  
- 🦾 6-DOF articulated robotic arm  
- ⚙️ Integrated with `ros2_control`  
- 🎮 Direct joint trajectory control via Python  
- 🔁 Continuous multi-point trajectory execution  
- 🧪 Fully tested in Gazebo simulation  

---

## 🛠️ Tech Stack

- **ROS 2 Humble**
- **Gazebo (Ignition / gz sim)**
- **ros2_control**
- **Python (rclpy)**
- **JointTrajectoryController**

---

## 📂 Project Structure

```
articulate2d_ws/
├── src/
│   ├── articulate_2d/              # URDF, meshes, configs
│   ├── articulate_2d_moveit/       # MoveIt config (optional)
│
├── send_trajectory.py              # Python control script
```

---

## ⚙️ Setup Instructions

### 1️⃣ Install Dependencies

```bash
sudo apt update
sudo apt install ros-humble-ros-gz-sim
sudo apt install ros-humble-gz-ros2-control
```

---

### 2️⃣ Build Workspace

```bash
cd ~/Documents/Robotics/articulate2d_ws
colcon build --symlink-install
source install/setup.bash
```

---

### 3️⃣ Run Simulation

```bash
ros2 launch articulate_2d sim.launch.py
```

---

### 4️⃣ Verify Controllers

```bash
ros2 control list_controllers
```

Expected output:

```
joint_state_broadcaster → active
arm_controller → active
```

---

## 🎮 Controlling the Robot

### ▶️ Run Python Controller

```bash
python3 send_trajectory.py
```

---

### 📌 What it does:

- Sends **multiple joint trajectories**
- Executes them in a **continuous loop**
- Moves all joints simultaneously

---

## 📡 Manual Control (Optional)

You can also publish commands manually:

```bash
ros2 topic pub /arm_controller/joint_trajectory trajectory_msgs/msg/JointTrajectory "
joint_names: ['shoulder_pan','shoulder_lift','elbow_flex','wrist_flex','wrist_roll','gripper_joint']
points:
- positions: [0.5, 0.5, -1.0, 0.3, 0.2, 0.1]
  time_from_start: {sec: 2}
"
```

---

## 🧠 Key Learnings

- Importance of **controller naming consistency**  
- Correct **launch order** (Gazebo → Controllers → Control nodes)  
- Avoiding ROS environment conflicts (`.bashrc`, DDS, domain ID)  
- Using **ros2_control directly for reliable execution**  

---

## ⚠️ Troubleshooting

### ❌ No `/joint_states` or `/clock`
- Ensure Gazebo is launched via ROS (`ros_gz_sim`)

### ❌ Controller not working
- Check naming consistency across:
  - `ros2_controllers.yaml`
  - `moveit_controllers.yaml`

### ❌ ROS crashes / strange behavior
- Remove extra workspace sourcing from `.bashrc`
- Use a clean terminal

---

## 🚀 Future Improvements

- MoveIt integration for motion planning  
- Inverse Kinematics (IK) control  
- Pick and place pipeline  
- Real robot hardware deployment  

---

## ⭐ Acknowledgements

- ROS 2 Community  
- MoveIt Documentation  
- Gazebo Simulation Tools  

---

## 📜 License

This project is open-source and available for learning and research purposes.
