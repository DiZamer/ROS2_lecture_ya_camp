# Пакеты в ROS2

## Коротко

Package — минимальная единица организации кода в ROS2. Один пакет решает одну задачу: драйвер камеры, навигация, детектор объектов.

> *Официальное определение*: «Пакет — это организационная единица вашего кода ROS 2.» — [Packages](https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Creating-Your-First-ROS2-Package.html)

## Что такое package

Пакет — папка со строго определенной структурой:

```text
my_first_pkg/
├── package.xml            # метаданные: имя, версия, зависимости, лицензия
├── setup.py               # инструкция для установки Python-пакета
├── setup.cfg              # конфигурация установки
├── resource/
│   └── my_first_pkg       # маркерный файл (aament Python)
└── my_first_pkg/          # исходный код
    ├── __init__.py
    └── my_node.py         # узел
```

### package.xml

Файл, в котором объявляются метаданные пакета:

```xml
<?xml version="1.0"?>
<package format="3">
  <name>my_first_pkg</name>
  <version>0.0.1</version>
  <description>My first ROS2 package</description>
  <maintainer email="student@example.com">Student</maintainer>
  <license>Apache-2.0</license>

  <buildtool_depend>ament_python</buildtool_depend>

  <depend>rclpy</depend>
  <depend>std_msgs</depend>

  <test_depend>ament_copyright</test_depend>
  <test_depend>ament_flake8</test_depend>
  <test_depend>ament_pep257</test_depend>

  <export>
    <build_type>ament_python</build_type>
  </export>
</package>
```

### setup.py — точка входа

ROS2 должен знать, какой Python-файл запускать как узел. Это настраивается в `setup.py` через `entry_points`:

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
            'my_node = my_first_pkg.my_node:main',
            # формат: 'имя_команды = имя_пакета.имя_файла:имя_функции'
        ],
    },
)
```

После этого узел запускается командой:

```bash
ros2 run my_first_pkg my_node
```

## Зачем нужно

Пакет группирует код, зависимости и конфигурацию в одну единицу. Без пакетов ROS2-проект превращается в мешанину файлов, которую невозможно собрать и запустить.

Каждый пакет компилируется или устанавливается независимо. Можно обновить пакет камеры, не трогая навигацию.

## Аналогия

Пакет — **папка-проект** внутри большого workspace. Как папка с исходниками одной программы в monorepo: у нее свой `package.json` (аналог `package.xml`), свой список зависимостей и свои точки входа.

## ament_python vs ament_cmake

| | `ament_python` | `ament_cmake` |
| --- | --- | --- |
| Язык | Python | C++ |
| Сборка | `setup.py` (setuptools) | `CMakeLists.txt` + CMake |
| Использование в курсе | **Основной** — все примеры | Только ссылкой |
| Создание | `ros2 pkg create --build-type ament_python pkg_name` | `ros2 pkg create --build-type ament_cmake pkg_name` |

**В курсе используется `ament_python`.** Python проще для первого знакомства с ROS2 API. Студенты, знающие C++, могут изучить `ament_cmake` самостоятельно по официальной документации.

## Создание пакета

```bash
cd ~/ros2_ws/src

# Создать пакет
ros2 pkg create --build-type ament_python my_pkg

# С зависимостями
ros2 pkg create --build-type ament_python my_pkg \
  --dependencies rclpy std_msgs
```

Команда создает папку `my_pkg/` со всей структурой: `package.xml`, `setup.py`, `setup.cfg`, папка исходников.

## Установка зависимостей

Зависимости, объявленные в `package.xml`, устанавливаются через `rosdep`:

```bash
rosdep update
rosdep install --from-paths ~/ros2_ws/src --ignore-src -r -y
```

`rosdep` читает `package.xml` каждого пакета в `src/` и устанавливает все зависимости через `apt`.

## Типичные ошибки

| Ошибка | Симптом | Исправление |
| --- | --- | --- |
| Забыли `--build-type` | Пакет создан как `ament_cmake` по умолчанию | Удалить и создать заново с `--build-type ament_python` |
| Имя пакета не совпадает с именем папки | `colcon build` предупреждает | Название в `package.xml` должно совпадать с именем папки |
| Не обновили `entry_points` | `ros2 run` не находит узел | Добавить запись в `entry_points` → `console_scripts` в `setup.py` |
| Узел создан, но `spin()` не вызван | Узел запускается и сразу завершается | Проверить, что в функции `main()` есть `rclpy.spin()` |
| Зависимость не объявлена в `package.xml` | `colcon build` падает с ImportError | Добавить `<depend>имя_пакета</depend>` в `package.xml` |

### Пример в реальном роботе

TIAGo содержит **64 пакета** из 18 репозиториев PAL Robotics: пакеты симуляции, контроллеров, навигации, манипуляции, сенсоров.
В [`3_Robot/TIAgo_humble/docs/tiago_architecture.md`](../../3_Robot/TIAgo_humble/docs/tiago_architecture.md) показана карта подсистем
и распределение пакетов по слоям: планирование, координация, сенсоры.

## Связанные темы

- [Workspace и окружение](workspace.md) — где создать пакет
- [colcon](colcon.md) — сборка пакета
- [Nodes](nodes.md) — код внутри пакета
- [Topics](topics.md) — обмен сообщениями

## Источники

- [Creating a package](https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Creating-Your-First-ROS2-Package.html)
- [ament_python documentation](https://docs.ros.org/en/jazzy/How-To-Guides/Ament-CMake-Python-Documentation.html)