# Шпаргалка: Topic, Service, Action

## Выбор механизма

| | Topic | Service | Action |
|---|---|---|---|
| **Связь** | Многие → многие | 1 → 1 | 1 → 1 |
| **Ответ** | Нет | Один | Прогресс + итог |
| **Длительность** | Непрерывно | < 1 с | Секунды/минуты |
| **Отмена** | Нет | Нет | Есть |
| **Пример** | `/scan` | `/emergency_stop` | `/navigate_to_pose` |

**Правило**: поток → topic, запрос-ответ → service, долгая задача → action.

---

## Publisher

```python
from std_msgs.msg import String

self.pub = self.create_publisher(String, '/chatter', 10)

msg = String()
msg.data = f'Hello {self.count}'
self.pub.publish(msg)
```

## Subscriber

```python
self.sub = self.create_subscription(
    String, '/chatter', self.callback, 10)

def callback(self, msg):
    self.get_logger().info(f'Heard: {msg.data}')
```

---

## Service server

```python
from example_interfaces.srv import AddTwoInts

self.srv = self.create_service(AddTwoInts, '/add_two_ints', self.callback)

def callback(self, request, response):
    response.sum = request.a + request.b
    return response
```

## Service client

```python
self.cli = self.create_client(AddTwoInts, '/add_two_ints')
self.cli.wait_for_service()

request = AddTwoInts.Request()
request.a = 5; request.b = 3
future = self.cli.call_async(request)
future.add_done_callback(lambda f: print(f.result().sum))
```

---

## Action server

```python
from example_interfaces.action import Fibonacci
from rclpy.action import ActionServer

self.server = ActionServer(self, Fibonacci, '/fibonacci', self.execute)

def execute(self, goal_handle):
    # вычисления...
    goal_handle.publish_feedback(Fibonacci.Feedback(sequence=seq))
    if goal_handle.is_cancel_requested:
        goal_handle.canceled()
        return Fibonacci.Result(sequence=seq)
    goal_handle.succeed()
    return Fibonacci.Result(sequence=seq)
```

## Action client

```python
from rclpy.action import ActionClient

self.client = ActionClient(self, Fibonacci, '/fibonacci')
self.client.wait_for_server()

goal = Fibonacci.Goal()
goal.order = 5
self.client.send_goal_async(
    goal,
    feedback_callback=lambda msg: print(msg.feedback.sequence)
).add_done_callback(self.goal_response)

def goal_response(self, future):
    goal_handle = future.result()
    if goal_handle.accepted:
        goal_handle.get_result_async().add_done_callback(
            lambda f: print(f.result().result.sequence))
```

---

## Parameters

```python
self.declare_parameter('publish_rate', 1.0)
rate = self.get_parameter('publish_rate').value
# Читать в callback, если нужно менять на лету
```

## YAML-конфиг

```yaml
my_node:
  ros__parameters:
    publish_rate: 2.0
    frame_id: "lidar"
```

## Launch

```python
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(package='my_pkg', executable='talker'),
        Node(package='my_pkg', executable='listener'),
    ])
```

С YAML:

```python
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare

config = PathJoinSubstitution([FindPackageShare('my_pkg'), 'config', 'params.yaml'])
Node(..., parameters=[config])
```

---

## Часто используемые message types

| Пакет | Тип | Поля |
|---|---|---|
| `std_msgs` | `String` | `data: string` |
| `std_msgs` | `Float32` | `data: float32` |
| `std_msgs` | `Int32` | `data: int32` |
| `geometry_msgs` | `Twist` | `linear: Vector3, angular: Vector3` |
| `std_srvs` | `Trigger` | Request: пустой, Response: `success: bool, message: string` |
| `example_interfaces` | `AddTwoInts` (srv) | `a: int64, b: int64 → sum: int64` |
| `example_interfaces` | `Fibonacci` (action) | Goal: `order: int32`, Feedback/Result: `sequence: int32[]` |