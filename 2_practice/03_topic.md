# Практика: Publisher и Subscriber

## Цель

Создать Python-пакет `topic_demo` с двумя узлами: `talker` (публикует `std_msgs/String` с инкрементальным счётчиком в топик `/chatter` раз в секунду) и `listener` (подписан на `/chatter`, выводит полученные сообщения в лог). Проверить обмен через `ros2 topic echo`, `ros2 topic info`, `ros2 topic hz` и ручную вставку сообщения через `ros2 topic pub`.

## Предварительные требования

- Выполнены практики [01_workspace](01_workspace.md) и [02_package](02_package.md)
- Workspace `~/ros2_ws` создан и активирован

## Что получится

- Пакет `topic_demo` (ament_python) с зависимостями `rclpy` и `std_msgs`
- Узел `talker`: создаёт publisher для `std_msgs/String` по адресу `/chatter`, по таймеру 1.0 с публикует `Message #N`
- Узел `listener`: создаёт subscription на `/chatter`, при каждом сообщении вызывает `callback(msg)` и выводит `I heard: ...`
- Проверка через `ros2 topic echo /chatter` (поток сообщений), `ros2 topic hz /chatter` (частота ~1.0 Гц), `ros2 topic info /chatter` (1 publisher, 1 subscriber)
- Ручная вставка сообщения через `ros2 topic pub --once`

---

## Шаг 1. Создать пакет

```bash
cd ~/ros2_ws/src
ros2 pkg create --build-type ament_python topic_demo \
  --dependencies rclpy std_msgs
```

## Шаг 2. Код publisher

Создать `topic_demo/talker.py`:

```python
import rclpy                         # ROS2 Python-клиент
from rclpy.node import Node          # Базовый класс узла
from std_msgs.msg import String      # Тип сообщения: строка


class Talker(Node):
    """Издатель: по таймеру публикует String с инкрементальным счётчиком в /chatter"""

    def __init__(self):
        super().__init__('talker')   # Имя узла в ROS Graph
        # Создаём publisher:
        #   String — тип сообщения
        #   '/chatter' — имя топика (все subscriber-ы подписываются по этому имени)
        #   10 — queue_size (буфер на 10 сообщений, если subscriber медленный)
        self.publisher = self.create_publisher(String, '/chatter', 10)
        self.count = 0
        # Таймер: раз в секунду вызывает timer_callback()
        self.timer = self.create_timer(1.0, self.timer_callback)

    def timer_callback(self):
        """Формирует сообщение, публикует в топик — все subscriber-ы получат копию"""
        msg = String()
        msg.data = f'Message #{self.count}'
        self.publisher.publish(msg)  # Отправка — DDS доставит всем подписчикам
        self.get_logger().info(f'Published: {msg.data}')
        self.count += 1
```

## Шаг 3. Код subscriber

Создать `topic_demo/listener.py`:

```python
import rclpy                         # ROS2 Python-клиент
from rclpy.node import Node          # Базовый класс узла
from std_msgs.msg import String      # Тип сообщения: строка


class Listener(Node):
    """Подписчик: при каждом новом сообщении в /chatter вызывает callback"""

    def __init__(self):
        super().__init__('listener')  # Имя узла в ROS Graph
        # Создаём subscription:
        #   String — тип сообщения (должен совпадать с типом publisher-а)
        #   '/chatter' — имя топика (подписываемся на тот же, что публикует talker)
        #   self.callback — функция, вызываемая при каждом новом сообщении
        #   10 — queue_size (буфер входящих сообщений)
        self.subscriber = self.create_subscription(
            String, '/chatter', self.callback, 10)

    def callback(self, msg):
        """Вызывается при каждом новом сообщении в /chatter"""
        self.get_logger().info(f'I heard: {msg.data}')
```

## Шаг 4. Настроить точки входа

Отредактировать `setup.py` — добавить оба узла в `entry_points`:

```python
entry_points={
    'console_scripts': [
        'talker = topic_demo.talker:main',
        'listener = topic_demo.listener:main',
    ],
},
```

Не забудьте добавить `main()` в каждый файл:

```python
def main(args=None):
    rclpy.init(args=args)
    node = Talker()     # или Listener()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
```

## Шаг 5. Сборка

```bash
cd ~/ros2_ws
colcon build --packages-select topic_demo
source install/setup.bash
```

## Шаг 6. Запуск

Терминал 1 — publisher:

```bash
ros2 run topic_demo talker
# [INFO] [talker]: Published: Message #0
# [INFO] [talker]: Published: Message #1
```

Терминал 2 — subscriber:

```bash
ros2 run topic_demo listener
# [INFO] [listener]: I heard: Message #1
# [INFO] [listener]: I heard: Message #2
```

---

## Проверка результата

| Команда | Ожидаемый результат |
| --- | --- |
| `ros2 topic list` | `/chatter` в списке |
| `ros2 topic echo /chatter` | Поток сообщений `data: 'Message #N'` |
| `ros2 topic hz /chatter` | Частота публикации (около 1.0 Гц) |
| `ros2 topic info /chatter` | Тип `std_msgs/String`, 1 pub, 1 sub |

### Вставка сообщения из CLI

Когда publisher и subscriber работают:

```bash
ros2 topic pub --once /chatter std_msgs/String "data: 'Hello from CLI'"
```

Subscriber немедленно показывает: `I heard: Hello from CLI`. Это сообщение вставлено вручную, а не publisher.

---

## Вопросы студентам

1. Что произойдет, если запустить subscriber без publisher? А наоборот?
2. Сколько subscriber-ов можно подключить к одному topic?
3. Почему `ros2 topic pub` отправляет сообщение, даже если publisher не запущен?
4. Что делает `ros2 topic hz` и зачем это нужно при отладке?

---

## Типичные ошибки

| Симптом | Причина | Исправление |
| --- | --- | --- |
| `ros2 topic list` пустой | Ни один узел с pub/sub не запущен | Запустить talker или listener |
| `ros2 topic echo` не показывает сообщения | Publisher не запущен или забыли `spin()` | Проверить `rclpy.spin(node)` и запустить оба узла |
| Subscriber не получает сообщения | Разные имена topic | Сверить `/chatter` в pub и sub |
| `ros2 topic info` показывает 0 subscriber | Subscriber не запущен или упал | Проверить ошибки в терминале subscriber |
| `ModuleNotFoundError: No module named 'std_msgs'` | Зависимость не объявлена в `package.xml` | Добавить `<depend>std_msgs</depend>` |

---

## Дополнительное задание

1. **Заменить тип сообщения** на `geometry_msgs/Twist`. Publisher публикует случайную линейную и угловую скорость, subscriber выводит значения. Не забудьте добавить `geometry_msgs` в зависимости.

2. **Добавить второго subscriber** — `logger`, который пишет полученные сообщения в файл. Проверить `ros2 topic info` — должно быть 2 subscriber-а.

3. **Запустить три subscriber-а одновременно** и убедиться, что все получают одни и те же сообщения:

```bash
ros2 run topic_demo listener &
ros2 run topic_demo listener &
ros2 run topic_demo listener &
ros2 topic info /chatter  # → Subscribers: 3
```

---

## Ссылки

- [Topics — статья базы знаний](../2_knowledge/topics.md)
- [Writing a simple publisher/subscriber](https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Py-Publisher-And-Subscriber.html)
- [Understanding ROS2 Topics](https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Topics/Understanding-ROS2-Topics.html)