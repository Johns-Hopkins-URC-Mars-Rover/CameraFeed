import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

class CameraFeedPublisher(Node):
    """
    Creates a ROS 2 Node that publishes camera frames to an image topic.
    """

    def __init__(self):
        """
        Instatiation of 5 Publisher Objects. Publisher0 - Publisher3 are for the 
        4 Innomaker Cameras. Publisherz is for the ZED Camera.
        """
        super().__init__('camera_feed_publisher')
        
        self.publisher_dict = {
            0: self.create_publisher(Image, "/camera0/image_raw", 10),
            1: self.create_publisher(Image, "/camera1/image_raw", 10),
            2: self.create_publisher(Image, "/camera2/image_raw", 10),
            3: self.create_publisher(Image, "/camera3/image_raw", 10),
            4: self.create_publisher(Image, "/cameraz/image_raw", 10),
        }
        self.br = CvBridge()

    def send_frame(self, frame, port):
        """
        Converts and publishes an Image Message Type message given the image.
        
        Args:
            frame(np.ndarray): The camera image as a BGR numpy array from OpenCV.
        """
        
        # Convert the OpenCV frame to a ROS 2 image message and broadcast it
        # on the appropriate channel
        msg = self.br.cv2_to_imgmsg(frame, encoding="bgr8") # not sure setting encoding is supported, if erro just rmv the arg
        if ( self.publisher_dict.get(port) ):
            self.publisher_dict[port].publish(msg)
            # Log the publish event to the console for debugging and tracking
            self.get_logger().info(f'Publishing Frame')
        else: return
    

def main(args=None):
    """
    The main entry point for the node.
    
    Initializes ROS 2 communications, creates the node instance, performs 
    a placeholder publish call, and spins the node to keep it alive.
    """
    rclpy.init(args=args)
    camera_feed_publisher = CameraFeedPublisher()
    camera_feed_publisher.send_frame(None, 1) # for your use/test case, you could replace this with a cv2 camera reader and publish real image frames
    rclpy.spin(camera_feed_publisher)
    camera_feed_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
