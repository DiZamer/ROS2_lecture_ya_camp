from example_interfaces.action import Fibonacci
import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from std_msgs.msg import Float32
from std_srvs.srv import Trigger


class ProcessorNode(Node):

    def __init__(self):
        super().__init__('processor_node')
        self.declare_parameter('threshold', 7.0)
        self.subscriber = self.create_subscription(
            Float32, '/sensor_data', self.data_callback, 10)

        self.alarm_client = self.create_client(Trigger, '/alarm')
        while not self.alarm_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for /alarm service...')

        self.task_client = ActionClient(self, Fibonacci, '/process_task')
        self.task_client.wait_for_server()

        self.get_logger().info('Processor ready')

    def data_callback(self, msg):
        threshold = self.get_parameter('threshold').value
        self.get_logger().info(
            f'Received: {msg.data:.3f} (threshold: {threshold:.1f})')

        if msg.data > threshold:
            self.get_logger().warn(
                f'Value {msg.data:.3f} exceeds threshold {threshold:.1f}!')
            self.call_alarm()
            self.start_task(int(msg.data))

    def call_alarm(self):
        request = Trigger.Request()
        future = self.alarm_client.call_async(request)
        future.add_done_callback(self.alarm_response_callback)

    def alarm_response_callback(self, future):
        response = future.result()
        self.get_logger().info(f'Alarm response: {response.message}')

    def start_task(self, order):
        order = min(order, 10)
        goal_msg = Fibonacci.Goal()
        goal_msg.order = order
        self.get_logger().info(f'Starting task: order={order}')
        self.task_client.send_goal_async(
            goal_msg, feedback_callback=self.task_feedback_callback
        ).add_done_callback(self.task_goal_callback)

    def task_goal_callback(self, future):
        goal_handle = future.result()
        if goal_handle.accepted:
            self.get_logger().info('Task accepted')
            goal_handle.get_result_async().add_done_callback(
                self.task_result_callback)
        else:
            self.get_logger().warn('Task rejected')

    def task_feedback_callback(self, feedback_msg):
        seq = feedback_msg.feedback.sequence
        self.get_logger().info(f'Task progress: {seq}')

    def task_result_callback(self, future):
        result = future.result().result
        self.get_logger().info(f'Task result: {result.sequence}')


def main(args=None):
    rclpy.init(args=args)
    node = ProcessorNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()