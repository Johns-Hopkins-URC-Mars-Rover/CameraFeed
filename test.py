import cv2
import rclpy
from camera_feed_publisher import CameraFeedPublisher

rclpy.init()
publisher = CameraFeedPublisher()
USB_CAMERA_PORTS = {
    0: 0,
    1: 2
}
cameras = {}

def open_configured_cameras():
    """
    Opens the configured USB cameras and stores the capture objects.

    The dictionary maps our logical camera number to the OpenCV device index:
    camera0 -> /camera0/image_raw
    camera1 -> /camera1/image_raw
    camera2 -> /camera2/image_raw
    camera3 -> /camera3/image_raw
    """
    for camera_number, port in USB_CAMERA_PORTS.items():
        cap = cv2.VideoCapture(port)
        if not cap.isOpened():
            pass
        cameras[cap] = camera_number

def capture_frame(cap):
    """
    Captures a single frame from the camera and returns it.

    Reads one frame from the provided capture object and returns the
    image exactly as received from OpenCV.

    Args:
        cap: An open cv2.VideoCapture object for the camera.

    Returns:
        np.ndarray: The captured image as a BGR numpy array.

    Raises:
        RuntimeError: If the frame could not be read.
    """
    if (not cap): print("Not a valid camera object")
    ret, frame = cap.read()
    if not ret:
        raise RuntimeError("Failed to capture frame from camera.")
    return frame


def release_camera(cap):
    """
    Releases the camera and closes any OpenCV windows.

    Args:
        cap: The cv2.VideoCapture object to release.
    """
    cap.release()
    cv2.destroyAllWindows()


def send_frame(frame, port):
    """
    Publishes a frame and processes pending ROS 2 work once.

    Args:
        frame: The image frame to send to the publisher.
        port: The camera port associated with the frame.
    """
    publisher.send_frame(frame, port)
    rclpy.spin_once(publisher, timeout_sec=0.1)

try:
    open_configured_cameras()

    if (cameras):
        pass
    else:
        raise RuntimeError("No camera were deteced")


    while True:
        for cap, port in cameras.items():
            image = capture_frame(cap)
            send_frame(image, port)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

finally:
    for cap in cameras:
        release_camera(cap)
    publisher.destroy_node()
    rclpy.shutdown()
