##Camera Feed Via Foxglove

#Follow the steps below to publish your camera stream via ROS2 and view it on 
#Foxglove



# 1. Install Dependencies
```bash
sudo apt update
sudo apt install ros-humble-foxglove-bridge
```

# 2. Run the Image publisher
```bash
python3 - u .\test.py 
```

# 3. Verify the your camera node is being published
Your ROS2 camera node should publish something like: /camera/camera_frame
Check topics:

```bash
ros2 topic list
```

# 3. Run Foxglove bridge
```bash
ros2 launch foxglove_bridge foxglove_bridge_launch.xml port:=8765
```

# 4. Open the Foxglove Web Application
In Foxglove:cOpen connection -> ROS2 Foxglove WebSocket -> ws://localhost:8765 -> Open

# 5. Add the Image panel, and then select your topic
ROS Topic: /camera/camera_frame

# 6. Debugging
If Foxglove connects but no image appears, try this:
```bash
ros2 topic echo /camera/image_raw --once
```
If that prints image data, ROS is publishing correctly. Sometimes restarting the
Foxglove Connection helps too (basically restablish the connection on the webapp)
