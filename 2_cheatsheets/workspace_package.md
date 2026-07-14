# Шпаргалка: Workspace и Package

## Создание workspace

```bash
mkdir -p ~/ros2_ws/src && cd ~/ros2_ws
# Создать пакет
ros2 pkg create --build-type ament_python <name> --dependencies rclpy std_msgs
# Собрать
colcon build && source install/setup.bash
```

## Структура пакета ament_python

```
my_pkg/
├── package.xml                # метаданные, зависимости
├── setup.py                   # точки входа (entry_points)
├── setup.cfg                  # конфигурация установки
├── resource/
│   └── my_pkg                 # маркерный файл
└── my_pkg/
    ├── __init__.py
    └── my_node.py             # код узла
```

## package.xml — минимальный

```xml
<package format="3">
  <name>my_pkg</name>
  <version>0.0.1</version>
  <buildtool_depend>ament_python</buildtool_depend>
  <depend>rclpy</depend>
  <depend>std_msgs</depend>
  <export><build_type>ament_python</build_type></export>
</package>
```

## setup.py — entry_points

```python
entry_points={
    'console_scripts': [
        'my_node = my_pkg.my_node:main',
        # формат: команда = пакет.файл:функция
    ],
},
```

## setup.py — data_files (для launch и config)

```python
import os
from glob import glob

data_files=[
    # ... стандартные ...
    (os.path.join('share', package_name, 'launch'),
        glob('launch/*.launch.py')),
    (os.path.join('share', package_name, 'config'),
        glob('config/*.yaml')),
],
```

## Шаблон узла

```python
import rclpy
from rclpy.node import Node

class MyNode(Node):
    def __init__(self):
        super().__init__('my_node')
        self.get_logger().info('Started')

def main(args=None):
    rclpy.init(args=args)
    node = MyNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
```

## Добавление зависимостей

```xml
<!-- В package.xml -->
<depend>std_msgs</depend>
<depend>geometry_msgs</depend>
<depend>example_interfaces</depend>
<depend>std_srvs</depend>
<depend>tf2_ros</depend>
```

## Сборка

```bash
colcon build                    # все пакеты
colcon build --packages-select my_pkg   # один пакет
colcon build --symlink-install  # пересборка не нужна (Python)

# После сборки всегда:
source ~/ros2_ws/install/setup.bash
echo "source ~/ros2_ws/install/setup.bash" >> ~/.bashrc
```