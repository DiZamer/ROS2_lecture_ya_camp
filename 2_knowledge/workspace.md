# Workspace в ROS2

## Коротко

Workspace — папка, где лежат исходники пакетов и результаты их сборки. Работа идет в контейнере — ROS2 не устанавливается на хост.

> *Официальное определение*: «Workspace — это директория, содержащая пакеты ROS 2.» — [Workspace](https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Creating-A-Workspace/Creating-A-Workspace.html)

## Что такое workspace

Workspace (рабочее пространство) — корневая папка ROS2-проекта. Внутри:

| Папка | Назначение | Кто создает |
| --- | --- | --- |
| `src/` | Исходные коды пакетов | Вы |
| `build/` | Промежуточные файлы сборки | `colcon build` |
| `install/` | Готовые к запуску артефакты | `colcon build` |
| `log/` | Логи сборки | `colcon build` |

**Не редактируйте `build/`, `install/`, `log/` вручную.** Эти папки создает и управляет ими `colcon`.

## Зачем нужно

Workspace отделяет исходный код от результатов сборки. Вы работаете только в `src/`. Сборка, зависимости, окружение — все изолировано в рамках workspace.

Несколько workspace могут сосуществовать независимо — например, один для учебных примеров, другой для проекта робота.

## Аналогия

Workspace — **мастерская**:
- `src/` — чертежи и детали;
- `colcon build` — сборка изделия;
- `install/` — готовая продукция на складе;
- `source install/setup.bash` — вы берете изделие со склада и кладете на верстак.

## Контейнерная среда

ROS2 **не устанавливается на хост**. Вся работа — внутри Dev Container:

```
Хост (ваш компьютер)
└── Docker
    └── Dev Container (Ubuntu 24.04 + ROS2 Jazzy)
        └── Terminal → ros2 ...
```

Такой подход гарантирует:
- одинаковое окружение у всех студентов;
- изоляцию — ROS2 не конфликтует с программами хоста;
- воспроизводимость — контейнер можно пересоздать за минуты.

## Проверка окружения

Перед созданием workspace убедитесь, что ROS2 работает:

```bash
# Справка по CLI
ros2 --help

# Запуск демонстрационного узла
ros2 run demo_nodes_cpp talker
# Ожидаемый вывод: [INFO] [...] Publishing: 'Hello World: 1'

# Диагностика окружения
ros2 doctor --report

# Проверка используемого DDS
printenv RMW_IMPLEMENTATION
# Ожидаемый вывод: rmw_fastrtps_cpp (по умолчанию в Jazzy)
```

## Создание workspace

```bash
# Создать папку src внутри workspace
mkdir -p ~/ros2_ws/src

# Перейти в workspace
cd ~/ros2_ws

# Проверить структуру
ls
# Вывод: src
```

На этом этапе workspace пуст — в `src/` еще нет пакетов. Пакеты создаются через `ros2 pkg create` (см. [Пакеты](packages.md)).

## Сборка workspace

```bash
# Находясь в корне workspace (~/ros2_ws):
colcon build
# Вывод: Summary: 0 packages finished (если src/ пуст)

# После сборки появляются папки build/, install/, log/
ls
# Вывод: build install log src
```

## Активация workspace

После сборки нужно активировать workspace, чтобы ROS2 видел ваши пакеты:

```bash
source ~/ros2_ws/install/setup.bash
```

**Без этой команды** ваши пакеты не видны для `ros2 run`, `ros2 pkg list` и других команд.

Автоматизируйте активацию — добавьте в `~/.bashrc`:

```bash
echo "source ~/ros2_ws/install/setup.bash" >> ~/.bashrc
```

Теперь при каждом открытии терминала workspace будет активирован.

## Типичные ошибки

| Ошибка | Симптом | Исправление |
| --- | --- | --- |
| Забыли `source setup.bash` | `ros2 pkg list` не показывает ваш пакет | `source ~/ros2_ws/install/setup.bash` |
| Пакет создан не в `src/` | `colcon build` не видит пакет | Переместить пакет в `~/ros2_ws/src/` |
| Команда `ros2` не найдена | `bash: ros2: command not found` | Контейнер не запущен или не пересобран |
| `colcon build` вызывается не из корня workspace | Ошибка сборки | `cd ~/ros2_ws && colcon build` |

### Пример в реальном роботе

TIAGo workspace (`ros2_ws/`) содержит 64 пакета из 18 репозиториев PAL Robotics.
В [`3_Robot/TIAgo_humble/docs/tiago_architecture.md`](../../3_Robot/TIAgo_humble/docs/tiago_architecture.md) показана
структура workspace, источники пакетов (`fetch_external.sh`) и порядок сборки в контейнере.

## Связанные темы

- [Пакеты](packages.md) — создание и устройство пакетов
- [colcon](colcon.md) — детально о сборке
- [Nodes](nodes.md) — написание первого узла
- [Topics](topics.md) — обмен сообщениями

## Источники

- [Creating a workspace](https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Creating-A-Workspace/Creating-A-Workspace.html)
- [ROS2 Jazzy Installation](https://docs.ros.org/en/jazzy/Installation.html)