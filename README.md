# ROS2 Rover Camera Feed

This repository currently contains the first camera-stream UI path for the rover. It is a static web UI that connects to ROS2 through `rosbridge_suite` and subscribes to image topics with `roslibjs`.

## Architecture

- The ZED camera driver publishes frames to ROS2 image topics.
- `rosbridge_suite` exposes ROS2 topics to the browser over WebSocket.
- The UI subscribes to configured image topics and renders incoming frames.
- The UI does not publish camera frames or manually call a publisher.
- Future side cameras should be added as new entries in `src/cameras.js`.

The first configured stream is:

- Label: `Front / ZED Camera`
- Compressed image topic: `/zed/zed_node/rgb/image_rect_color/compressed`
- Raw image topic: `/zed/zed_node/rgb/image_rect_color`
- Camera info topic: `/zed/zed_node/rgb/camera_info`

The raw ZED topics are the standard ROS2 ZED wrapper names. Confirm them on the rover because launch remaps can change the namespace.

## Camera Config

Camera definitions live in `src/cameras.js`:

```js
{
  id: "front-zed",
  label: "Front / ZED Camera",
  image_topic: "/zed/zed_node/rgb/image_rect_color/compressed",
  raw_image_topic: "/zed/zed_node/rgb/image_rect_color",
  camera_info_topic: "/zed/zed_node/rgb/camera_info",
  enabled: true,
  encoding: "compressed"
}
```

Use `image_topic` for the browser subscription. Use `camera_info_topic` for calibration metadata and later overlays.

## Run

Install the ZED ROS2 wrapper and rosbridge in your ROS2 workspace if they are not already available:

```bash
sudo apt install ros-${ROS_DISTRO}-rosbridge-suite
```

Launch the ZED node using your rover launch file, or directly with the ZED wrapper launch file installed on the robot. A common direct launch form is:

```bash
ros2 launch zed_wrapper zed_camera.launch.py camera_model:=zed2i
```

Adjust `camera_model` for the actual rover camera.

Confirm the image and camera info topics exist:

```bash
ros2 topic list | grep zed
ros2 topic info /zed/zed_node/rgb/image_rect_color
ros2 topic info /zed/zed_node/rgb/image_rect_color/compressed
ros2 topic echo /zed/zed_node/rgb/camera_info --once
```

If the compressed topic does not exist, enable compressed image transport for the ZED stream or update `src/cameras.js` to match the available web stream path.

Launch rosbridge:

```bash
ros2 launch rosbridge_server rosbridge_websocket_launch.xml
```

Open the UI from this repository:

```bash
python3 -m http.server 5173
```

Then open:

```text
http://localhost:5173
```

The default bridge URL is:

```text
ws://localhost:9090
```

Change it in the UI if rosbridge is running on another machine, for example `ws://ROVER_IP:9090`.

## Mock Data

No mock camera data is included. Testing should use a real ROS2 image topic or a clearly separate test publisher outside this UI path.
