import time
from example_interfaces.action import Fibonacci
import rclpy
from rclpy.action import ActionServer
from rclpy.node import Node


class TaskServer(Node):

    def __init__(self):
        super().__init__('task_server')
        self.action_server = ActionServer(
            self, Fibonacci, '/process_task', self.execute_callback)
        self.get_logger().info('Task server ready')

    def execute_callback(self, goal_handle):
        order = goal_handle.request.order
        self.get_logger().info(f'Processing task: order={order}')

        sequence = [0, 1]
        goal_handle.publish_feedback(Fibonacci.Feedback(sequence=sequence))

        for i in range(1, order):
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                self.get_logger().info('Task canceled')
                return Fibonacci.Result(sequence=sequence)
            sequence.append(sequence[i] + sequence[i - 1])
            goal_handle.publish_feedback(
                Fibonacci.Feedback(sequence=sequence))
            time.sleep(1.0)

        goal_handle.succeed()
        self.get_logger().info(f'Task finished: {sequence}')
        return Fibonacci.Result(sequence=sequence)


def main(args=None):
    rclpy.init(args=args)
    node = TaskServer()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()