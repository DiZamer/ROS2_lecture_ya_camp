# Архитектура TIAGo

TIAGo (Take It And Go) — полнофункциональный мобильный манипулятор PAL Robotics. В этом проекте реализована **виртуальная модель робота** в симуляции Gazebo Classic 11 с полным ROS2-стеком.

> Связь с теорией: [`2_knowledge/ros_architecture.md`](../../2_knowledge/ros_architecture.md) — общая архитектура ROS2, [`2_knowledge/subsystem.md`](../../2_knowledge/subsystem.md) — принцип деления робота на подсистемы.
>
> Подробная конфигурация проекта (пакеты, команды, аргументы): [`TIAgo_configuration.md`](../TIAgo_configuration.md).

---

## Карта подсистем

```
┌──────────────────────────────────────────────────────────────────┐
│                        ПОЛЬЗОВАТЕЛЬ                               │
│  teleop_twist_keyboard │ RViz2 │ CLI (ros2 topic/action/service)  │
└────────────┬──────────────────────────────┬───────────────────────┘
             │                              │
             ▼                              ▼
┌────────────────────────┐  ┌──────────────────────────────────────┐
│  ПЛАНИРОВАНИЕ           │  │  ВОСПРИЯТИЕ                          │
│  Nav2 (planner+DWB+BT)  │  │  YOLO detection                      │
│  MoveIt2 (move_group)   │  │  RGB-D камера + LiDAR                │
│  play_motion2           │  │  /detections → /camera/image_raw     │
│  AMCL / slam_toolbox    │  │                                       │
└────────┬───────────────┬─┘  └──────────────┬──────────────────────┘
         │               │                    │
         ▼               ▼                    ▼
┌──────────────────────────────────────────────────────────────────┐
│  КООРДИНАЦИЯ                                                        │
│  twist_mux (4 приоритета) │ velocity_smoother │ costmaps          │
│  controller_manager (ros2_control)                                 │
│  DiffDriveController │ arm_controller │ torso/head/gripper         │
└──────────────────────────────────────────────────────────────────┘
         │                    │                    │
         ▼                    ▼                    ▼
┌──────────────────────────────────────────────────────────────────┐
│  СЕНСОРЫ И СИМУЛЯЦИЯ                                               │
│  Gazebo Classic 11 │ LiDAR (/scan) │ camera (/image_raw)          │
│  IMU │ FT sensor │ joint_state_broadcaster                        │
└──────────────────────────────────────────────────────────────────┘
```

**Цветовая маркировка:**
- 🟦 Пользовательский слой — управление
- 🟩 Планирование — высокоуровневая логика
- 🟧 Координация — стык логики и управления
- 🟥 Сенсоры/симуляция — физический мир

---

## Путеводитель по архитектуре

Пошаговое знакомство с TIAGo. Каждый шаг: действие → что смотреть → что проверить.
Ссылки ведут в `docs/` (детальное описание) и `2_knowledge/` (теория).

### Шаг 1. Живой робот

Запустите симуляцию и увидьте робота в Gazebo и RViz:

```bash
start_gui.sh                                          # терминал 1: noVNC
ros2 launch tiago_gazebo tiago_gazebo.launch.py is_public_sim:=True   # терминал 2
```

**Что смотреть:**
- Gazebo (http://localhost:6080) — робот в мире pal_office
- RViz (там же, вкладка) — модель, TF-дерево, лазерные лучи

**Что проверить:**
- Робот стоит на поверхности, не проваливается
- В RViz есть лазерные лучи (`/scan`)
- TF-дерево не пустое

**Типичная ошибка:** `start_gui.sh` не запущен — RViz и Gazebo открываются, но висят в Xvfb.
**→ Дальше:** [simulation.md](simulation.md) — детали Gazebo.

---

### Шаг 2. Кто в графе

Узнайте, из каких узлов состоит система:

```bash
ros2 node list                    # все живые узлы
rqt_graph                         # визуальный граф связей
ros2 topic list                   # все топики
ros2 service list                 # все сервисы
```

**Что смотреть:**
- `rqt_graph` показывает, какие узлы общаются через какие топики
- Сколько узлов в системе? (базовый запуск ~15 узлов)
- Найдите: `robot_state_publisher`, `controller_manager`, `DiffDriveController`, `twist_mux`

**Что проверить:**
- Все ожидаемые узлы в списке? Если нет — запуск неполный
- Есть ли узлы с состоянием `ERROR`?

**Типичная ошибка:** `rqt_graph` пуст — забыли `source install/setup.bash` в новом терминале, или нет активных publisher/subscriber.
**→ Дальше:** [launch_params.md](launch_params.md) — как запускаются узлы.

---

### Шаг 3. Анатомия робота

TIAGo — это 7-DOF манипулятор на дифференциальной базе с RGB-D камерой, LiDAR и тактильным датчиком. Посмотрите, из каких частей он состоит:

```bash
ros2 run tf2_tools view_frames    # PDF дерева координат
ros2 topic echo /robot_description --once | head -50 | xmllint --format -
                                    # URDF-модель (первые 50 строк)
ros2 topic echo /joint_states --once  # текущие углы суставов
```

**Что смотреть:**
- `base_link` — корневой фрейм, всё крепится к нему
- 7 суставов руки: `arm_1_link` → `arm_7_link`
- `torso_lift_link` — выдвижной торс (ход 35 см)
- `camera_link` — RGB-D на голове
- `base_laser_link` — лазерный сканер

**Что проверить:**
- Дерево TF не обрывается — все фреймы соединены
- `joint_states` показывает текущие углы всех суставов

**Типичная ошибка:** `view_frames` падает с `Could not find tf2_tools` — пакет `tf2_tools` не установлен в контейнере (`sudo apt install ros-humble-tf2-tools`).
**→ Дальше:** [robot_model.md](robot_model.md), [tf_frames.md](tf_frames.md).

---

### Шаг 4. Мышцы — ros2_control

ros2_control — слой, который превращает ROS2-команды в движение приводов:

```bash
ros2 control list_controllers                     # активные контроллеры
ros2 control list_hardware_interfaces              # hardware interfaces
ros2 topic echo /cmd_vel_unstamped --once          # команда скорости
```

**Что смотреть:**
- `DiffDriveController` — принимает `/cmd_vel`, вращает колёса, публикует `/odom`
- `arm_controller` — JointTrajectoryController для 7 суставов руки
- `torso_controller` — управление высотой торса
- `gripper_controller` — открытие/закрытие пальцев

**Что проверить:**
- `ros2 control list_controllers` показывает все контроллеры в состоянии `active`
- Если контроллер в `inactive` — нужен вызов `lifecycle_manager`

**→ Дальше:** [ros2_control.md](ros2_control.md).

---

### Шаг 5. Нервная система — RMW и DDS

ROS2 передаёт данные через DDS. TIAGo использует CycloneDDS:

```bash
printenv RMW_IMPLEMENTATION          # текущий middleware (должен быть rmw_cyclonedds_cpp)
ros2 doctor                           # диагностика системы
ros2 doctor --report                  # полный отчёт
```

**Что смотреть:**
- `RMW_IMPLEMENTATION=rmw_cyclonedds_cpp` — это рекомендованный PAL Robotics vendor
- `ros2 doctor` проверяет: RMW, discovery, network, clock sync

**Что проверить:**
- middleware стабилен — узлы видят друг друга
- `ros2 doctor` не выдаёт ошибок discovery

**Расширяющий материал:**
Почему CycloneDDS, а не Fast DDS (дефолтный)? У PAL Robotics долгая история работы с Cyclone DDS; он показал лучшую стабильность на multi-robot сценариях и в конфигурациях с несколькими сетевыми интерфейсами. В контейнере это зафиксировано через `RMW_IMPLEMENTATION` в `.bashrc`.

**→ Дальше:** [rmw_dds.md](rmw_dds.md).

---

### Шаг 6. Надёжность — QoS

Каждый топик в TIAGo использует свои QoS-настройки:

```bash
ros2 topic info /scan --verbose       # QoS лазера
ros2 topic info /cmd_vel --verbose    # QoS команд скорости
ros2 topic info /head_front_camera/rgb/image_raw --verbose  # QoS видео
```

**Что смотреть:**
- `/scan` — `BEST_EFFORT` (терять кадры не страшно, следующий через 0.1 с)
- `/cmd_vel` — `RELIABLE` (нельзя терять команду)
- `/camera/image_raw` — `BEST_EFFORT` (потоковый, потеря кадра ок)

**Что проверить:**
- pub/sub совместимы по QoS — иначе не соединятся
- Разные QoS для `/scan_raw` (сырой) и `/scan` (фильтрованный)

**→ Дальше:** [qos_profiles.md](qos_profiles.md).

---

### Шаг 7. Как робот едет — Nav2

Запустите навигацию и отправьте робота в точку на карте:

```bash
# Терминал 1: симуляция с навигацией
ros2 launch tiago_gazebo tiago_gazebo.launch.py navigation:=True is_public_sim:=True

# В RViz: 2D Pose Estimate (указать позицию) → Navigation2 Goal (указать цель)
# Терминал 2: посмотреть action
ros2 action info /navigate_to_pose
```

**Что смотреть:**
- RViz показывает: карту, AMCL-частицы (зелёные стрелки), costmap (цветные зоны), путь (зелёная линия)
- Робот строит маршрут, объезжает препятствия
- В `/cmd_vel` приходят сглаженные команды скорости

**Что проверить:**
- Робот едет к цели и останавливается
- Если поставить препятствие в Gazebo (Insert → модели → Construction Cone) — робот перестраивает маршрут

**Типичная ошибка:** Нет `ros-humble-nav2-bringup` — доустановить в контейнере.
**→ Дальше:** [navigation.md](navigation.md).

---

### Шаг 8. Как робот берёт предметы — MoveIt2

Запустите манипуляцию и пошевелите рукой:

```bash
# Терминал 1: симуляция с MoveIt2
ros2 launch tiago_gazebo tiago_gazebo.launch.py moveit:=True is_public_sim:=True

# Терминал 2: RViz с MotionPlanning
ros2 launch tiago_moveit_config moveit_rviz.launch.py

# Терминал 3: активировать панель (загрузить URDF в RViz)
RVN=$(ros2 node list | grep rviz | tail -1) && \
ros2 param set "$RVN" robot_description "$(ros2 topic echo /robot_description --once --field data 2>/dev/null)"
```

**Что смотреть:**
- MoveIt RViz: оранжевый шар на эндекторе, панель MotionPlanning
- Планирование: перетащить → Plan → Execute
- Рука двигается в симуляции

**Что проверить:**
- Планирование успешно (жёлтая траектория)
- Execute двигает руку в Gazebo

**Типичная ошибка:** RViz без MotionPlanning — не активировали панель (третья команда).
**→ Дальше:** [manipulation.md](manipulation.md).

---

### Шаг 9. Безопасность

У TIAGo несколько уровней защиты:

```bash
# E-stop через сервис
ros2 service call /emergency_stop std_srvs/srv/Trigger

# twist_mux — приоритеты команд скорости
ros2 topic echo /mobile_base_controller/cmd_vel_unstamped

# Battery
ros2 topic echo /battery_state
```

**Что смотреть:**
- twist_mux имеет 4 уровня приоритетов (навигация < телеоп < безопасность < E-stop)
- E-stop блокирует все команды скорости

**Расширяющий материал:**
Патч `twist_mux.py` комментирует `diagnostic_aggregator` (ROS1-пакет, который не портирован на Humble) — это пример, как в production обходят отсутствующие зависимости без изменения чужого кода.

**→ Дальше:** [safety.md](safety.md), [lifecycle_nodes.md](lifecycle_nodes.md).

---

### Шаг 10. Полный стек

Всё вместе — навигация + манипуляция:

```bash
ros2 launch tiago_gazebo tiago_gazebo.launch.py \
    navigation:=True moveit:=True is_public_sim:=True
```

Робот может одновременно ехать к цели и планировать движение руки. В системе работают все узлы из шагов 1–9.

**Что проверить:**
- Два RViz: навигационный (карта + costmap) и MoveIt (MotionPlanning)
- Цели навигации и манипуляции работают параллельно и не мешают друг другу

---

## Подсистемы и слои — карта файлов

| Файл | Уровень | Технологии | Связь с `2_knowledge/` |
|---|---|---|---|
| [`navigation.md`](navigation.md) | Подсистема | Nav2, AMCL, SLAM, costmaps | `nav2_bridge.md` |
| [`manipulation.md`](manipulation.md) | Подсистема | MoveIt2, OMPL, play_motion2 | `moveit2_bridge.md` |
| [`perception.md`](perception.md) | Подсистема | YOLO, cv_bridge, vision_msgs | `yolo_bridge.md` |
| [`llm_bridge.md`](llm_bridge.md) | Подсистема | OpenAI API, play_motion2, Nav2 | `llm_bridge.md` |
| [`safety.md`](safety.md) | Подсистема | twist_mux, E-stop, battery | `safety.md` |
| [`rmw_dds.md`](rmw_dds.md) | Слой | CycloneDDS, ROS_DOMAIN_ID | `rmw.md`, `dds_protocol.md`, `discovery.md` |
| [`ros2_control.md`](ros2_control.md) | Слой | controller_manager, DiffDrive, arm_controller | `ros2_control.md` |
| [`robot_model.md`](robot_model.md) | Слой | URDF/Xacro, links, joints | `urdf_xacro.md` |
| [`tf_frames.md`](tf_frames.md) | Слой | TF-дерево, frame_id | `tf2.md` |
| [`launch_params.md`](launch_params.md) | Слой | Launch, YAML, параметры | `launch.md`, `parameters.md` |
| [`qos_profiles.md`](qos_profiles.md) | Слой | Reliability, durability, depth | `qos.md` |
| [`lifecycle_nodes.md`](lifecycle_nodes.md) | Слой | Managed nodes, состояния | `lifecycle.md` |
| [`simulation.md`](simulation.md) | Слой | Gazebo, миры, спавн | `simulation.md` |

---

## Расширяющий материал

### Два режима симуляции: public vs private

TIAGo поддерживает два режима, которые отличаются источником одометрии:

| Режим | Одометрия | Навигация | Флаг |
|---|---|---|---|
| **Public** | `DiffDriveController` (из колёсной одометрии) | Nav2 с AMCL | `is_public_sim:=True` |
| **Private** | `DLO` (LiDAR + IMU) или `gazebo_ros` | Nav2 без AMCL | флаг `is_public_sim:=False` |

В **public**-режиме одометрия считается по вращению колёс (проще, нагляднее для обучения). В **private** — по данным лидара и IMU (реалистичнее для PAL-продукта). Для обучения рекомендуется `is_public_sim:=True`.

### Архитектура twist_mux: 4 уровня приоритетов

`twist_mux` — ключевой узел безопасности. Он получает команды скорости из нескольких источников и выбирает одну по приоритету:

| Приоритет | Источник | Ситуация |
|---|---|---|
| 0 (низкий) | Nav2 controller_server | Автономная навигация |
| 1 | teleop_twist_keyboard | Ручное управление |
| 2 | joy_node (джойстик) | Оператор с пультом |
| 3 (высокий) | emergency_stop | Аварийная остановка |

Если E-stop активен — все остальные источники блокируются, робот не едет ни при каких обстоятельствах.

### Два RViz: почему не один?

При запуске `moveit:=True` появляются **два** окна RViz:
1. **Базовый RViz** — модель робота, TF, LaserScan (конфиг: `tiago_gazebo/config/tiago_sim.rviz`)
2. **MoveIt RViz** — панель MotionPlanning, планирование траекторий

Почему не объединить? Потому что конфиги RViz имеют разное назначение: базовый показывает сенсоры и одометрию, MoveIt — планирование движений. Их объединение создаёт конфликты в конфигурационных плагинах.

### GUI в контейнере: noVNC + Xvfb

Поскольку контейнер не имеет собственного дисплея, графический интерфейс работает через связку:
`Xvfb (виртуальный экран) → x11vnc (VNC-сервер) → websockify → noVNC (браузерный клиент)`

Это позволяет открывать RViz, Gazebo и rqt в браузере по адресу `http://localhost:6080`, без X-сервера на хосте.

---

## Связанные документы

- [`TIAgo_configuration.md`](../TIAgo_configuration.md) — полная конфигурация: пакеты, команды, аргументы
- [`AGENTS.md`](../AGENTS.md) — правила работы агентов в проекте
- [`TIAgo_conf_improv_plan.md`](../TIAgo_conf_improv_plan.md) — план доработки (YOLO, LLM, lifecycle)
- [`2_knowledge/ros_architecture.md`](../../2_knowledge/ros_architecture.md) — архитектура ROS2
- [`2_knowledge/subsystem.md`](../../2_knowledge/subsystem.md) — подсистемы робота
