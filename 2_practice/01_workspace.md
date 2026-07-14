# Практика: Первый workspace

## Цель

Научиться открывать Dev Container с ROS2 Jazzy, проверить окружение (CLI, демо-узлы, middleware), создать пустой workspace `~/ros2_ws` и выполнить первую сборку через `colcon build`.

## Предварительные требования

- Установлены Docker и VS Code с расширением Dev Containers
- Проект открыт в VS Code (`File → Open Folder → ROS2_course/`)

## Что получится

- Работающий ROS2 Jazzy внутри контейнера
- Проверка CLI (`ros2 --help`), запуск демо-узла `demo_nodes_cpp talker` (публикует `std_msgs/String` в `/chatter`)
- Диагностика окружения через `ros2 doctor`
- Созданный workspace `~/ros2_ws` с папкой `src/` и результат `colcon build` (папки `build/`, `install/`, `log/`)

## Шаг 1. Открыть Dev Container

```bash
# В VS Code: Ctrl+Shift+P → «Dev Containers: Rebuild and Reopen in Container»
# Эта команда запускает сборку Docker-образа по .devcontainer/Dockerfile
# Внутри образа: Ubuntu 24.04 + ROS2 Jazzy + все зависимости курса
# Первый раз — несколько минут, последующие — секунды
```

После открытия контейнера в терминале VS Code доступен ROS2.

## Шаг 2. Проверить ROS2

Проверяем, что CLI ROS2 работает и может запускать узлы:

```bash
# Справка по всем подкомандам ROS2 CLI
# Если команда выполняется — ROS2 установлен и настроен
ros2 --help
```

Ожидаемый вывод: справка по `ros2` CLI с перечислением доступных подкоманд (`run`, `topic`, `service`, `action`, `node`, ...).

```bash
# Запускаем готовый демо-узел talker из пакета demo_nodes_cpp
# Этот узел каждую секунду публикует std_msgs/String в топик /chatter
# (аналог того, что мы сами напишем в практиках 02-03)
ros2 run demo_nodes_cpp talker
```

Ожидаемый вывод:

```
[INFO] [talker]: Publishing: 'Hello World: 1'
[INFO] [talker]: Publishing: 'Hello World: 2'
[INFO] [talker]: Publishing: 'Hello World: 3'
...
```

Остановить: `Ctrl+C`.

## Шаг 3. Проверить middleware

Проверяем, какой DDS используется и нет ли проблем с окружением:

```bash
# Диагностика окружения — проверяет RMW, discovery, clock sync, network
# Если есть ошибки — ros2 doctor подскажет причину
ros2 doctor --report

# Какой DDS используется (RMW — ROS Middleware Wrapper)
# В ROS2 Jazzy по умолчанию Fast DDS (rmw_fastrtps_cpp)
printenv RMW_IMPLEMENTATION
```

Ожидаемый вывод: `rmw_fastrtps_cpp` (Fast DDS по умолчанию в ROS2 Jazzy).

## Шаг 4. Создать workspace

```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws
ls
```

Ожидаемый вывод:

```
src
```

## Шаг 5. Первая сборка (пустой workspace)

`colcon build` — главная команда сборки ROS2-проекта. Она обходит все пакеты в `src/`, собирает их и раскладывает результаты:

```bash
cd ~/ros2_ws
colcon build
# colcon (collective construction) — мета-инструмент сборки
# Собирает все пакеты в src/ в порядке зависимостей
# Результат: build/ (объектные файлы), install/ (готовые пакеты), log/ (логи)
```

Ожидаемый вывод:

```
Summary: 0 packages finished [< 1s]
```

После сборки появляются папки `build/`, `install/`, `log/`:

```bash
ls ~/ros2_ws
```

Ожидаемый вывод:

```
build  install  log  src
```

**Назначение папок:**
- `build/` — временные файлы компиляции (не трогать)
- `install/` — собранные пакеты, готовые к запуску (source отсюда)
- `log/` — логи сборки (читать при ошибках)
- `src/` — исходный код пакетов (только эту папку редактируем)

## Шаг 6. Активировать workspace

После сборки пакеты лежат в `install/`, но ROS2 о них ещё не знает. `source setup.bash` добавляет пути в `PATH`, `PYTHONPATH`, `AMENT_PREFIX_PATH`:

```bash
# Активация workspace — добавляет пути к install/ в переменные окружения
# Без этого ros2 run не найдёт ваши пакеты
source ~/ros2_ws/install/setup.bash
```

Чтобы не делать это каждый раз при открытии терминала:

```bash
# Добавляем source в .bashrc — будет активироваться автоматически
echo "source ~/ros2_ws/install/setup.bash" >> ~/.bashrc
```

## Проверка результата

| Команда | Ожидаемый результат |
| --- | --- |
| `ros2 --help` | Справка по CLI |
| `ros2 run demo_nodes_cpp talker` | Узел печатает «Hello World» |
| `ros2 doctor --report` | Диагностика без ошибок |
| `printenv RMW_IMPLEMENTATION` | `rmw_fastrtps_cpp` |
| `ls ~/ros2_ws` | `build install log src` |

## Вопросы студентам

1. Зачем мы работаем в контейнере, а не устанавливаем ROS2 на хост?
2. Что делает команда `ros2 doctor --report`?
3. Что лежит в папках `build/`, `install/`, `log/`?

## Типичные ошибки

| Симптом | Причина | Исправление |
| --- | --- | --- |
| `bash: ros2: command not found` | Контейнер не запущен или не пересобран | `Ctrl+Shift+P → Rebuild Container` |
| `colcon build` не в корне workspace | Команда вызвана из другой папки | `cd ~/ros2_ws && colcon build` |
| `ros2 run demo_nodes_cpp talker` — пакет не найден | Не установлены `ros-jazzy-demo-nodes-cpp` | Пересобрать контейнер |

## Ссылки

- [Workspace в ROS2](../2_knowledge/workspace.md) — подробная статья
- [Пакеты](../2_knowledge/packages.md) — следующий шаг
- [Creating a workspace](https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Creating-A-Workspace/Creating-A-Workspace.html)