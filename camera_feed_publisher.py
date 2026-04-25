import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

class CameraFeedPublisher(Node):

    def __init__(self):
        super().__init__('camera_feed_publisher')
        
        self.publisher_ = self.create_publisher(Image, 'camera_frame', 10)
        self.br = CvBridge()

    def send_frame(self, frame):
        """
        Constructs and publishes a Vector3 message with the provided coordinates.
        
        Args:
            x (float): The movement displacement along the X-axis (e.g., in meters).
            y (float): The movement displacement along the Y-axis (e.g., in meters).
            z (float): The movement displacement along the Z-axis (e.g., in meters).
        """
        
        # Broadcast the message to the ROS 2 network
        self.publisher_.publish(self.br.cv2_to_imgmsg(frame))
        
        # Log the published data to the console for debugging and tracking
        self.get_logger().info(f'Publishing Frame')
    

def main(args=None):
    """
    The main entry point for the node.
    
    Initializes ROS 2 communications, creates the node instance, demonstrates 
    a test publish, and spins the node to keep it alive.
    """
    rclpy.init(args=args)
    camera_feed_publisher = CameraFeedPublisher()
    camera_feed_publisher.send_frame(None)
    rclpy.spin(camera_feed_publisher)
    camera_feed_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()