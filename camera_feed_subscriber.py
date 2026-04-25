import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

class CameraFeedSubscriber(Node):

    def __init__(self):
        super().__init__('camera_feed_subscriber')
        
        self.subscription = self.create_subscription(
            Image,
            'camera_frame',
            self.frame_callback,
            10
        )
        self.br = CvBridge()

    def frame_callback(self, frame):
        self.get_logger().info(f'Recieved Frame')
    

def main(args=None):
    """
    The main entry point for the node.
    
    Initializes ROS 2 communications, creates the node instance, demonstrates 
    a test publish, and spins the node to keep it alive.
    """
    rclpy.init(args=args)
    camera_feed_subscriber = CameraFeedSubscriber()
    rclpy.spin(camera_feed_subscriber)
    camera_feed_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()