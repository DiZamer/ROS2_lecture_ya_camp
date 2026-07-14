# Практика: Service Server и Client

## Цель

Создать Python-пакет `service_demo` с service server-ом `/add_two_ints` (тип `example_interfaces/srv/AddTwoInts`): принимает запрос с полями `a` и `b` (int64), возвращает ответ с полем `sum` (int64). Вызвать сервис из CLI через `ros2 service call`. Опционально — написать service client, который вызывает сервер программно.

## Предварительные требования

- Выполнены практики [01_workspace](01_workspace.md) и [02_package](02_package.md)
- Пройдена практика [03_topic](03_topic.md)

## Что получится

- Пакет `service_demo` с зависимостями `rclpy` и `example_interfaces`
- Узел `server` (класс `AddTwoIntsServer`): создаёт service `/add_two_ints`, в `callback()` принимает `request.a + request.b`, возвращает `response.sum`
- Узел `client` (опционально, класс `AddTwoIntsClient`): через `wait_for_service()` ждёт сервер, вызывает с `a=5, b=3`, получает `sum=8`
- Проверка через `ros2 service list`, `ros2 service type`, `ros2 service call` с JSON-аргументами

---

## Шаг 1. Создать пакет

```bash
cd ~/ros2_ws/src
ros2 pkg create --build-type ament_python service_demo \
  --dependencies rclpy example_interfaces
```

`example_interfaces` содержит встроенный тип `AddTwoInts` — не нужно создавать `.srv`-файлы.

## Шаг 2. Код service server

Создать `service_demo/server.py`:

```python
from example_interfaces.srv import AddTwoInts   # .srv-файл: int64 a, int64 b, ---, int64 sum
import rclpy
from rclpy.node import Node


class AddTwoIntsServer(Node):
    """Service server: принимает a и b, возвращает сумму"""

    def __init__(self):
        super().__init__('add_two_ints_server')  # Имя узла
        # Создаём сервис:
        #   AddTwoInts — тип (описывает request и response)
        #   '/add_two_ints' — имя сервиса (клиент обращается по нему)
        #   self.callback — функция, вызываемая при каждом запросе
        self.srv = self.create_service(
            AddTwoInts, '/add_two_ints', self.callback)

    def callback(self, request, response):
        """Вызывается при обращении клиента — складывает числа и возвращает результат"""
        response.sum = request.a + request.b
        self.get_logger().info(
            f'{request.a} + {request.b} = {response.sum}')
        return response  # ROS2 автоматически отправляет response клиенту
```

## Шаг 3. Код service client (опционально)

Создать `service_demo/client.py`:

```python
from example_interfaces.srv import AddTwoInts
import rclpy
from rclpy.node import Node


class AddTwoIntsClient(Node):
    """Service client: ждёт сервер, отправляет запрос, получает ответ"""

    def __init__(self):
        super().__init__('add_two_ints_client')
        # Создаём клиент для сервиса /add_two_ints типа AddTwoInts
        self.cli = self.create_client(AddTwoInts, '/add_two_ints')
        # Ожидание: пока сервер не появится — блокируемся
        # Без wait_for_service() клиент упадёт с ошибкой «service not available»
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for service...')
        # Сервер готов — отправляем запрос
        self.send_request(5, 3)

    def send_request(self, a, b):
        """Формирует запрос и отправляет асинхронно — не блокирует узел"""
        request = AddTwoInts.Request()
        request.a = a
        request.b = b
        # Асинхронный вызов: не ждём ответа, а подписываемся на него через callback
        future = self.cli.call_async(request)
        future.add_done_callback(self.response_callback)

    def response_callback(self, future):
        """Вызывается, когда сервер вернул ответ"""
        response = future.result()
        self.get_logger().info(f'Result: {response.sum}')
```

## Шаг 4. Настроить точки входа

Добавить `main()` в `server.py` и `client.py`:

```python
def main(args=None):
    rclpy.init(args=args)
    node = AddTwoIntsServer()   # или AddTwoIntsClient()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
```

Обновить `setup.py` → `entry_points`:

```python
entry_points={
    'console_scripts': [
        'server = service_demo.server:main',
        'client = service_demo.client:main',
    ],
},
```

## Шаг 5. Сборка

```bash
cd ~/ros2_ws
colcon build --packages-select service_demo
source install/setup.bash
```

## Шаг 6. Запуск и проверка

Терминал 1 — запустить server:

```bash
ros2 run service_demo server
# [INFO] [add_two_ints_server]: Service ready
```

Терминал 2 — проверка из CLI:

```bash
# Список services
ros2 service list
# /add_two_ints

# Тип service
ros2 service type /add_two_ints
# example_interfaces/srv/AddTwoInts

# Вызов
ros2 service call /add_two_ints example_interfaces/srv/AddTwoInts "{a: 5, b: 3}"
# sum: 8

ros2 service call /add_two_ints example_interfaces/srv/AddTwoInts "{a: 100, b: 200}"
# sum: 300
```

В терминале server появляются логи:

```
[INFO] [add_two_ints_server]: 5 + 3 = 8
[INFO] [add_two_ints_server]: 100 + 200 = 300
```

Терминал 2 — запустить client:

```bash
ros2 run service_demo client
# [INFO] [add_two_ints_client]: Result: 8
```

---

## Проверка результата

| Команда | Ожидаемый результат |
| --- | --- |
| `ros2 service list` | `/add_two_ints` в списке |
| `ros2 service type /add_two_ints` | `example_interfaces/srv/AddTwoInts` |
| `ros2 service call /add_two_ints ... "{a: 5, b: 3}"` | `sum: 8` |
| `ros2 run service_demo client` | `Result: 8` |

---

## Вопросы студентам

1. Что произойдет, если вызвать `ros2 service call` до запуска server?
2. Чем отличается `call_async` от синхронного вызова? Почему в курсе используется асинхронный?
3. Почему client ждет server через `wait_for_service()`? Что будет без этой проверки?
4. В чем отличие service от topic в этой практике? (topic — поток, service — запрос-ответ)

---

## Типичные ошибки

| Симптом | Причина | Исправление |
| --- | --- | --- |
| `ros2 service call` — service not available | Server не запущен | Запустить `server` перед вызовом |
| Client сразу падает | Server не готов, `wait_for_service` не используется | Добавить `wait_for_service()` перед `send_request` |
| Service виден, но не отвечает | Server забыл `spin()` | Добавить `rclpy.spin(node)` в `main()` |
| `ros2 service call` — wrong type | Неправильное имя типа | `example_interfaces/srv/AddTwoInts` |
| Неправильные имена полей | Ответ 0 или пустой | Поля: `a`, `b`, `sum` (строчные) |

---

## Дополнительное задание

1. **Измените логику server**: пусть он умножает числа, а не складывает. Вызовите из CLI, проверьте ответ.
2. **Добавьте второй service** в тот же пакет: `/subtract_two_ints`. Не забудьте новый `entry_point`.
3. **Две ноды — два разных service**: запустите `server_add` и `server_subtract` одновременно. Проверьте `ros2 service list` — оба видны.

---

## Ссылки

- [Services — статья базы знаний](../2_knowledge/services.md)
- [Writing a simple service/client](https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Py-Service-And-Client.html)
- [Understanding ROS2 Services](https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Services/Understanding-ROS2-Services.html)