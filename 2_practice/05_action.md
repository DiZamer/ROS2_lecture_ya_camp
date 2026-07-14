# Практика: Action Server и Client

## Цель

Создать Python-пакет `action_demo` с action server-ом `/fibonacci` (тип `example_interfaces/action/Fibonacci`): принимает `goal.order` (сколько чисел вычислить), считает последовательность с паузой 1 сек между числами, отправляет `feedback.sequence` после каждого шага, поддерживает отмену через `cancel`. Написать action client, который отправляет `goal.order=8`, получает все feedback и финальный result. Проверить через `ros2 action send_goal --feedback` и демонстрацию cancel (Ctrl+C).

## Предварительные требования

- Выполнены практики [01-04](01_workspace.md)
- Пройдена практика [04_service](04_service.md)

## Что получится

- Пакет `action_demo` с зависимостями `rclpy` и `example_interfaces`
- Узел `fibonacci_server`: `ActionServer(self, Fibonacci, '/fibonacci', execute_callback)`. В цикле: проверяет `is_cancel_requested`, считает следующее число, публикует feedback через `publish_feedback()`, спит 1 сек. По завершении — `succeed()` или `canceled()`
- Узел `fibonacci_client`: ждёт сервер через `wait_for_server()`, отправляет goal.order=8 через `send_goal_async()`, получает feedback через `feedback_callback` и result через `result_callback`
- Проверка: `ros2 action send_goal /fibonacci ... --feedback` (постепенный вывод sequence), Ctrl+C во время выполнения (сервер выводит «Goal canceled»)

---

## Шаг 1. Создать пакет

```bash
cd ~/ros2_ws/src
ros2 pkg create --build-type ament_python action_demo \
  --dependencies rclpy example_interfaces
```

`example_interfaces` содержит встроенный тип `Fibonacci` с `.action`-файлом.

## Шаг 2. Код action server

Создать `action_demo/server.py`:

```python
import time
from example_interfaces.action import Fibonacci   # .action: int32 order(int64 order), ---, int32[] sequence
import rclpy
from rclpy.action import ActionServer            # Класс для создания action server
from rclpy.node import Node


class FibonacciServer(Node):
    """Action server: принимает goal (order), шлёт feedback каждую секунду, возвращает result"""

    def __init__(self):
        super().__init__('fibonacci_server')
        # Создаём action server:
        #   Fibonacci — тип действия (goal: order, feedback: sequence, result: sequence)
        #   '/fibonacci' — имя (клиент подключается по нему)
        #   execute_callback — вызывается при получении новой цели
        self.action_server = ActionServer(
            self, Fibonacci, '/fibonacci', self.execute_callback)

    def execute_callback(self, goal_handle):
        """Выполняет действие: считает числа Фибоначчи, шлёт feedback, поддерживает cancel"""
        self.get_logger().info(
            f'Goal received: order={goal_handle.request.order}')
        feedback_msg = Fibonacci.Feedback()
        feedback_msg.sequence = [0, 1]
        goal_handle.publish_feedback(feedback_msg)
        sequence = [0, 1]
        for i in range(1, goal_handle.request.order):
            # Проверка отмены — клиент может отправить cancel в любой момент
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()  # Подтверждаем отмену
                self.get_logger().info('Goal canceled')
                return Fibonacci.Result(sequence=sequence)
            sequence.append(sequence[i] + sequence[i - 1])
            feedback_msg.sequence = sequence
            goal_handle.publish_feedback(feedback_msg)  # Отправляем прогресс клиенту
            self.get_logger().info(f'Feedback: {sequence}')
            time.sleep(1.0)  # Имитация длительной операции
        goal_handle.succeed()  # Отмечаем успешное завершение
        self.get_logger().info('Goal succeeded')
        return Fibonacci.Result(sequence=sequence)
```

**Разбор ключевых строк:**

| Строка | Что делает |
| --- | --- |
| `ActionServer(self, Fibonacci, '/fibonacci', ...)` | Создает action server для типа Fibonacci |
| `execute_callback(self, goal_handle)` | Вызывается при получении goal |
| `goal_handle.publish_feedback(...)` | Отправляет клиенту прогресс |
| `goal_handle.is_cancel_requested` | Проверяет, попросил ли client отмену |
| `goal_handle.canceled()` | Сообщает, что задача отменена |
| `goal_handle.succeed()` | Сообщает, что задача выполнена успешно |
| `return Fibonacci.Result(...)` | Возвращает итоговый результат |

## Шаг 3. Код action client

Создать `action_demo/client.py`:

```python
from example_interfaces.action import Fibonacci
import rclpy
from rclpy.action import ActionClient            # Класс для создания action client
from rclpy.node import Node


class FibonacciClient(Node):
    """Action client: отправляет goal, получает feedback (прогресс) и result (итог)"""

    def __init__(self):
        super().__init__('fibonacci_client')
        # Создаём action client для /fibonacci типа Fibonacci
        self.client = ActionClient(self, Fibonacci, '/fibonacci')
        # Ждём, пока сервер запустится — без этого send_goal_async упадёт
        self.client.wait_for_server()
        self.send_goal(8)

    def send_goal(self, order):
        """Формирует goal с order=8 и отправляет асинхронно"""
        goal_msg = Fibonacci.Goal()
        goal_msg.order = order
        self.get_logger().info(f'Sending goal: order={order}')
        # Асинхронная отправка: не блокирует узел
        self.client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback  # каждый feedback → этот callback
        ).add_done_callback(self.goal_response_callback)  # ответ сервера → этот callback

    def goal_response_callback(self, future):
        """Сервер принял или отклонил goal"""
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected')
            return
        self.get_logger().info('Goal accepted')
        # Запрашиваем финальный result — придёт, когда сервер завершит
        goal_handle.get_result_async().add_done_callback(self.result_callback)

    def feedback_callback(self, feedback_msg):
        """Каждый шаг — сервер прислал прогресс"""
        seq = feedback_msg.feedback.sequence
        self.get_logger().info(f'Progress: {seq}')

    def result_callback(self, future):
        """Сервер завершил — получили финальный result"""
        result = future.result().result
        self.get_logger().info(f'Result: {result.sequence}')
```

**Три callback-а action client:**

| Callback | Когда вызывается |
| --- | --- |
| `feedback_callback` | При каждом feedback от server |
| `goal_response_callback` | Когда server принял или отклонил goal |
| `result_callback` | Когда server завершил задачу |

## Шаг 4. Настроить точки входа

Добавить `main()` в оба файла:

```python
def main(args=None):
    rclpy.init(args=args)
    node = FibonacciServer()   # или FibonacciClient()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
```

Обновить `setup.py` → `entry_points`:

```python
entry_points={
    'console_scripts': [
        'fibonacci_server = action_demo.server:main',
        'fibonacci_client = action_demo.client:main',
    ],
},
```

## Шаг 5. Сборка

```bash
cd ~/ros2_ws
colcon build --packages-select action_demo
source install/setup.bash
```

## Шаг 6. Запуск и проверка

Терминал 1 — server:

```bash
ros2 run action_demo fibonacci_server
```

Терминал 2 — отправить goal из CLI с feedback:

```bash
ros2 action list
# /fibonacci

ros2 action info /fibonacci
# Action: /fibonacci
# Action clients: 0
# Action servers: 1

ros2 action send_goal /fibonacci example_interfaces/action/Fibonacci "{order: 5}" --feedback
```

Ожидаемый вывод (feedback приходит постепенно):

```
Goal accepted with ID: <id>

Feedback:
    sequence: [0, 1]

Feedback:
    sequence: [0, 1, 1]

Feedback:
    sequence: [0, 1, 1, 2]

Feedback:
    sequence: [0, 1, 1, 2, 3]

Feedback:
    sequence: [0, 1, 1, 2, 3, 5]

Result:
    sequence: [0, 1, 1, 2, 3, 5]
```

Терминал 2 — client:

```bash
ros2 run action_demo fibonacci_client
# [INFO] [fibonacci_client]: Sending goal: order=8
# [INFO] [fibonacci_client]: Goal accepted
# [INFO] [fibonacci_client]: Progress: [0, 1]
# [INFO] [fibonacci_client]: Progress: [0, 1, 1]
# [INFO] [fibonacci_client]: Progress: [0, 1, 1, 2]
# ... (еще 5 feedback-ов)
# [INFO] [fibonacci_client]: Result: [0, 1, 1, 2, 3, 5, 8, 13, 21]
```

---

### Демонстрация отмены (cancel)

Отправить goal с большим order из CLI:

```bash
ros2 action send_goal /fibonacci example_interfaces/action/Fibonacci "{order: 100}" --feedback
```

Пока идет счет — `Ctrl+C`. Server выводит:

```
[INFO] [fibonacci_server]: Goal canceled
```

---

## Проверка результата

| Команда | Ожидаемый результат |
| --- | --- |
| `ros2 action list` | `/fibonacci` в списке |
| `ros2 action info /fibonacci` | Тип: `example_interfaces/action/Fibonacci` |
| `ros2 action send_goal ... --feedback` | Постепенный вывод sequence, финальный result |
| `Ctrl+C` во время выполнения | Server сообщает «Goal canceled» |
| `ros2 run action_demo fibonacci_client` | Client получает все feedback и result |

---

## Вопросы студентам

1. Чем action отличается от service? Почему Fibonacci — это action, а не service?
2. Где в коде server проверяется запрос на отмену? Что будет, если убрать `is_cancel_requested`?
3. Сколько callback-ов у action client? За что каждый отвечает?
4. Почему `time.sleep(1.0)` внутри `execute_callback` — это нормально, а внутри callback subscriber-а — плохо?
5. Зачем нужен `wait_for_server()` перед `send_goal_async()`?

---

## Типичные ошибки

| Симптом | Причина | Исправление |
| --- | --- | --- |
| Goal не принимается | Server не запущен | Запустить server |
| Feedback не приходит | `publish_feedback` не вызывается | Проверить цикл в `execute_callback` |
| Cancel не работает | Не проверяется `is_cancel_requested` | Добавить проверку в цикл |
| Server зависает после cancel | `canceled()` вызван, но `return` не сделан | Сделать `return` после `canceled()` |
| `wait_for_server()` висит бесконечно | Server не запущен | Запустить server или поставить timeout |
| `ImportError` для `Fibonacci` | Зависимость `example_interfaces` не объявлена | Добавить в `package.xml` и пересобрать |
| Goal rejected при order=0 | Server не обрабатывает edge cases | Добавить проверку `if order < 1: goal_handle.abort()` |

---

## Дополнительное задание

1. **Измените логику**: пусть server считает не Фибоначчи, а факториал. Обновите feedback и result.

2. **Отмена по таймеру**: добавьте в client код, который отправляет goal и через 3 секунды автоматически вызывает cancel:

```python
import threading

def send_then_cancel(self):
    future = self.client.send_goal_async(goal_msg)
    threading.Timer(3.0, lambda: future.result().cancel_goal_async()).start()
```

3. **Goal rejected**: измените server так, чтобы он отклонял goal с `order > 20`. Проверьте, что client получает «Goal rejected».

4. **Множественные goals**: отправьте два goal подряд из CLI и посмотрите, как server их обрабатывает (по очереди — action server по умолчанию обрабатывает goals последовательно).

---

## Ссылки

- [Actions — статья базы знаний](../2_knowledge/actions.md)
- [Writing an action server/client (Python)](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Writing-an-Action-Server-Client/Py.html)
- [Understanding ROS2 Actions](https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Actions/Understanding-ROS2-Actions.html)