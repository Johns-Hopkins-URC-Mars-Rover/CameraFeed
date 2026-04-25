import cv2
import rclpy
from camera_feed_publisher import CameraFeedPublisher
from camera_feed_subscriber import CameraFeedSubscriber

rclpy.init()
publisher = CameraFeedPublisher()


def init_camera(port = 4):
    """
    Initialises and returns the ZED camera using OpenCV's VideoCapture.

    The ZED camera exposes itself as two side-by-side frames in a single
    wide image. We capture that and split it to get the left frame only.

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
    Captures a single frame from the camera and returns the left image.

    The outputs a wide side-by-side stereo image. The left half
    corresponds to the left camera, which matches the calibration file.

    Args:
        cap: An open cv2.VideoCapture object for the camera.

    Returns:
        np.ndarray: The left camera image as a BGR numpy array.

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


def send_frame(frame):
    publisher.send_frame(frame)
    rclpy.spin_once(publisher, timeout_sec=0.1)

cap = init_camera()

while True:
    image = capture_frame(cap)
    send_frame(image)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

release_camera()
publisher.destroy_node()
rclpy.shutdown()
cv2.destroyAllWindows()