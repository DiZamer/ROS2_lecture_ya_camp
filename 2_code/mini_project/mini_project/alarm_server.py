import rclpy
from rclpy.node import Node
from std_srvs.srv import Trigger


class AlarmServer(Node):

    def __init__(self):
        super().__init__('alarm_server')
        self.srv = self.create_service(Trigger, '/alarm', self.callback)
        self.alarm_count = 0
        self.get_logger().info('Alarm server ready')

    def callback(self, request, response):
        self.alarm_count += 1
        self.get_logger().warn(
            f'ALARM triggered! Total alarms: {self.alarm_count}')
        response.success = True
        response.message = f'Alarm #{self.alarm_count} confirmed'
        return response


def main(args=None):
    rclpy.init(args=args)
    node = AlarmServer()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()