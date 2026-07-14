import random
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32


class SensorNode(Node):

    def __init__(self):
        super().__init__('sensor_node')
        self.declare_parameter('publish_rate', 1.0)
        self.declare_parameter('max_value', 10.0)

        rate = self.get_parameter('publish_rate').value
        self.publisher = self.create_publisher(Float32, '/sensor_data', 10)
        period = 1.0 / rate if rate > 0 else 1.0
        self.timer = self.create_timer(period, self.timer_callback)
        self.get_logger().info(f'Sensor started: rate={rate} Hz')

    def timer_callback(self):
        max_val = self.get_parameter('max_value').value
        msg = Float32()
        msg.data = random.uniform(0.0, max_val)
        self.publisher.publish(msg)
        self.get_logger().info(f'Sensor data: {msg.data:.3f}')


def main(args=None):
    rclpy.init(args=args)
    node = SensorNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()