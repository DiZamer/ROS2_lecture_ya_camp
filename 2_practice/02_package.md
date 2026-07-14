# Практика: Первый пакет и узел

## Цель

Создать Python-пакет `my_first_pkg` через `ros2 pkg create`, написать узел `my_node` с таймером (печатает `Tick #N` каждую секунду), настроить точку входа `entry_points` в `setup.py` для запуска через `ros2 run`, собрать `colcon build` и проверить в `ros2 node list` / `rqt_graph`.

## Предварительные требования

- Выполнена [практика 01_workspace](01_workspace.md)
- Workspace `~/ros2_ws` создан и активирован

## Что получится

- Пакет `my_first_pkg` (ament_python) в `~/ros2_ws/src/`
- Узел `my_node` (класс `MyNode` на Python): создаёт таймер 1.0 с, по каждому срабатыванию инкрементирует счётчик и выводит `Tick #N` в лог
- Точка входа `my_node = my_first_pkg.my_node:main` в `setup.py` — связывает команду `ros2 run my_first_pkg my_node` с функцией `main()`
- Узел виден в `ros2 node list` как `/my_node` и отображается в `rqt_graph`

---

## Шаг 1. Создать пакет

```bash
cd ~/ros2_ws/src
ros2 pkg create --build-type ament_python my_first_pkg --dependencies rclpy
```

Проверить структуру:

```bash
tree my_first_pkg
```

Ожидаемый вывод:

```
my_first_pkg/
├── my_first_pkg/
│   └── __init__.py
├── package.xml
├── setup.cfg
├── setup.py
└── resource/
    └── my_first_pkg
```

---

## Шаг 2. Написать узел

Создать файл `my_first_pkg/my_node.py`:

```python
import rclpy                         # ROS2 Python-клиент: init, spin, shutdown
from rclpy.node import Node          # Базовый класс для любого узла ROS2


class MyNode(Node):
    """Узел с таймером: каждую секунду инкрементирует счётчик и пишет в лог"""

    def __init__(self):
        super().__init__('my_node')  # Регистрируем узел с именем 'my_node' в ROS Graph
        self.count = 0
        # Таймер — вызывает timer_callback() каждые 1.0 секунды
        # Без rclpy.spin() в main() таймер никогда не сработает
        self.timer = self.create_timer(1.0, self.timer_callback)
        self.get_logger().info('Node started')

    def timer_callback(self):
        """Вызывается таймером каждую секунду"""
        self.count += 1
        self.get_logger().info(f'Tick #{self.count}')


def main(args=None):
    rclpy.init(args=args)             # Инициализация ROS2: подключается к DDS
    node = MyNode()                   # Создаём узел — регистрируется в ROS Graph
    rclpy.spin(node)                  # Цикл обработки событий: без него callbacks не работают
    node.destroy_node()               # Корректное завершение узла
    rclpy.shutdown()                  # Отключение от DDS
```

---

## Шаг 3. Настроить точку входа

Отредактировать `setup.py` в папке `my_first_pkg/` — добавить `entry_points` (эта секция связывает команду `ros2 run my_first_pkg my_node` с функцией `main()` в файле `my_node.py`):

```python
from setuptools import setup

package_name = 'my_first_pkg'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Student',
    maintainer_email='student@example.com',
    description='My first ROS2 package',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            # Формат: 'команда = пакет.файл:функция'
            # ros2 run my_first_pkg my_node → вызывает my_first_pkg.my_node:main()
            'my_node = my_first_pkg.my_node:main',
        ],
    },
)
```

---

## Шаг 4. Собрать пакет

```bash
cd ~/ros2_ws
colcon build --packages-select my_first_pkg
```

Ожидаемый вывод:

```
Starting >>> my_first_pkg
Finished <<< my_first_pkg [< 2s]
Summary: 1 package finished [< 3s]
```

Активировать workspace:

```bash
source ~/ros2_ws/install/setup.bash
```

---

## Шаг 5. Запустить узел

```bash
ros2 run my_first_pkg my_node
```

Ожидаемый вывод:

```
[INFO] [my_node]: Node started
[INFO] [my_node]: Tick #1
[INFO] [my_node]: Tick #2
[INFO] [my_node]: Tick #3
...
```

Остановить: `Ctrl+C`.

---

## Шаг 6. Проверить узел в системе

Оставить узел запущенным, открыть второй терминал:

```bash
# Список узлов
ros2 node list
# Вывод: /my_node

# Информация об узле
ros2 node info /my_node
# Вывод: показывает подписки, публикации, сервисы, параметры

# Визуализация ROS Graph
rqt_graph
# Показывает один узел /my_node
```

---

## Проверка результата

| Команда | Ожидаемый результат |
| --- | --- |
| `ros2 run my_first_pkg my_node` | Узел печатает `Tick #N` каждую секунду |
| `ros2 node list` | `/my_node` в списке |
| `ros2 node info /my_node` | Информация об узле |
| `rqt_graph` | Визуализация: один узел `/my_node` |

---

## Вопросы студентам

1. Что произойдет, если убрать `rclpy.spin(node)` из `main()`?
2. Почему `source install/setup.bash` нужно выполнять после каждой сборки?
3. Где в `setup.py` задается связь между командой `ros2 run my_first_pkg my_node` и файлом `my_node.py`?
4. Можно ли запустить два экземпляра одного узла? Что произойдет, если попробовать?

---

## Типичные ошибки

| Симптом | Причина | Исправление |
| --- | --- | --- |
| `ros2 run` не находит команду | Не обновлен `entry_points` в `setup.py` | Проверить секцию `console_scripts` в `setup.py` |
| Узел запускается и сразу завершается | Забыли `rclpy.spin(node)` | Добавить `spin()` в `main()` |
| `ModuleNotFoundError: No module named 'my_first_pkg'` | Забыли `source setup.bash` | `source ~/ros2_ws/install/setup.bash` |
| Два экземпляра узла — ошибка | Имена узлов должны быть уникальны | Использовать разные имена в `__init__` |
| Изменения кода не применяются | Старая версия в `install/` | Пересобрать (`colcon build`) или использовать `--symlink-install` |

---

## Дополнительное задание

1. Измените частоту таймера с 1.0 на 0.5 секунд, пересоберите и проверьте.
2. Добавьте второй узел `another_node` в тот же пакет — с другим именем и сообщением в логе. Не забудьте `entry_points`.
3. Запустите оба узла одновременно:

```bash
ros2 run my_first_pkg my_node &
ros2 run my_first_pkg another_node &
```

Проверьте `ros2 node list` и `rqt_graph` — должны быть видны оба узла.

---

## Ссылки

- [Nodes — статья базы знаний](../2_knowledge/nodes.md)
- [Пакеты — статья базы знаний](../2_knowledge/packages.md)
- [colcon — статья базы знаний](../2_knowledge/colcon.md)
- [Writing a simple publisher and subscriber](https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Py-Publisher-And-Subscriber.html)