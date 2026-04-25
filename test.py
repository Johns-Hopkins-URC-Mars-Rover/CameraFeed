import cv2
import rclpy
from camera_feed_publisher import CameraFeedPublisher
from camera_feed_subscriber import CameraFeedSubscriber

rclpy.init()
publisher = CameraFeedPublisher()
ports = {}

def identify_ports():
    """
    Scans camera ports and stores the opened capture objects.

    Iterates through ports 0 through 9, attempts to open each one,
    and adds each available camera to the global ports dictionary.
    """
    for i in range(10):
        cap = cv2.VideoCapture(i)
        if not cap.isOpened():continue
        ports[cap] = i

def init_camera(port = 4):
    """
    Initialises and returns a camera using OpenCV's VideoCapture.

    Opens the camera at the given port and returns the capture object
    if the camera is available.

    Returns:
        cv2.VideoCapture: An opened camera capture object.

    Raises:
        RuntimeError: If the camera cannot be opened.
    """
    cap = cv2.VideoCapture(port)
    if not cap.isOpened():
        raise RuntimeError("Could not open camera. Check USB connection.")
    return cap


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
    identify_ports()

    while True:
        for cap, port in ports.items():
            image = capture_frame(cap)
            send_frame(image, port)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

finally:
    for cap in ports:
        release_camera(cap)
    publisher.destroy_node()
    rclpy.shutdown()
