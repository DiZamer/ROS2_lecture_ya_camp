# Практика: Parameters и Launch

## Цель

Научиться задавать параметры узла через YAML и launch-файл, читать параметры в коде через `declare_parameter/get_parameter`, менять их на лету через `ros2 param set`, сохранять и загружать через `dump/load`.

## Предварительные требования

- Выполнены практики [01-05](01_workspace.md)
- Пройдена практика [03_topic](03_topic.md) — понимание publisher/subscriber

## Что получится

- Пакет `launch_demo` с зависимостями `rclpy`, `std_msgs`, `launch`, `launch_ros`
- Узел `timed_talker` (класс `TimedTalker`): объявляет параметры `publish_rate` (float, по умолч. 1.0) и `message_prefix` (string, по умолч. "Msg"), публикует `std_msgs/String` в `/chatter` с частотой из `publish_rate`. Параметр читается каждый цикл — изменение через `ros2 param set` применяется без перезапуска
- YAML-конфиг `config/talker_params.yaml`: задаёт `publish_rate: 2.0` и `message_prefix: "Tick"`
- Launch-файл `launch/talker.launch.py`: через `FindPackageShare` + `PathJoinSubstitution` находит YAML и передаёт узлу через `parameters=[config]`
- `data_files` в `setup.py`: копирует `launch/` и `config/` в `install/`
- Проверка: `ros2 topic hz /chatter` (2.0 Гц), `ros2 param set publish_rate 5.0` (частота меняется), `ros2 param dump` и `ros2 param load`

---

## Шаг 1. Создать пакет

```bash
cd ~/ros2_ws/src
ros2 pkg create --build-type ament_python launch_demo \
  --dependencies rclpy std_msgs launch launch_ros
```

## Шаг 2. Код узла с параметром

Создать `launch_demo/timed_talker.py`:

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class TimedTalker(Node):
    """Publisher с параметризованной частотой — параметр читается каждый цикл"""

    def __init__(self):
        super().__init__('timed_talker')
        # Объявляем параметры со значениями по умолчанию
        # Если параметр не объявлен — get_parameter() упадёт с ошибкой
        self.declare_parameter('publish_rate', 1.0)      # float, Гц
        self.declare_parameter('message_prefix', 'Msg')  # string, префикс сообщения
        self.publisher = self.create_publisher(String, '/chatter', 10)
        self.count = 0
        self.create_timer(0.1, self.timer_callback)  # Проверка частоты каждые 0.1 с
        self.last_time = self.get_clock().now()
        self.get_logger().info('Node started')

    def timer_callback(self):
        """Читает параметры каждый цикл — так ros2 param set работает на лету"""
        rate = self.get_parameter('publish_rate').value
        if rate <= 0:
            return  # Если частота 0 или отрицательная — не публикуем
        now = self.get_clock().now()
        elapsed = (now - self.last_time).nanoseconds / 1e9
        # Публикуем, только если прошло достаточно времени (1.0 / rate секунд)
        if elapsed >= (1.0 / rate):
            prefix = self.get_parameter('message_prefix').value
            msg = String()
            msg.data = f'{prefix} #{self.count}'
            self.publisher.publish(msg)
            self.get_logger().info(f'Published: {msg.data}')
            self.count += 1
            self.last_time = now
```

## Шаг 3. YAML-конфиг

Создать `config/talker_params.yaml`:

```yaml
timed_talker:
  ros__parameters:
    publish_rate: 2.0
    message_prefix: "Tick"
```

## Шаг 4. Launch-файл

Создать `launch/talker.launch.py`:

```python
from launch import LaunchDescription          # Описание запуска: список действий
from launch_ros.actions import Node           # Действие: запуск ROS2-узла
from launch.substitutions import PathJoinSubstitution  # Склеивание частей пути
from launch_ros.substitutions import FindPackageShare  # Поиск пути установленного пакета


def generate_launch_description():            # Имя функции строго фиксировано
    # Собираем путь: install/launch_demo/share/launch_demo/config/talker_params.yaml
    config = PathJoinSubstitution([
        FindPackageShare('launch_demo'),       # Корень установленного пакета
        'config', 'talker_params.yaml'         # Относительный путь внутри пакета
    ])

    node = Node(
        package='launch_demo',                # Имя пакета
        executable='timed_talker',            # Имя из entry_points в setup.py
        name='timed_talker',                  # Имя узла в ROS Graph (переопределяет код)
        parameters=[config]                   # Передаём YAML-файл с параметрами
    )

    return LaunchDescription([node])
```

## Шаг 5. Настроить setup.py

Важно: `data_files` копирует файлы `launch/` и `config/` в `install/`. Без этого `ros2 launch` и `FindPackageShare` не найдут файлы.

```python
import os
from glob import glob                # Поиск файлов по шаблону (*.launch.py, *.yaml)
from setuptools import setup

package_name = 'launch_demo'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # Копируем все .launch.py из launch/ в install/ — иначе ros2 launch не найдёт
        (os.path.join('share', package_name, 'launch'),
            glob('launch/*.launch.py')),
        # Копируем все .yaml из config/ в install/ — иначе параметры не загрузятся
        (os.path.join('share', package_name, 'config'),
            glob('config/*.yaml')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Student',
    maintainer_email='student@example.com',
    description='Launch demo package',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'timed_talker = launch_demo.timed_talker:main',
        ],
    },
)
```

## Шаг 6. Сборка

```bash
cd ~/ros2_ws
colcon build --packages-select launch_demo
source install/setup.bash
```

## Шаг 7. Запуск через launch

```bash
ros2 launch launch_demo talker.launch.py
# [INFO] [timed_talker]: Node started
# [INFO] [timed_talker]: Published: Tick #0
# [INFO] [timed_talker]: Published: Tick #1
```

Ожидаемая частота — 2 сообщения в секунду (из YAML: `publish_rate: 2.0`).

Проверить:

```bash
ros2 topic hz /chatter
# average rate: 2.0 Hz
```

## Шаг 8. Проверка параметров

Оставить узел запущенным. В другом терминале:

```bash
# Список параметров
ros2 param list
# /timed_talker:
#   publish_rate
#   message_prefix
#   use_sim_time

# Прочитать значение
ros2 param get /timed_talker publish_rate
# 2.0

ros2 param get /timed_talker message_prefix
# "Tick"

# Изменить на лету
ros2 param set /timed_talker publish_rate 5.0
# Set parameter successful

# Проверить частоту
ros2 topic hz /chatter
# average rate: 5.0 Hz
```

Узел меняет частоту без перезапуска — потому что `get_parameter()` вызывается в `timer_callback` каждый цикл.

## Шаг 9. Сохранить и загрузить параметры

```bash
# Сохранить текущие параметры в файл
ros2 param dump /timed_talker > my_params.yaml

# Изменить префикс
ros2 param set /timed_talker message_prefix "Hello"

# Загрузить сохраненное — префикс возвращается к "Tick"
ros2 param load /timed_talker my_params.yaml
```

---

## Проверка результата

| Команда | Ожидаемый результат |
| --- | --- |
| `ros2 launch launch_demo talker.launch.py` | Узел запущен, публикует c частотой из YAML |
| `ros2 param list` | `publish_rate`, `message_prefix` в списке |
| `ros2 param get /timed_talker publish_rate` | `2.0` (из YAML) |
| `ros2 param set /timed_talker publish_rate 5.0` | Частота меняется на лету |
| `ros2 param dump /timed_talker > my.yaml` | YAML-файл с текущими значениями |

---

## Вопросы студентам

1. Почему `publish_rate` читается в `timer_callback`, а не один раз в `__init__`?
2. Что произойдет, если убрать `declare_parameter` и оставить только `get_parameter`?
3. Где в `setup.py` настраивается копирование `launch/` и `config/` при сборке?
4. Чем отличается запуск через `ros2 run` от запуска через `ros2 launch`?

---

## Типичные ошибки

| Симптом | Причина | Исправление |
| --- | --- | --- |
| `ros2 launch` не находит файл | Launch не установлен в `setup.py` | Добавить `data_files` → `launch/*.launch.py` в `setup.py` |
| YAML не применяется | Config не установлен в `setup.py` | Добавить `data_files` → `config/*.yaml` в `setup.py` |
| `ros2 param set` не меняет поведение | Параметр прочитан один раз в `__init__` | Читать `get_parameter()` в callback |
| `ros2 param list` не показывает параметр | `declare_parameter` не вызван | Добавить `self.declare_parameter(...)` в `__init__` |
| Параметр не меняется после `set` | Параметр используется для вычислений в `__init__` (например, период таймера) | Пересоздать таймер в callback или использовать переменную частоту как в примере |

---

## Дополнительное задание

1. **Добавьте аргумент в launch**: `publish_rate` как аргумент командной строки (`DeclareLaunchArgument`). Запустите с разными значениями:

```bash
ros2 launch launch_demo talker.launch.py publish_rate:=10.0
```

2. **Добавьте второй узел** `logger` в тот же launch-файл — subscriber для `/chatter` с параметром `log_level` (debug/info/warn).

3. **Создайте YAML с параметрами для двух узлов** — отдельные секции для `timed_talker` и `logger`.

---

## Ссылки

- [Parameters — статья базы знаний](../2_knowledge/parameters.md)
- [Launch — статья базы знаний](../2_knowledge/launch.md)
- [Using parameters in a class](https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Using-Parameters-In-A-Class-Python.html)
- [Creating a launch file](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Launch/Creating-Launch-Files.html)