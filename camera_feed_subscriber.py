import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

class CameraFeedSubscriber(Node):

    def __init__(self):
        super().__init__('camera_feed_subscriber')

        self.subscriptions = []
        for topic in (
            "/camera0/image_raw",
            "/camera1/image_raw",
            "/camera2/image_raw",
            "/camera3/image_raw",
            "/cameraz/image_raw",
        ):
            subscription = self.create_subscription(
                Image,
                topic,
                lambda frame, topic=topic: self.frame_callback(frame, topic),
                10
            )
            self.subscriptions.append(subscription)

        self.br = CvBridge()

    def frame_callback(self, frame, topic):
        self.get_logger().info(f'Received frame from {topic}')
    

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
