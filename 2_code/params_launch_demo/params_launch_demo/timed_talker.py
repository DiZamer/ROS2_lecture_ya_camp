import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class TimedTalker(Node):

    def __init__(self):
        super().__init__('timed_talker')
        self.declare_parameter('publish_rate', 1.0)
        self.declare_parameter('message_prefix', 'Msg')
        self.publisher = self.create_publisher(String, '/chatter', 10)
        self.count = 0
        self.create_timer(0.1, self.timer_callback)
        self.last_time = self.get_clock().now()
        self.get_logger().info('TimedTalker started')

    def timer_callback(self):
        rate = self.get_parameter('publish_rate').value
        if rate <= 0:
            return
        now = self.get_clock().now()
        elapsed = (now - self.last_time).nanoseconds / 1e9
        if elapsed >= (1.0 / rate):
            prefix = self.get_parameter('message_prefix').value
            msg = String()
            msg.data = f'{prefix} #{self.count}'
            self.publisher.publish(msg)
            self.get_logger().info(f'Published: {msg.data}')
            self.count += 1
            self.last_time = now


def main(args=None):
    rclpy.init(args=args)
    node = TimedTalker()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()