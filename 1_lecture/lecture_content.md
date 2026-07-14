# lecture_content.md

## Назначение документа

Этот документ — содержательная спецификация лекции по ROS2 (уровень 1) и сопутствующих материалов уровней 2 и 3. Он создается до полного каркаса курса и служит внутренним договором: что именно войдет в лекцию, какие практики и код будут подготовлены, как каждая тема отражается в архитектуре робота из `3_Robot/`.

Документ не является публичной программой лекции и не заменяет `1_lecture/lecture_plan.md`. Его задача — дать ИИ-агентам (например, `deepseek/deepseek-v4-pro`) достаточную детализацию, чтобы они могли углублять любой блок-тему без повторного обсуждения структуры курса.

## Границы лекции на 80 минут (40+40 минут)

Лекция длится 80 минут с естественным разделением:

- первая часть (0-40 минут): введение, nodes и ROS Graph, middleware (DDS/RMW/discovery), workspace, node, topic, service, action, вопросы и переход;
- вторая часть (40-80 минут): launch, parameters, tf2, QoS, lifecycle, simulation-first, архитектурные мосты к Nav2, MoveIt2, YOLO и LLM bridge.

Важно объяснить устройство лекции, структуру материала в репозитории, как использовать три уровня материала по каждому блоку, показать самого Robot как идеальную демонстрацию - это надо сделать в README.md проекта и на одном-двух слайдах введения. 

В файлах `2_knowledge/*.md` блоков обязательно присутствуют команды, необходимые для выполнения задания, с кратким указанием назначения и объяснением синтаксиса (аналогично help в bash). Там же приводится ссылка на документацию с полным списком команд.

В 80 минут входит только уровень 1 — объяснение концепций, схемы, минимальные фрагменты кода на слайдах и короткие CLI-демонстрации. Полные практики, код и углубленные объяснения вынесены в уровень 2. Архитектурные привязки к роботу — в уровень 3.

ROS2 не устанавливается на хост. Все демонстрации и практики подразумевают контейнерную среду: общий контейнер курса для уровня 2 и контейнер `3_Robot/` для уровня 3.

## Общий план тем

1. Что такое ROS2 и зачем он нужен роботу
2. Архитектура робота как набор подсистем, ROS Graph и middleware: sensors, control, navigation, perception, manipulation, behavior, safety, DDS/RMW/discovery
3. Установка ROS2 Jazzy и проверка окружения
4. Workspace, package и сборка через `colcon`
5. Node, ROS Graph, Executor и callbacks
6. Topic, publisher, subscriber и message types
7. Service и client
8. Action server и action client
9. Parameters и launch
10. tf2 и дерево координат
11. QoS на практических примерах
12. Lifecycle как модель управляемого устройства
13. Simulation-first: URDF/Xacro, Gazebo/Ignition, `rviz2`, `ros2_control`
14. Архитектурный мост к Nav2
15. Архитектурный мост к MoveIt2
16. Архитектурный мост к YOLO
17. Архитектурный мост к LLM bridge
18. Мини-проект: связать несколько узлов в систему

План согласован с `COURSE_ARCHITECTURE.md`. Блоки 14-17 выделены в отдельные темы для детального объяснения каждого архитектурного моста.

## Карта уровней 1, 2 и 3

| Тема | Уровень 1 (лекция) | Уровень 2 (самостоятельно) | Уровень 3 (3_Robot/) |
| --- | --- | --- | --- |
| 1. Что такое ROS2 | 0-4 мин: место в воркшопе, middleware как суть ROS2 | `2_knowledge/ros_architecture.md` | Карта подсистем робота |
| 2. Архитектура, ROS Graph и middleware | 4-14 мин: подсистемы, nodes, ROS Graph, путь сообщения через DDS/RMW/discovery | `2_knowledge/ros_architecture.md` | Схема подсистем 3_Robot/ и RMW в контейнере 3_Robot/ |
| 3. Установка и окружение | 14-16 мин: контейнер, проверка `ros2` CLI | `2_knowledge/workspace.md`, `2_practice/01_workspace.md` | Контейнер 3_Robot/ |
| 4. Workspace, package, `colcon` | 16-18 мин: `ros2 pkg create`, `colcon build` | `2_knowledge/packages.md`, `2_knowledge/colcon.md`, `2_practice/02_package.md` | `ros2_ws/src/` |
| 5. Node, Executor и callbacks | 18-20 мин: написание node, `rqt_graph` | `2_knowledge/nodes.md` | `tiago_bringup/`, `tiago_controller_configuration/` |
| 6. Topic, publisher, subscriber | 20-28 мин: pub/sub, message types, CLI | `2_knowledge/topics.md`, `2_practice/03_topic.md`, `1_demo/demo2_topics.md` | `/cmd_vel`, `/odom`, `/scan` |
| 7. Service и client | 28-33 мин: запрос-ответ | `2_knowledge/services.md`, `2_practice/04_service.md`, `1_demo/demo3_services.md` | `/emergency_stop`, диагностика |
| 8. Action server и client | 33-38 мин: goal, feedback, cancel, result | `2_knowledge/actions.md`, `2_practice/05_action.md` | `/navigate_to_pose` |
| 9. Parameters и launch | 38-40 мин (вопросы) + 40-46 мин: YAML, Python launch | `2_knowledge/parameters.md`, `2_knowledge/launch.md` | `tiago_bringup/launch/` |
| 10. tf2 | 46-52 мин: дерево координат, `tf2_echo`, `view_frames` | `2_knowledge/tf2.md`, `2_practice/07_tf2.md`, `1_demo/demo4_tf2.md` | `map -> odom -> base_link -> lidar/camera` |
| 11. QoS | 52-54 мин: reliability, durability, history, deadline | `2_knowledge/qos.md` | QoS для `/scan`, `/camera/image_raw` |
| 12. Lifecycle | 54-56 мин: состояния, переходы | `2_knowledge/lifecycle.md` | Lifecycle для hardware nodes |
| 13. Simulation-first | 56-62 мин: URDF/Xacro, Gazebo, rviz2, ros2_control | будущие `2_knowledge/urdf_xacro.md`, `2_knowledge/simulation.md`, `2_knowledge/ros2_control.md` | `tiago_description/`, `tiago_gazebo/` |
| 14. Мост к Nav2 | 62-67 мин: карта, локализация, `/navigate_to_pose` | `2_knowledge/nav2_bridge.md`, `1_demo/demo5_nav2_architecture.md` | `pmb2_navigation/` |
| 15. Мост к MoveIt2 | 67-72 мин: модель, joint limits, planning scene | `2_knowledge/moveit2_bridge.md`, `1_demo/demo6_moveit2_architecture.md` | `tiago_moveit_config/` |
| 16. Мост к YOLO | 72-76 мин: камера, detection, `/detections` | `2_knowledge/yolo_bridge.md`, `1_demo/demo7_yolo_perception.md` | `tiago_yolo` (планируется) |
| 17. Мост к LLM bridge | 76-80 мин: команда -> high-level action -> policy -> safety | `2_knowledge/llm_bridge.md`, `1_demo/demo8_llm_bridge_safety.md` | `tiago_llm_bridge` (планируется) |
| 18. Мини-проект | вне 80 минут: ссылка для самостоятельной работы | `2_practice/`-интеграция | все подсистемы вместе |

## Блок 1. Что такое ROS2 и зачем он нужен роботу

### Роль блока в лекции

Первый контакт с ROS2. Студент должен понять: ROS2 — не библиотека и не операционная система, а среда для связи программ робота. Блок открывает лекцию и задает всю мотивацию.

### Уровень 1: лекция

- Учебная цель: студент может объяснить, зачем роботу нужен middleware, и назвать, какие задачи ROS2 решает.
- Тайминг: 0-4 минуты.
- Ключевые концепты: middleware, распределенная система, ROS Graph.
- Новые термины: ROS2, middleware, ROS Graph (определены в `TERMINOLOGY.md`).
- Порядок объяснения:
  1. Что такое ROS2: среда, в которой отдельные программы робота обмениваются сообщениями и командами.
  2. Зачем нужно: без middleware каждый раз писать свой протокол, сериализацию, обнаружение узлов и логирование.
  3. Аналогия: ROS2 — это городская инфраструктура (дороги, почта, адреса, светофоры), а программы робота — жители, которые пользуются инфраструктурой, а не строят ее заново.
  4. Как выглядит в ROS2: nodes общаются через topics, services и actions; система сама находит узлы (discovery).
  5. Место лекции в воркшопе: после ROS2 идут сенсорика, YOLO, SLAM, Nav2, манипуляторы. ROS2 — общий язык для всех этих тем.
- Схемы: Mermaid-диаграмма "Программы робота без middleware vs с ROS2".
- Фрагменты кода: не нужны. Показать только концептуальную схему.
- CLI-команды: не нужны.
- Источники: [ROS2 Concepts](https://docs.ros.org/en/jazzy/Concepts.html), [Why ROS2](https://design.ros2.org/).
- Что вынести в самостоятельную работу: история ROS1 vs ROS2, сравнение с другими middleware.

### Уровень 2: самостоятельная практика и код

- Файлы: `2_knowledge/ros_architecture.md`.
- Назначение: статья объясняет архитектуру ROS2, отличие от монолитного ПО, схему ROS Graph, место DDS и discovery. Содержит схему "как сообщение проходит от publisher к subscriber".
- Задача студента: прочитать статью, понять архитектурную модель.
- Команды: не требуются.
- Код: не требуется.
- Типичные ошибки: путаница ROS2 с операционной системой, ожидание что ROS2 — это библиотека вроде OpenCV.
- Показ на лекции: не нужен, только ссылка на статью.
- Материалы только ссылкой: историческая справка, сравнение ROS1/ROS2, список альтернативных middleware.

### Уровень 3: робот из 3_Robot/

- Подсистемы: все подсистемы робота используют ROS2 как общий язык.
- Фрагмент архитектуры: обзорная схема подсистем робота — Mobile Base, Navigation, Manipulation, Perception, Sensor Suite, Safety, LLM Bridge, Simulation.
- Каталоги и файлы: `3_Robot/TIAgo_humble/AGENTS.md` (архитектура), `3_Robot/TIAgo_humble/TIAgo_configuration.md` (конфигурация).
- Nodes: обзорно перечислить основные узлы каждой подсистемы.
- Topics/services/actions: обзорно — `/cmd_vel`, `/odom`, `/scan`, `/camera/image_raw`, `/detections`, `/navigate_to_pose`, `/emergency_stop`, `/battery_state`.
- Диаграмма: обзорная Mermaid-схема ROS Graph всего робота (план Б: статическая схема, если робот не запускается).

### Что не успеваем в лекции

История ROS1, сравнение с другими middleware (MQTT, ZeroMQ, DDS напрямую), внутренняя архитектура DDS.

### Источники и проверка фактов

- [ROS2 Design: Why ROS2](https://design.ros2.org/)
- [ROS2 Concepts](https://docs.ros.org/en/jazzy/Concepts.html)

### Открытые вопросы

Нет.

## Блок 2. Архитектура робота, ROS Graph и middleware

### Роль блока в лекции

Студент должен понять две вещи: (1) робот делится на независимые подсистемы с четкими интерфейсами — это архитектурная модель; (2) ROS2 реализует эту модель через nodes, ROS Graph и middleware — DDS, RMW, discovery. Блок связывает архитектурное мышление с технической реализацией.

### Уровень 1: лекция

- Учебная цель: студент может перечислить подсистемы робота, объяснить их интерфейсы и понимает, как middleware (DDS/RMW/discovery) доставляет сообщения между узлами.
- Тайминг: 4-14 минут.
  1. 4-8 мин: nodes, ROS Graph, Executor, callbacks — устройство ROS2 изнутри.
  2. 8-14 мин: middleware — DDS, RMW, discovery, путь сообщения от publisher к subscriber.
- Ключевые концепты: node, ROS Graph, middleware, DDS, RMW, discovery, подсистема.
- Новые термины: node (отдельная программа робота), ROS Graph (сеть узлов и связей), DDS (служба доставки сообщений), RMW (адаптер между ROS2 API и DDS), discovery (автоматическое знакомство узлов), подсистема. Определены в `TERMINOLOGY.md`.
- Порядок объяснения (часть 1 — nodes и Graph, 4-8 мин):
  1. Что такое node: программа, которая решает одну задачу. Примеры из 3_Robot/: camera_node, lidar_node, motor_controller.
  2. Аналогия: node — сотрудник в офисе. У каждого свой стол и задача. Executor — секретарь, раскладывающий входящие сообщения по папкам.
  3. Как выглядит в ROS2: `rclpy.init()`, `create_node()`, `spin()`, `rqt_graph`.
  4. Схема: Mermaid-диаграмма ROS Graph с 3-4 узлами (camera -> YOLO -> planner -> motor).
- Порядок объяснения (часть 2 — middleware, 8-14 мин):
  1. Что такое middleware: слой между ROS2 API (publisher/subscriber в коде) и реальной сетью. Это не код студента, а готовая служба доставки.
  2. Зачем нужен middleware: publisher и subscriber могут быть на разных машинах, в разных процессах, с разными QoS. Middleware берет на себя сериализацию, отправку по сети, обнаружение узлов и контроль доставки.
  3. Аналогия: middleware — это почтовая служба. Вы (publisher) опускаете письмо в ящик, не думая, как оно доедет. Почта (DDS) сортирует, везет и вручает адресату (subscriber). RMW — это выбор почтовой компании: Fast DDS или Cyclone DDS.
  4. Как это выглядит технически:
     - DDS (Data Distribution Service): протокол, который реально передает данные по сети. Реализует QoS, discovery, multicast/unicast.
     - RMW (ROS Middleware Wrapper): тонкий слой, который переводит ROS2-команды (`publish()`, `subscribe()`) в вызовы конкретного DDS.
     - Discovery: когда вы запускаете `ros2 run`, новый узел через DDS объявляет о себе, и другие узлы узнают о нем без ручной настройки.
     - Путь сообщения: `publisher.publish(msg)` → RMW → DDS (сериализация) → сеть (UDP multicast/unicast) → DDS (десериализация) → RMW → callback subscriber-а.
  5. Ключевой вывод: студент не пишет сетевой код. ROS2 + RMW + DDS делают это сами. Студент пишет только бизнес-логику в callbacks.
  6. Подсистемы робота как архитектурная модель (кратко, развернуто в уровне 3):
     - Mobile Base, Navigation, Manipulation, Perception, Safety, LLM Bridge, Simulation.
     - Каждая подсистема — это группа nodes, объединенных общими topics/services/actions.
- Схемы:
  - Mermaid-диаграмма "путь сообщения от publisher к subscriber" (publisher → RMW → DDS → сеть → DDS → RMW → subscriber).
  - Mermaid-диаграмма ROS Graph с 3-4 узлами.
  - Mermaid-диаграмма подсистем робота с интерфейсами (Mobile Base, Navigation, etc.).
- Фрагменты кода: не в этом блоке — первый код будет в блоках 4-5 после проверки окружения и создания workspace.
- CLI-команды: `rqt_graph` (для визуализации ROS Graph), `ros2 node list`.
- Источники: [ROS2 Concepts](https://docs.ros.org/en/jazzy/Concepts.html), [About DDS](https://docs.ros.org/en/jazzy/Concepts/Intermediate/About-Different-Middleware-Vendors.html), [ROS2 Discovery](https://docs.ros.org/en/jazzy/Concepts/Intermediate/About-Discovery.html).
- Что вынести в самостоятельную работу: сравнение DDS-вендоров (Fast DDS vs Cyclone DDS), multicast vs unicast, shared memory transport, внутреннее устройство RTPS.

### Уровень 2: самостоятельная практика и код

- Файлы: `2_knowledge/ros_architecture.md` (статья с разделами: nodes, ROS Graph, middleware, DDS, RMW, discovery, подсистемы).
- Назначение: полное объяснение middleware с диаграммами и примерами. Раздел "как сообщение проходит от publisher к subscriber" с поэтапной схемой.
- Код: минимальный пример проверки и смены RMW: `ros2 doctor --report`, `printenv RMW_IMPLEMENTATION`, `export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp` при установленном пакете Cyclone DDS.
- Ожидаемый результат: студент понимает, что RMW можно менять без изменения кода узлов.
- Типичные ошибки: ожидание, что ROS2 сам по себе передает данные (без DDS); путаница между ROS2 API и middleware.
- Показ на лекции: `rqt_graph` с запущенными узлами; смена RMW и перезапуск (если позволяет время).
- Материалы только ссылкой: RTPS wire protocol, DDS security, сравнение вендоров.

### Уровень 3: робот из 3_Robot/

- Подсистемы: все 8 подсистем из `3_Robot/TIAgo_humble/AGENTS.md`.
- Фрагмент архитектуры: таблица подсистем с их ROS2-компонентами (из `3_Robot/TIAgo_humble/AGENTS.md`, раздел 3).
- Nodes: перечислить основные узлы каждой подсистемы (из `3_Robot/TIAgo_humble/AGENTS.md`).
- Topics/services/actions: `/cmd_vel`, `/odom`, `/scan`, `/camera/image_raw`, `/detections`, `/navigate_to_pose`, `/emergency_stop`, `/battery_state`.
- RMW в контейнере `3_Robot/TIAgo_humble/`: используется CycloneDDS (рекомендован PAL). Зафиксирован в контейнере робота.
- Диаграмма: Mermaid-схема ROS Graph робота с ~10-15 узлами (план Б: статическая схема).

### Что не успеваем в лекции

Сравнение вендоров DDS, RTPS wire protocol, DDS security, multicast/unicast конфигурация.

### Источники и проверка фактов

- [About DDS and RMW](https://docs.ros.org/en/jazzy/Concepts/Intermediate/About-Different-Middleware-Vendors.html)
- [About Discovery](https://docs.ros.org/en/jazzy/Concepts/Intermediate/About-Discovery.html)
- `3_Robot/AGENTS.md`, раздел 3 (архитектура системы).

### Открытые вопросы

Выбор DDS-вендора для курса нужно зафиксировать в контейнере. По умолчанию не утверждать Cyclone DDS без проверки образа и `RMW_IMPLEMENTATION`.

## Блок 3. Установка ROS2 Jazzy и проверка окружения

### Роль блока в лекции

Студент должен понять: ROS2 не ставится на хост. Все работает в контейнере. Блок дает первую работающую команду и уверенность, что окружение готово.

### Уровень 1: лекция

- Учебная цель: студент понимает контейнерный подход и умеет проверить, что ROS2 работает.
- Тайминг: 14-16 минут.
- Ключевые концепты: контейнер, Dev Container, `ros2` CLI, `RMW_IMPLEMENTATION`.
- Новые термины: контейнер (изолированная среда с ROS2), Dev Container, ROS2 CLI. Workspace будет раскрыт в блоке 4.
- Порядок объяснения:
  1. Почему не на хост: изоляция, воспроизводимость, одинаковое окружение у всех студентов.
  2. Что внутри контейнера: ROS2 Jazzy, Ubuntu 24.04, `colcon`, зависимости.
  3. Проверка ROS2 CLI: `ros2 --help`.
  4. Проверка demo node: `ros2 run demo_nodes_cpp talker`.
  5. Проверка middleware: `ros2 doctor --report` и `printenv RMW_IMPLEMENTATION` как диагностические команды, не как обязательная настройка.
- Фрагменты кода: не нужны на этом этапе.
- CLI-команды: `ros2 --help`, `ros2 run demo_nodes_cpp talker`, `ros2 doctor --report`, `printenv RMW_IMPLEMENTATION`.
- Источники: [ROS2 Jazzy Installation](https://docs.ros.org/en/jazzy/Installation.html), [ROS2 CLI tools](https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools.html).
- Что вынести в самостоятельную работу: Dockerfile, Dev Container настройка, альтернативные способы установки.

### Уровень 2: самостоятельная практика и код

- Файлы: `2_knowledge/workspace.md` (раздел про контейнер), `2_practice/01_workspace.md`, `1_demo/demo1_environment.md`.
- Назначение: пошаговая инструкция по запуску контейнера с ROS2 Jazzy и проверке окружения.
- Команды: `ros2 --help`, `ros2 run demo_nodes_cpp talker`, `ros2 doctor --report`.
- Ожидаемый результат: в терминале есть справка `ros2`, demo talker печатает сообщения, `ros2 doctor --report` показывает окружение.
- Типичные ошибки: контейнер не запущен, команда `ros2` не найдена, пакет `demo_nodes_cpp` не установлен в образе.
- Показ на лекции: преподаватель показывает `ros2 --help` и запуск `demo_nodes_cpp talker` внутри контейнера.

### Уровень 3: робот из 3_Robot/

- Подсистемы: все (контейнер `3_Robot/TIAgo_humble/`).
- Фрагмент: показать, что контейнер `3_Robot/TIAgo_humble/` содержит ROS2 Humble, Gazebo Classic 11, Nav2, MoveIt2, `ros2_control` и workspace робота.
- Каталоги и файлы: `3_Robot/TIAgo_humble/.devcontainer/` или `3_Robot/TIAgo_humble/docker/`, `ros2_ws/`.

### Что не успеваем в лекции

Dockerfile, Dev Container настройка, альтернативные способы установки (robostack, conda).

### Источники и проверка фактов

- [ROS2 Jazzy Installation](https://docs.ros.org/en/jazzy/Installation.html)

### Открытые вопросы

Конкретная конфигурация контейнера (`.devcontainer/`) еще не создана; уточнить на этапе каркаса.

## Блок 4. Workspace, package и сборка через `colcon`

### Роль блока в лекции

Студент должен создать workspace, пакет и собрать его. Это фундамент: без workspace и `colcon` невозможно написать ни одного собственного узла.

### Уровень 1: лекция

- Учебная цель: студент может создать workspace, создать пакет через `ros2 pkg create`, собрать через `colcon build` и подготовить пакет к запуску.
- Тайминг: 16-18 минут.
- Ключевые концепты: workspace, package, `colcon`, `setup.bash`, `ament_python`, `package.xml`.
- Новые термины: workspace (папка с пакетами и результатами сборки), package (минимальная единица кода в ROS2), `colcon` (инструмент сборки), `ament` (система сборки ROS2). Определены в `TERMINOLOGY.md`.
- Порядок объяснения:
  1. Что такое workspace: `src/` для исходников, `build/`, `install/`, `log/` — результаты сборки.
  2. Аналогия: workspace — мастерская; `src/` — чертежи; `colcon build` — сборка; `install/` — готовые артефакты.
  3. Как создать пакет: `ros2 pkg create --build-type ament_python my_pkg`.
  4. Как собрать: `colcon build`, `source install/setup.bash`.
  5. Почему `source install/setup.bash` нужен перед `ros2 run`.
- Фрагменты кода: не показывать полный код, только структуру пакета и место будущего `my_node.py`.
- CLI-команды: `mkdir -p ros2_ws/src`, `ros2 pkg create`, `colcon build`, `source install/setup.bash`, `ros2 pkg list`.
- Источники: [Creating a workspace](https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Creating-A-Workspace/Creating-A-Workspace.html), [Creating a package](https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Creating-Your-First-ROS2-Package.html).
- Что вынести в самостоятельную работу: `ament_cmake` vs `ament_python`, `CMakeLists.txt`, overlay/underlay, флаги `colcon`.

### Уровень 2: самостоятельная практика и код

- Файлы: `2_knowledge/workspace.md`, `2_knowledge/packages.md`, `2_knowledge/colcon.md`, `2_practice/02_package.md`, `1_demo/demo1_environment.md`.
- Назначение: пошаговые инструкции по созданию workspace и пакета.
- Код: минимальный Python-узел будет добавлен в блоке 5; здесь достаточно структуры пакета.
- Ожидаемый результат: `colcon build` завершается без ошибок, пакет появляется после `source install/setup.bash`.
- Типичные ошибки: забыли `source setup.bash`, имя пакета не совпадает с именем папки, пакет создан не в `src/`.
- Показ на лекции: быстрый цикл `pkg create -> colcon build -> source`.

### Уровень 3: робот из 3_Robot/

- Подсистемы: все (ros2_ws).
- Фрагмент: структура `ros2_ws/src/` с пакетами `tiago_bringup`, `tiago_description`, `tiago_gazebo`, `tiago_moveit_config`, `pmb2_robot`, `pmb2_navigation`, `play_motion2`, `pal_msgs` и др.
- Каталоги: `ros2_ws/src/`, `ros2_ws/install/`.
- Диаграмма: дерево каталогов `ros2_ws/`.

### Что не успеваем в лекции

`ament_cmake` для C++, `CMakeLists.txt` подробно, `colcon` флаги, `--merge-install`, overlay/underlay, чистка сборки.

### Источники и проверка фактов

- [ROS2 Beginner Tutorials](https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries.html)

### Открытые вопросы

Будет ли использоваться `ament_python` или `ament_cmake` как основной в курсе? Предпочтительно `ament_python` для первых примеров и `ament_cmake` ссылкой для C++.

## Блок 5. Node, ROS Graph, Executor и callbacks

### Роль блока в лекции

Node — основная единица вычислений в ROS2. После проверки окружения и сборки пакета студент должен увидеть первый собственный узел, понять `spin()` и связь с Executor/callbacks.

### Уровень 1: лекция

- Учебная цель: студент понимает, что такое node, как Executor вызывает callbacks и почему без `spin()` узел не обрабатывает события.
- Тайминг: 18-20 минут.
- Ключевые концепты: node, ROS Graph, Executor, callback, timer callback, `spin()`.
- Новые термины: node, ROS Graph, Executor, callback, spin (определены в `TERMINOLOGY.md`; здесь — практическое закрепление).
- Порядок объяснения:
  1. Что такое node: программа, которая решает одну задачу. Например, node камеры, node навигации, node моторов.
  2. Как выглядит в коде: `rclpy.init()`, класс `Node`, `create_timer()`, `get_logger()`, `rclpy.spin()`.
  3. Что делает Executor: ждет события и вызывает callbacks.
  4. Что показать: минимальный node с timer callback, затем `ros2 node list` и `rqt_graph`.
  5. Типичная ошибка: узел создан, но `spin()` не вызван, поэтому callbacks не выполняются.
- Фрагменты кода: минимальный node на Python (5-10 строк).
- CLI-команды: `ros2 run my_pkg my_node`, `ros2 node list`, `ros2 node info`, `rqt_graph`.
- Источники: [Understanding nodes](https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Nodes/Understanding-ROS2-Nodes.html), [ROS2 Executors](https://docs.ros.org/en/jazzy/Concepts/Intermediate/About-Executors.html).
- Что вынести в самостоятельную работу: multithreaded executor, callback groups, `spin_once`, composition.

### Уровень 2: самостоятельная практика и код

- Файлы: `2_knowledge/nodes.md`, раздел в `2_practice/02_package.md`.
- Назначение: статья с объяснением node, Executor, callbacks и `spin()`.
- Код: минимальный timer node и расширение до subscriber callback.
- Ожидаемый результат: студент запускает узел и видит его в `ros2 node list` и `rqt_graph`.
- Типичные ошибки: забыли `spin()`, блокирующий код в callback, неправильное имя executable в `setup.py`.
- Показ на лекции: `rqt_graph` с одним-двумя узлами.

### Уровень 3: робот из 3_Robot/

- Подсистемы: все.
- Nodes: `/camera_node`, `/lidar_node`, `/motor_controller`, `/nav2_planner`, `/safety_node`, `/llm_bridge`.
- Фрагмент: показать, что каждый пакет TIAGo (`tiago_bringup`, `pmb2_robot`, `tiago_gazebo`...) содержит один или несколько узлов с узкой ответственностью.
- Диаграмма: ROS Graph робота с 10-15 узлами (план Б: статическая Mermaid-схема).

### Что не успеваем в лекции

Multithreaded executor, callback groups, intra-process communication, composition, `rclcpp` API.

### Источники и проверка фактов

- [ROS2 Nodes](https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Nodes/Understanding-ROS2-Nodes.html)
- [ROS2 Executor](https://docs.ros.org/en/jazzy/Concepts/Intermediate/About-Executors.html)

### Открытые вопросы

Нет.

## Блок 6. Topic, publisher, subscriber и message types

### Роль блока в лекции

Topic — основной механизм связи в ROS2. Это самый важный блок первой части лекции: publisher, subscriber, message types, CLI-проверка. На этом блоке студент впервые видит реальный обмен данными между узлами.

### Уровень 1: лекция

- Учебная цель: студент может написать publisher и subscriber, выбрать стандартный message type и проверить обмен через `ros2 topic`.
- Тайминг: 20-28 минут.
- Ключевые концепты: topic, publisher, subscriber, message type, интерфейс.
- Новые термины: topic (именованный поток сообщений — "Telegram-канал"), publisher (отправитель в канал), subscriber (подписчик канала), message (письмо с полями). Определены в `TERMINOLOGY.md`.
- Порядок объяснения:
  1. Что такое topic: именованный канал, куда publishers отправляют сообщения типа `std_msgs/String`, а subscribers их читают.
  2. Зачем нужно: передача потоковых данных — `/scan`, `/camera/image_raw`, `/cmd_vel`.
  3. Аналогия: Telegram-канал "Новости робота". Один пишет, многие читают. Кто подписался — получает.
  4. Как выглядит в ROS2: `create_publisher()`, `create_subscription()`, callback.
  5. Как выглядит в коде: publisher печатает число, subscriber выводит его в лог.
  6. Типичные ошибки: забыли `spin()`, разные message types, неправильное имя topic.
- Фрагменты кода: publisher и subscriber на Python (по 8-10 строк каждый).
- CLI-команды: `ros2 topic list`, `ros2 topic echo`, `ros2 topic pub`, `ros2 topic hz`, `ros2 topic info`.
- Источники: [Writing a simple publisher and subscriber (Python)](https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Py-Publisher-And-Subscriber.html).

### Уровень 2: самостоятельная практика и код

- Файлы: `2_knowledge/topics.md`, `2_practice/03_topic.md`, `1_demo/demo2_topics.md`, `2_code/` с примерами publisher/subscriber.
- Назначение:
  - `topics.md`: полное описание topics, message types, `ros2 topic` CLI, `rqt_plot`.
  - `2_practice/03_topic.md`: студент создает пакет с publisher и subscriber.
  - `1_demo/demo2_topics.md`: демонстрация обмена данными с `ros2 topic echo`.
- Код: pub/sub для `std_msgs/String`, расширение до `geometry_msgs/Twist`.
- Ожидаемый результат: в терминале `ros2 topic echo /chatter` показывает сообщения.
- Типичные ошибки: разные message types у pub и sub, неправильное QoS, topic не виден из-за namespace.
- Показ на лекции: два терминала — один с `ros2 topic echo`, другой с `ros2 topic pub`.

### Уровень 3: робот из 3_Robot/

- Подсистемы: Mobile Base, Navigation, Perception, Sensor Suite.
- Topics: `/cmd_vel` (geometry_msgs/Twist), `/odom` (nav_msgs/Odometry), `/scan` (sensor_msgs/LaserScan), `/camera/image_raw` (sensor_msgs/Image), `/joint_states` (sensor_msgs/JointState), `/battery_state` (sensor_msgs/BatteryState).
- Nodes: `motor_controller` публикует `/odom`, подписан на `/cmd_vel`; `lidar_node` публикует `/scan`; `camera_node` публикует `/camera/image_raw`.
- Диаграмма: фрагмент ROS Graph с topics между базой и навигацией.

### Что не успеваем в лекции

Custom messages (`.msg`), `rqt_plot`, `ros2 bag`, запись/воспроизведение данных, `topic statistics`.

### Источники и проверка фактов

- [ROS2 Topics Tutorial](https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Topics/Understanding-ROS2-Topics.html)

### Открытые вопросы

Стоит ли показывать custom message в лекции или только ссылкой? (Предположительно: ссылкой.)

## Блок 7. Service и client

### Роль блока в лекции

Service нужен, когда topic недостаточно — требуется запрос-ответ. Блок дает третий способ связи после topic, завершая картину коммуникаций.

### Уровень 1: лекция

- Учебная цель: студент понимает, когда нужен service, а не topic, и может написать service server и client.
- Тайминг: 28-33 минут.
- Ключевые концепты: service, synchronous/asynchronous call, request/response.
- Новые термины: service (запрос-ответ, как звонок в справочную), client (тот, кто вызывает service), server (тот, кто отвечает). Определены в `TERMINOLOGY.md`.
- Порядок объяснения:
  1. Что такое service: один узел отправляет запрос, другой отвечает. В отличие от topic — связь точка-точка, с ожиданием ответа.
  2. Зачем нужно: запросить статус батареи, включить/выключить датчик, получить текущую конфигурацию, активировать emergency stop.
  3. Аналогия: звонок в справочную службу: вы задаете вопрос и ждете ответа.
  4. Как выглядит в ROS2: `create_service()`, `create_client()`, `send_request()`.
  5. Как выглядит в коде: server принимает два числа и возвращает сумму; client отправляет запрос.
- Фрагменты кода: service server и client на Python (по 10-12 строк).
- CLI-команды: `ros2 service list`, `ros2 service type`, `ros2 service call`.
- Источники: [Writing a simple service and client (Python)](https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Py-Service-And-Client.html).

### Уровень 2: самостоятельная практика и код

- Файлы: `2_knowledge/services.md`, `2_practice/04_service.md`, `1_demo/demo3_services.md`.
- Назначение:
  - `services.md`: полное описание, сравнение с topic, async client.
  - `2_practice/04_service.md`: создать пакет с service server и client.
  - `1_demo/demo3_services.md`: живой вызов service из CLI.
- Код: server "add two ints", client вызывает его из CLI и из кода.
- Ожидаемый результат: `ros2 service call /add_two_ints` возвращает сумму.
- Типичные ошибки: забыли `spin()`, client вызывает service до того, как server готов, неправильный message type.
- Показ на лекции: `ros2 service call` в реальном времени.

### Уровень 3: робот из 3_Robot/

- Подсистемы: Safety, Mobile Base, Sensor Suite.
- Services: `/emergency_stop` (trigger E-stop), `/reset_motors`, `/enable_lidar`, `/set_led`.
- Nodes: `safety_node` — server для `/emergency_stop`; `motor_controller` — server для `/reset_motors`.
- Диаграмма: фрагмент ROS Graph с service-связями.

### Что не успеваем в лекции

Custom service (`.srv`), async client, service timeout, service introspection.

### Источники и проверка фактов

- [ROS2 Services Tutorial](https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Services/Understanding-ROS2-Services.html)

### Открытые вопросы

Нет.

## Блок 8. Action server и action client

### Роль блока в лекции

Action — механизм для длительных задач с прогрессом и возможностью отмены. Это ключевой блок для понимания навигации (`/navigate_to_pose`) и манипуляции.

### Уровень 1: лекция

- Учебная цель: студент понимает отличие action от topic и service, знает структуру goal/feedback/result/cancel.
- Тайминг: 33-38 минут.
- Ключевые концепты: action, goal, feedback, result, cancel, preemption.
- Новые термины: action (длительная задача с прогрессом и отменой), goal (цель), feedback (промежуточный прогресс), result (итог), cancel (отмена). Определены в `TERMINOLOGY.md`.
- Порядок объяснения:
  1. Что такое action: задача, которая выполняется долго, сообщает о ходе и может быть отменена.
  2. Зачем нужно: навигация к точке (едет несколько секунд, сообщает расстояние), манипуляция (поднять предмет — долго, сообщает прогресс).
  3. Аналогия: доставка пиццы: вы делаете заказ (goal), курьер сообщает "выехал, подъезжаю" (feedback), пицца доставлена (result), можно отменить заказ (cancel).
  4. Как выглядит в ROS2: `create_action_server()`, `create_action_client()`, `send_goal()`.
  5. Как выглядит в коде: action server считает от 1 до N с паузой, отправляет feedback; client ждет result.
- Фрагменты кода: action server и client на Python (по 15-20 строк).
- CLI-команды: `ros2 action list`, `ros2 action send_goal`, `ros2 action info`.
- Источники: [Writing an action server and client (Python)](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Writing-an-Action-Server-Client/Py.html), [Understanding ROS2 Actions](https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Actions/Understanding-ROS2-Actions.html).

### Уровень 2: самостоятельная практика и код

- Файлы: `2_knowledge/actions.md`, `2_practice/05_action.md`.
- Назначение:
  - `actions.md`: полное описание, сравнение с topic и service, cancel/preeemption.
  - `2_practice/05_action.md`: создать пакет с action server и client.
- Код: action "Fibonacci" с progress feedback, client с возможностью cancel.
- Ожидаемый результат: `ros2 action send_goal` показывает feedback и result; отмена работает.
- Типичные ошибки: забыли `spin()`, goal принят но не выполняется, cancel не обработан в callback.
- Показ на лекции: `ros2 action send_goal` с флагом `--feedback`, демонстрация cancel.

### Уровень 3: робот из 3_Robot/

- Подсистемы: Navigation, Manipulation.
- Actions: `/navigate_to_pose` (Nav2 action — доехать до точки с прогрессом), `/follow_path`, MoveIt2 action для планирования траектории.
- Nodes: Nav2 BT navigator — action server, MoveIt2 move_group — action server.
- Frames: `map`, `odom`, `base_link`, `base_footprint`.

### Что не успеваем в лекции

Custom action (`.action`), preemption подробно, action introspection, `rqt` для actions.

### Источники и проверка фактов

- [ROS2 Actions Tutorial](https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Actions/Understanding-ROS2-Actions.html)
- [Nav2 navigate_to_pose](https://docs.nav2.org/)

### Открытые вопросы

Нет.

## Блок 9. Parameters и launch

### Роль блока в лекции

Parameters позволяют менять поведение узла без перекомпиляции. Launch позволяет запустить систему из нескольких узлов одной командой. Эти механизмы превращают набор отдельных узлов в рабочую систему.

### Уровень 1: лекция

- Учебная цель: студент умеет задавать параметры через YAML и запускать несколько узлов через launch-файл.
- Тайминг: 38-40 минут (вопросы и переход) + 40-46 минут (основная часть).
- Ключевые концепты: parameter, parameter declaration, YAML config, launch file, Python launch.
- Новые термины: parameter (настройка узла, которая меняется без перекомпиляции), launch (сценарий запуска нескольких узлов). Определены в `TERMINOLOGY.md`.
- Порядок объяснения:
  1. Что такое parameter: именованное значение в узле — скорость, порог, частота. Меняется в YAML или через CLI.
  2. Что такое launch: файл, который запускает несколько узлов, задает им параметры и аргументы.
  3. Аналогия parameters: настройки телефона — яркость, громкость, язык (меняются без перепрошивки).
  4. Аналогия launch: сценарий запуска театральной постановки — свет, звук, актеры выходят по сценарию, а не вручную.
  5. Как выглядит в ROS2: `declare_parameter()`, `get_parameter()`, YAML config, Python launch file.
  6. Как выглядит в коде: узел с параметром `speed`, YAML-файл `config.yaml`, `launch.py`.
- Фрагменты кода: узел с параметром (8 строк), YAML-файл (3 строки), launch-файл (10 строк).
- CLI-команды: `ros2 param list`, `ros2 param get`, `ros2 param set`, `ros2 launch`.
- Источники: [Using parameters](https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Parameters/Understanding-ROS2-Parameters.html), [Creating a launch file](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Launch/Creating-Launch-Files.html).

### Уровень 2: самостоятельная практика и код

- Файлы: `2_knowledge/parameters.md`, `2_knowledge/launch.md`, практика с launch-файлом.
- Назначение:
  - `parameters.md`: declare vs undeclared, dynamic parameters, YAML, CLI.
  - `launch.md`: Python launch, XML launch, substitutions, arguments.
- Код: узел с параметром `publish_rate` + YAML config + launch-файл, запускающий pub и sub с параметрами.
- Ожидаемый результат: `ros2 launch my_pkg my_launch.py` запускает два узла; `ros2 param set` меняет поведение на лету.
- Типичные ошибки: параметр не объявлен (не виден в `ros2 param list`), путь к YAML неверный, launch-файл не установлен в `setup.py`.
- Показ на лекции: запуск launch-файла, изменение параметра через CLI, демонстрация изменения поведения.

### Уровень 3: робот из 3_Robot/

- Подсистемы: все (bringup).
- Каталоги и файлы: `tiago_bringup/launch/` (56 launch-файлов), конфиги в `*/config/` (170 YAML).
- Launch-файлы: `tiago_gazebo.launch.py` (главный, с 22 аргументами), `bringup.launch.py`, `navigation_public_sim.launch.py`.
- Parameters: `nav2_params.yaml` (`nav_public_sim.yaml`), `arm_controller.yaml`, `camera_params.yaml`.
- Nodes: все узлы подсистем.

### Что не успеваем в лекции

XML launch (используется в Nav2, но можно ссылкой), lifecycle nodes в launch, conditional launch, `ComposableNodeContainer`.

### Источники и проверка фактов

- [ROS2 Launch](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Launch/Launch-Main.html)

### Открытые вопросы

Будет ли использоваться Python launch или XML launch? (Предположительно Python, но упомянуть XML для совместимости с Nav2.)

## Блок 10. tf2 и дерево координат

### Роль блока в лекции

tf2 связывает координатные системы робота: `map -> odom -> base_link -> lidar/camera/arm`. Без tf2 робот не понимает, где находится датчик относительно базы, и навигация/манипуляция невозможны.

### Уровень 1: лекция

- Учебная цель: студент понимает, зачем нужны transform-ы, как читать дерево `tf2` и как проверить связи через CLI.
- Тайминг: 46-52 минуты.
- Ключевые концепты: transform, frame, tf tree, static/dynamic transform, `map -> odom -> base_link`.
- Новые термины: tf2 (подсистема хранения и вычисления преобразований координат), frame (именованная система координат), transform (переход между frame). Определены в `TERMINOLOGY.md`.
- Порядок объяснения:
  1. Что такое tf2: карта систем координат робота и переходов между ними.
  2. Зачем нужно: LiDAR видит препятствие в своем frame (`lidar_link`), а моторы едут в `base_link`. tf2 пересчитывает координаты между ними.
  3. Аналогия: tf2 — это GPS-координаты + поэтажный план здания. Вы знаете, где находитесь относительно комнаты, здания и улицы.
  4. Как выглядит в ROS2: дерево `map -> odom -> base_link -> lidar_link / camera_link / left_arm_*`.
  5. Как выглядит в коде: `tf2_ros.TransformBroadcaster` для публикации transform-а.
- Фрагменты кода: минимальный static transform broadcaster (5 строк), слушатель transform-а.
- CLI-команды: `ros2 run tf2_ros tf2_echo`, `ros2 run tf2_tools view_frames`, `ros2 topic echo /tf`.
- Источники: [tf2 Introduction](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Tf2/Tf2-Main.html).

### Уровень 2: самостоятельная практика и код

- Файлы: `2_knowledge/tf2.md`, `2_practice/07_tf2.md`, `1_demo/demo4_tf2.md`.
- Назначение:
  - `tf2.md`: полное описание, static vs dynamic transforms, `tf2_ros`, `tf2_echo`, `view_frames`.
  - `2_practice/07_tf2.md`: создать два узла — один публикует transform, другой слушает и вычисляет.
  - `1_demo/demo4_tf2.md`: показать `view_frames` и `tf2_echo` в `rviz2`.
- Код: статический transform между `world` и `robot_base`, слушатель печатает координаты.
- Ожидаемый результат: `view_frames` показывает дерево из 2-3 frame; `tf2_echo` показывает transform.
- Типичные ошибки: разное время (timestamp) у transform-ов, неправильное имя frame, transform не опубликован.
- Показ на лекции: `view_frames` генерирует PDF с деревом, `tf2_echo` показывает координаты в реальном времени.

### Уровень 3: робот из 3_Robot/

- Подсистемы: Mobile Base, Navigation, Manipulation, Perception (все используют tf2).
- Frames: `map`, `odom`, `base_link`, `base_footprint`, `chassis_link`, `left_wheel_link`, `right_wheel_link`, `lidar_link`, `camera_link`, `arm_1_link`...`arm_7_link`, `wrist_ft_link`, `gripper_link`.
- Nodes: `robot_state_publisher` (публикует transforms из URDF), `slam_toolbox` (публикует `map -> odom`), `amcl` (публикует `map -> odom` при локализации).
- Диаграмма: tf2-дерево робота (`map -> odom -> base_link -> lidar/camera/arms/wheels`).

### Что не успеваем в лекции

Time travel, tf2 buffer, advanced `tf2_ros::Buffer`, интеграция с `robot_localization`.

### Источники и проверка фактов

- [tf2 Tutorials](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Tf2/Tf2-Main.html)

### Открытые вопросы

Нет.

## Блок 11. QoS на практических примерах

### Роль блока в лекции

QoS определяет, как доставляются сообщения: надежно или нет, с хранением истории или без. Неправильный QoS может привести к тому, что данные не доходят, и робот не видит препятствия. Блок короткий, но критичный.

### Уровень 1: лекция

- Учебная цель: студент понимает три главных настройки QoS (reliability, durability, history) и может объяснить, когда какие значения нужны.
- Тайминг: 52-54 минуты (в блоке 52-56 мин вместе с lifecycle).
- Ключевые концепты: reliability (reliable/best effort), durability (volatile/transient local), history (keep last/depth), deadline, liveliness.
- Новые термины: QoS (правила доставки сообщений). Определен в `TERMINOLOGY.md`.
- Порядок объяснения:
  1. Что такое QoS: настройки, которые говорят DDS, как доставлять сообщения.
  2. Зачем нужно: `/scan` должен быть best effort (пропуск кадра не страшен), а команда `/cmd_vel` или goal — reliable (нельзя терять).
  3. Аналогия: QoS — это выбор службы доставки: "срочно, но могут потерять" (best effort) или "надежно, с подтверждением" (reliable).
  4. Как выглядит в коде: `qos_profile = QoSProfile(reliability=ReliabilityPolicy.BEST_EFFORT, depth=10)`.
- Фрагменты кода: publisher с разными QoS (3-4 строки).
- CLI-команды: тип команды для демо — `ros2 topic echo <topic_name> --qos-reliability best_effort`; точный topic уточнить в `1_demo/` после создания контейнера.
- Источники: [About QoS](https://docs.ros.org/en/jazzy/Concepts/Intermediate/About-Quality-of-Service-Settings.html).

### Уровень 2: самостоятельная практика и код

- Файлы: `2_knowledge/qos.md`.
- Назначение: полное объяснение всех QoS-политик, таблица "когда что использовать", примеры для `/scan`, `/cmd_vel`, `/camera/image_raw`.
- Код: pub/sub с mismatched QoS (не соединяются), демонстрация.
- Типичные ошибки: pub и sub не соединяются из-за разных QoS, best effort для важных команд, забыли depth.

### Уровень 3: робот из 3_Robot/

- Подсистемы: все, особенно Sensor Suite, Mobile Base, Perception.
- QoS для конкретных topics:
  - `/scan` — best effort, keep last, depth 10 (быстро, можно терять кадры);
  - `/cmd_vel` — reliable, keep last, depth 10 (нельзя терять команду);
  - `/camera/image_raw` — best effort, keep last, depth 5 (поток кадров);
  - `/odom` — reliable, keep last, depth 10;
  - `/detections` — reliable, keep last, depth 10 (нельзя терять факт обнаружения).

### Что не успеваем в лекции

Deadline, liveliness, lifespan, partition. Все это — ссылкой в `2_knowledge/qos.md`.

### Источники и проверка фактов

- [ROS2 QoS](https://docs.ros.org/en/jazzy/Concepts/Intermediate/About-Quality-of-Service-Settings.html)
- [DDS QoS](https://www.omg.org/spec/DDS/1.4/PDF)

### Открытые вопросы

Нет.

## Блок 12. Lifecycle как модель управляемого устройства

### Роль блока в лекции

Lifecycle node имеет состояния (unconfigured, inactive, active, finalized) и переходы между ними. Это критично для драйверов датчиков и приводов: нельзя начать читать данные, пока устройство не настроено.

### Уровень 1: лекция

- Учебная цель: студент понимает, зачем нужны состояния узла и как lifecycle помогает безопасному запуску и остановке.
- Тайминг: 54-56 минут.
- Ключевые концепты: lifecycle states, transitions, managed node.
- Новые термины: lifecycle (жизненный цикл устройства — состояния и переходы). Определен в `TERMINOLOGY.md`.
- Порядок объяснения:
  1. Что такое lifecycle: модель состояний узла — unconfigured, inactive, active, finalized.
  2. Зачем нужно: драйвер мотора должен сначала настроить порт, затем активировать контроль, и только потом принимать `/cmd_vel`. Нельзя ехать с ненастроенным контроллером.
  3. Аналогия: запуск автомобиля: ключ -> стартер -> прогрев -> поехали. Нельзя сразу тронуться.
  4. Как выглядит в ROS2: `LifecycleNode`, `on_configure()`, `on_activate()`, `on_deactivate()`, `on_cleanup()`, `on_shutdown()`.
  5. Как выглядит в коде: lifecycle node с переходом unconfigured -> inactive -> active.
- Фрагменты кода: минимальный lifecycle node (15 строк).
- CLI-команды: `ros2 lifecycle list`, `ros2 lifecycle set`.
- Источники: [Managed nodes](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Managing-Nodes/Managed-Nodes.html).

### Уровень 2: самостоятельная практика и код

- Файлы: `2_knowledge/lifecycle.md`.
- Назначение: полное объяснение состояний, переходов, lifecycle manager, интеграция с launch.
- Код: lifecycle узел с переходами, lifecycle manager в launch.
- Типичные ошибки: забыли вызвать `configure()` перед `activate()`, узел в finalized и не принимает переходы.

### Уровень 3: робот из 3_Robot/

- Подсистемы: Sensor Suite, Mobile Base, Manipulation (драйверы датчиков и приводов).
- Nodes: `lidar_node`, `motor_controller`, `camera_node` — все как lifecycle nodes.
- Parameters: параметры для каждого состояния.
- Диаграмма: диаграмма состояний lifecycle node.

### Что не успеваем в лекции

Lifecycle manager, автоматические переходы, bond (heartbeat).

### Источники и проверка фактов

- [ROS2 Lifecycle](https://docs.ros.org/en/jazzy/Concepts/Intermediate/About-Managed-Nodes.html)

### Открытые вопросы

Нет.

## Блок 13. Simulation-first: URDF/Xacro, Gazebo/Ignition, `rviz2`, `ros2_control`

### Роль блока в лекции

Simulation-first — принцип разработки: сначала цифровой двойник, потом реальный робот. Студент должен понять, как URDF/Xacro описывает робота, как Gazebo/Ignition симулирует физику, как `ros2_control` связывает ROS2-команды с приводами.

### Уровень 1: лекция

- Учебная цель: студент понимает цепочку: URDF/Xacro -> Gazebo/Ignition -> `ros2_control` -> `rviz2`, и может объяснить, зачем нужен simulation-first подход.
- Тайминг: 56-62 минуты.
- Ключевые концепты: URDF/Xacro, simulation, digital twin, `ros2_control`, `rviz2`.
- Новые термины: URDF/Xacro (формат описания геометрии, суставов и масс робота), Gazebo/Ignition (симулятор с физикой), `ros2_control` (слой между ROS2 и приводами), `rviz2` (визуализатор данных). Определены в `TERMINOLOGY.md`.
- Порядок объяснения:
  1. Что такое simulation-first: проверка логики, сенсоров и управления в симуляции до реального робота.
  2. Зачем нужно: физический робот дорогой, а ошибка в коде управления может его сломать.
  3. Аналогия: авиасимулятор — пилоты тренируются в симуляторе перед реальным полетом.
  4. Как выглядит в ROS2:
     - URDF/Xacro: текстовый файл с links, joints, geometry, inertia, collision.
     - Gazebo/Ignition: запускает URDF, считает физику, публикует сенсоры.
     - `ros2_control`: получает команды из ROS2 (например, `/cmd_vel` -> `diff_drive_controller`) и передает их в симуляцию или реальные приводы.
     - `rviz2`: показывает модель, сенсоры, карту, tf2-дерево.
  5. Как выглядит в коде: показать фрагмент URDF на слайде (link + joint, 10 строк).
- Фрагменты кода: фрагмент URDF/Xacro (базовая платформа с двумя колесами), YAML для `ros2_control`.
- CLI-команды: `ros2 launch robot_description display.launch.py`, `rviz2`.
- Источники: [URDF](http://wiki.ros.org/urdf), [Gazebo](https://gazebosim.org/docs), [ros2_control](https://control.ros.org/).

### Уровень 2: самостоятельная практика и код

- Файлы: `2_knowledge/` статьи по URDF, Gazebo, `ros2_control`, `rviz2`.
- Назначение: научить студента создать модель, запустить в Gazebo, подключить `ros2_control` и увидеть в `rviz2`.
- Код: минимальный URDF для дифференциальной базы с двумя колесами; YAML-конфиг для `diff_drive_controller`.
- Ожидаемый результат: в Gazebo робот стоит на земле, в `rviz2` видна модель, `ros2_control` работает.
- Типичные ошибки: неправильные массы (робот улетает), забыли добавить `gazebo_ros2_control` plugin, не совпадают joint names.
- Показ на лекции: запуск Gazebo с моделью робота из `3_Robot/`, открытие `rviz2` с отображением `/scan`, `/camera`, tf2.

### Уровень 3: робот из 3_Robot/

- Подсистемы: Simulation, Mobile Base (через `ros2_control`).
- Каталоги и файлы: `tiago_description/urdf/`, `tiago_description/meshes/`, `tiago_gazebo/worlds/`, `tiago_gazebo/launch/`, `tiago_controller_configuration/config/`.
- Nodes: `robot_state_publisher`, `joint_state_publisher`, `gzserver`, `gzclient`, `controller_manager` (`ros2_control`).
- Topics: `/joint_states`, `/tf`, `/cmd_vel`, `/odom`.
- Parameters: `diff_drive_controller` YAML-конфиг.
- Launch: `tiago_gazebo.launch.py`, `display.launch.py`.
- План Б: показать URDF в `rviz2` без Gazebo; показать структуру файлов и объяснить, что Gazebo должен запускаться.

### Что не успеваем в лекции

Xacro-макросы, `<include>`, инерционные расчеты, collision geometry тонкости, `gazebo_ros2_control` plugin детально.

### Источники и проверка фактов

- [URDF Tutorials](http://wiki.ros.org/urdf/Tutorials)
- [ros2_control Documentation](https://control.ros.org/)
- [Gazebo Documentation](https://gazebosim.org/docs)

### Открытые вопросы

Готов ли URDF робота к моменту лекции? Если нет — план Б: статическая схема и фрагменты кода.

## Блок 14. Архитектурный мост к Nav2

### Роль блока в лекции

Nav2 — навигационный стек, который использует все, что студент узнал ранее: topics (`/scan`, `/odom`), actions (`/navigate_to_pose`), tf2 (`map -> odom -> base_link`), parameters, launch. Этот блок показывает, как базовые механизмы собираются в готовый продукт.

### Уровень 1: лекция

- Учебная цель: студент понимает, какие данные Nav2 потребляет, какие выдает, как связаны SLAM, локализация, costmaps и планирование пути.
- Тайминг: 62-67 минут.
- Ключевые концепты: Nav2, `/navigate_to_pose`, SLAM, `slam_toolbox`, `robot_localization`, costmap, planner, controller.
- Новые термины: Nav2 (навигатор робота), SLAM (одновременное построение карты и локализация), costmap (карта стоимости — где можно и нельзя ехать), planner (глобальный маршрут), controller (локальное управление). Nav2 определен в `TERMINOLOGY.md`.
- Порядок объяснения:
  1. Что такое Nav2: стек ROS2, который строит маршрут, объезжает препятствия и едет к цели.
  2. Зачем нужно: самостоятельное перемещение робота по квартире.
  3. Аналогия: Nav2 — это навигатор в автомобиле, но для мобильного робота.
  4. Как выглядит в ROS2:
     - входные данные: `/scan` (LiDAR), `/odom` (одометрия), `/tf` (дерево координат), карта (из SLAM);
     - выход: action `/navigate_to_pose` с goal, feedback, result.
     - внутреннее устройство: global planner (A*), local controller (DWB), costmaps (global, local), behavior tree.
  5. Как выглядит в коде: отправка goal в `/navigate_to_pose`, чтение feedback.
- Фрагменты кода: action client для `/navigate_to_pose` (10 строк Python).
- CLI-команды: тип команды для демо — `ros2 launch nav2_bringup navigation_launch.py ...`; точные параметры (`params_file`, `map`, `use_sim_time`) уточнить в `1_demo/demo5_nav2_architecture.md` после создания контейнера 3_Robot/.
- Источники: [Nav2 Documentation](https://docs.nav2.org/).

### Уровень 2: самостоятельная практика и код

- Файлы: `2_knowledge/nav2_bridge.md`, `1_demo/demo5_nav2_architecture.md`, будущий пример action client в `2_code/nav2_action_client/`.
- Назначение: студент запускает Nav2 в симуляции с TurtleBot или простым роботом и отправляет goal.
- Код: action client для `/navigate_to_pose`.
- Ожидаемый результат: робот в симуляции едет к цели, объезжает препятствия.
- Типичные ошибки: нет карты, нет `/scan`, неправильное tf2-дерево, забыли `slam_toolbox`.

### Уровень 3: робот из 3_Robot/

- Подсистема: Navigation.
- Каталоги и файлы: `pmb2_navigation/pmb2_2dnav/config/`, `pmb2_navigation/pmb2_2dnav/launch/`, `pal_maps/` (15 карт).
- Nodes: Nav2-узлы (`planner_server`, `controller_server`, `bt_navigator`, `slam_toolbox`, `amcl`).
- Topics: `/scan` (вход), `/odom` (вход), `/map` (из SLAM), `/cmd_vel` (выход — команда базе).
- Actions: `/navigate_to_pose` (основной action).
- Frames: `map`, `odom`, `base_link`, `lidar_link`.
- Parameters: `nav2_params.yaml` — параметры планировщика, контроллера, costmaps.
- План Б: показать схему ROS Graph для навигации, структуру YAML-конфига, фрагмент кода action client.

### Что не успеваем в лекции

BT navigator подробно, recovery behaviors, waypoints, keepout zones, Nav2 Smac planner vs NavFn, 3D costmaps.

### Источники и проверка фактов

- [Nav2 Getting Started](https://docs.nav2.org/getting_started/index.html)
- [Nav2 Concepts](https://docs.nav2.org/concepts/index.html)

### Открытые вопросы

Будет ли Nav2 доступен в контейнере курса, или только в контейнере `3_Robot/`? (Предположительно: Nav2 — в контейнере 3_Robot/; в лекции показать архитектуру и API.)

## Блок 15. Архитектурный мост к MoveIt2

### Роль блока в лекции

MoveIt2 — стек для планирования движений манипулятора. Он использует модель робота (URDF), joint limits, planning scene и actions. Блок показывает, как те же базовые механизмы (actions, parameters, tf2) работают для манипуляции.

### Уровень 1: лекция

- Учебная цель: студент понимает, как MoveIt2 использует модель робота и планирует траектории через actions.
- Тайминг: 67-72 минуты.
- Ключевые концепты: MoveIt2, planning scene, kinematics (IK/FK), MoveGroup, trajectory execution.
- Новые термины: MoveIt2 (планировщик движений руки), planning scene (сцена планирования — мир + робот), IK (обратная кинематика), MoveGroup (основной интерфейс MoveIt2). Определены в `TERMINOLOGY.md`.
- Порядок объяснения:
  1. Что такое MoveIt2: стек ROS2 для планирования движений манипулятора с учетом модели, столкновений и ограничений суставов.
  2. Зачем нужно: рука не может просто "поехать в точку" — нужен план траектории без столкновений.
  3. Аналогия: MoveIt2 — это диспетчер движения руки, который проверяет путь до команды приводам.
  4. Как выглядит в ROS2:
     - вход: URDF робота, joint limits, planning scene (препятствия).
     - выход: trajectory (action), которая передается в `ros2_control` для выполнения.
     - основной интерфейс: `move_group` action server.
  5. Как выглядит в коде: `MoveGroupInterface` задает цель, планирует и выполняет.
- Фрагменты кода: вызов `move_group` для перемещения схвата в позицию (5-7 строк Python).
- CLI-команды: тип команды для демо — `ros2 launch <moveit_config_package> demo.launch.py`; точную команду уточнить в `1_demo/demo6_moveit2_architecture.md` после появления MoveIt2-конфига.
- Источники: [MoveIt2 Documentation](https://moveit.picknik.ai/main/index.html).

### Уровень 2: самостоятельная практика и код

- Файлы: `2_knowledge/moveit2_bridge.md`, `1_demo/demo6_moveit2_architecture.md`, будущий пример MoveIt2 API в `2_code/moveit2_motion_client/`.
- Назначение: студент запускает MoveIt2 с демо-роботом (например, Panda) и двигает руку через `rviz2`.
- Код: `move_group` Python API для планирования позиции схвата.
- Ожидаемый результат: манипулятор в `rviz2` планирует и выполняет движение.
- Типичные ошибки: цель вне рабочей области, self-collision (рука врезается в себя), забыли запустить `move_group`.

### Уровень 3: робот из 3_Robot/

- Подсистема: Manipulation.
- Каталоги и файлы: `tiago_moveit_config/` (move_group.launch.py, config/srdf/, config/kinematics*, config/ompl_planning.yaml).
- Nodes: `move_group`, контроллеры `ros2_control` (joint_trajectory_controller, servo_controller).
- Actions: планирование траектории (через `move_group`), выполнение (через `ros2_control`).
- Frames: `base_link`, `arm_1_link`, `arm_2_link`, ..., `gripper_link`.
- Parameters: `moveit2_controllers.yaml`, joint limits, velocity limits.
- План Б: показать схему MoveIt2 pipeline, структуру конфигов, фрагмент кода Python API.

### Что не успеваем в лекции

KDL vs TRAC-IK, OMPL, CHOMP, STOMP, MoveIt Setup Assistant, perception integration.

### Источники и проверка фактов

- [MoveIt2 Tutorials](https://moveit.picknik.ai/main/doc/tutorials/tutorials.html)
- [MoveIt2 Concepts](https://moveit.picknik.ai/main/doc/concepts/concepts.html)

### Открытые вопросы

Будет ли MoveIt2 настроен для рук робота к моменту лекции? (Если нет — план Б: архитектурная схема, конфиги, фрагменты кода.)

## Блок 16. Архитектурный мост к YOLO

### Роль блока в лекции

YOLO — модель компьютерного зрения. Блок показывает, как подключить модель распознавания как ROS2-узел, публикующий факты в `/detections`.

Ключевое правило безопасности: YOLO публикует факты и confidence, но не принимает финальные решения о движении и не управляет приводами напрямую.

### Уровень 1: лекция

- Учебная цель: студент понимает, как YOLO подключается к ROS2 через camera topic -> detection node -> `/detections`, и где проходит граница ответственности perception.
- Тайминг: 72-76 минут.
- Ключевые концепты: YOLO, detection, `/detections`, confidence, граница perception/control.
- Новые термины: YOLO (модель компьютерного зрения — "быстрый детектор объектов"), `/detections` (topic с результатами распознавания), confidence (уверенность детекции). Определены в `TERMINOLOGY.md`.
- Порядок объяснения:
  1. Что такое YOLO в ROS2: узел, который подписан на `/camera/image_raw` и публикует найденные объекты в `/detections`.
  2. Зачем нужно: робот должен видеть кота, человека, дверь, воду, дым — и сообщать об этом другим подсистемам.
  3. Аналогия: YOLO — это зрение, которое быстро говорит: "вижу объект здесь, с такой-то уверенностью".
  4. Как выглядит в ROS2: `camera_node -> /camera/image_raw -> yolo_node -> /detections -> safety_node, planner`.
  5. Как выглядит в коде: YOLO-узел принимает изображение, прогоняет через модель, публикует `vision_msgs/Detection2DArray`.
  6. Граница безопасности: YOLO не управляет движением. Он сообщает факты — решение принимает safety/planner.
- Фрагменты кода: фрагмент YOLO-узла (подписка на image, публикация detections, 8-10 строк Python).
- CLI-команды: `ros2 topic echo /detections`.
- Источники: [vision_msgs](https://github.com/ros-perception/vision_msgs), [YOLO + ROS2 примеры](https://github.com/ros-perception/vision_opencv).

### Уровень 2: самостоятельная практика и код

- Файлы: `2_knowledge/yolo_bridge.md`, `1_demo/demo7_yolo_perception.md`, будущий минимальный YOLO-node в `2_code/yolo_detection_node/`.
- Назначение: студент запускает YOLO-узел в контейнере с тестовым изображением или веб-камерой.
- Код: минимальный YOLO-узел на Python с `cv_bridge` и `vision_msgs`.
- Ожидаемый результат: `ros2 topic echo /detections` показывает bounding boxes и confidence.
- Типичные ошибки: забыли `cv_bridge`, неправильный message type, YOLO-модель не загружена.

### Уровень 3: робот из 3_Robot/

- Подсистема: Perception.
- Статус: **не реализовано** (запланировано в `TIAgo_conf_improv_plan.md` как пакет `tiago_yolo`).
- Каталоги и файлы (будущие): `tiago_yolo/` (новый изолированный пакет — `yolo_node.py`, `launch/yolo_bringup.launch.py`, `config/yolo_params.yaml`).
- Близкое существующее: `pal_msgs/pal_detection_msgs/` — типы сообщений (bounding box, confidence). Камера уже публикует `/head_front_camera/rgb/image_raw` в Gazebo.
- Nodes: `camera_node` (существующий), `yolo_node` (планируется).
- Topics: `/head_front_camera/rgb/image_raw` (вход, уже есть), `/detections` (выход — `vision_msgs/Detection2DArray`, планируется).

### Что не успеваем в лекции

Обучение YOLO, выбор модели (YOLOv8 vs v11), трекинг объектов (DeepSORT, ByteTrack), `vision_msgs` детально.

### Источники и проверка фактов

- [vision_msgs](https://github.com/ros-perception/vision_msgs)
- [cv_bridge](https://github.com/ros-perception/vision_opencv)

### Открытые вопросы

Будет ли YOLO-узел запускаться в контейнере курса или только в `3_Robot/`? (Предположительно: в 3_Robot/; в лекции — архитектура, код и API.)

## Блок 17. Архитектурный мост к LLM bridge

### Роль блока в лекции

LLM bridge переводит голосовую или текстовую команду человека в разрешенные high-level actions робота.

Ключевое правило безопасности: LLM не управляет моторами, PWM, током, скоростью колес или сервоприводами напрямую. Он может только сформировать high-level request, который проходит через policy layer и safety layer.

### Уровень 1: лекция

- Учебная цель: студент понимает архитектуру LLM bridge, его место в ROS Graph и жесткие ограничения безопасности.
- Тайминг: 76-80 минут.
- Ключевые концепты: LLM bridge, policy layer, safety layer, high-level action, MCP, Behavior Tree.
- Новые термины: LLM bridge (мост от команды человека к разрешенному действию робота), policy layer (слой политик — что разрешено, а что нет), safety layer (слой аварийной защиты). Определены в `TERMINOLOGY.md`.
- Порядок объяснения:
  1. Что такое LLM bridge: узел или набор узлов, который переводит текстовую/голосовую команду в разрешенные высокоуровневые действия.
  2. Зачем нужно: вместо ручного управления пользователь говорит "принеси тапочки", а bridge формирует план действий.
  3. Аналогия: LLM bridge — это переводчик с человеческого языка на язык действий робота, но с жесткими правилами: перевести можно только разрешенные фразы.
  4. Как выглядит в ROS2:
     - вход: голосовая/текстовая команда;
     - обработка: LLM -> task planner -> Behavior Tree;
     - выход: high-level actions (например, goal для `/navigate_to_pose`, цель для MoveIt2);
     - обязательная проверка: policy layer (разрешено ли действие) и safety layer (безопасно ли сейчас).
  5. Как выглядит в коде: фрагмент bridge-узла — прием текста, запрос к LLM, формирование goal.
  6. Граница безопасности: LLM bridge не может напрямую вызвать `/cmd_vel` или установить PWM. Все команды проходят policy и safety.
- Фрагменты кода: схема pipeline (5-7 шагов), фрагмент bridge-узла.
- CLI-команды: не применимы напрямую; показать схему.
- Источники: [MCP Specification](https://modelcontextprotocol.io/), [Nav2 Behavior Trees](https://docs.nav2.org/behavior_trees/index.html).

### Уровень 2: самостоятельная практика и код

- Файлы: `2_knowledge/llm_bridge.md`, `1_demo/demo8_llm_bridge_safety.md`, будущий безопасный bridge-узел в `2_code/llm_bridge_stub/`.
- Назначение: студент запускает минимальный bridge-узел, который принимает текстовую команду и преобразует ее в ROS2 action.
- Код: bridge-узел с фиксированным словарем команд (без LLM API на первых порах).
- Ожидаемый результат: отправка команды "go to kitchen" вызывает `/navigate_to_pose`.
- Типичные ошибки: LLM генерирует непредусмотренную команду, нет валидации через policy layer.

### Уровень 3: робот из 3_Robot/

- Подсистемы: LLM Bridge, Safety, Navigation, Manipulation.
- Каталоги и файлы: `tiago_llm_bridge/` (новый изолированный пакет, планируется в `TIAgo_conf_improv_plan.md`).
- Nodes: `llm_bridge_node`, `task_planner`, `behavior_tree_engine`, `safety_node`, `policy_node`.
- Topics/service/actions:
  - вход: `/voice_command` (std_msgs/String), `/text_command` (std_msgs/String);
  - выход: goal для `/navigate_to_pose` (Nav2 action), цель для `move_group` (MoveIt2 action);
  - safety: `/emergency_stop` (service), `/battery_state` (topic).
- План Б: показать схему pipeline: `команда -> LLM -> task planner -> BT -> policy -> safety -> Nav2/MoveIt2`. Показать, что LLM не подключен напрямую к `/cmd_vel`.

### Что не успеваем в лекции

MCP протокол подробно, Behavior Tree подробно, prompt engineering для LLM, rate limiting, failover при потере сети.

### Источники и проверка фактов

- [ROS2 Behavior Tree](https://navigation.ros.org/behavior_trees/index.html)
- [MCP Specification](https://modelcontextprotocol.io/)

### Открытые вопросы

Будет ли LLM bridge реализован к моменту лекции? Если нет — план Б: архитектурная схема pipeline, ограничения безопасности, фрагменты кода.

## Блок 18. Мини-проект: связать несколько узлов в систему

### Роль блока в лекции

Мини-проект не входит в 80 минут лекции. Это самостоятельная работа, которая объединяет темы 1-17 в один сценарий: студент создает несколько узлов, запускает их через launch, проверяет связи через CLI и видит маленькую работающую систему.

### Уровень 1: лекция

Не входит в 80 минут. В конце лекции преподаватель дает ссылку и кратко описывает сценарий.

- Тайминг: упоминание в конце блока 17 (76-80 минут) как маршрут дальнейшей работы; приводит алгоритм последовательности проектирования робота на ROS2.
- Что сказать: "Вы узнали все базовые механизмы ROS2. Теперь соберите их вместе — напишите систему из 3-4 узлов, запустите через launch и убедитесь, что данные идут по цепочке. Подробная инструкция — в `2_practice/` и `2_code/`."

### Уровень 2: самостоятельная практика и код

- Файлы: `2_practice/08_mini_project.md`, `2_code/mini_project/`, файл с инструкцией-пайплайном последовательного создания робота.
- Назначение: студент создает пакет с несколькими узлами, которые работают вместе.
- Сценарий: робот публикует данные датчика (число), service-узел обрабатывает запрос, action-узел выполняет длительную задачу, launch запускает все вместе.
- Код: ~4 узла (publisher, subscriber, service server, action server) + launch-файл + YAML config.
- Ожидаемый результат: `ros2 launch` запускает систему; `ros2 topic echo`, `ros2 service call`, `ros2 action send_goal` работают.
- Типичные ошибки: забыли `spin()` в одном из узлов, неправильные имена topics, namespace conflicts.

### Уровень 3: робот из 3_Robot/

- Подсистемы: все.
- Фрагмент: студент сравнивает свой мини-проект с архитектурой робота. Где в роботе publisher? Где service? Где action? Где launch?
- Задача: найти в `3_Robot/TIAgo_humble/AGENTS.md` и `3_Robot/TIAgo_humble/TIAgo_configuration.md` те же механизмы и сопоставить со своим кодом.

### Что не успеваем в лекции

Весь блок 18 — самостоятельная работа. В лекции только упоминание и ссылка.

### Источники и проверка фактов

- Все предыдущие источники.

### Открытые вопросы

Нет.

## Итоговая проверка связности

- Все 18 блоков согласованы с `COURSE_ARCHITECTURE.md` (порядок тем, тайминг).
- Каждый блок явно делится на уровни 1, 2 и 3.
- Блоки 14-17 (Nav2, MoveIt2, YOLO, LLM bridge) выделены в отдельные темы с детальной архитектурной привязкой к роботу.
- Для YOLO и LLM bridge явно зафиксированы ограничения безопасности: YOLO не управляет приводами, LLM не получает прямой доступ к моторам.
- Все примеры кода — минимальные, на Python, актуальные для ROS2 Jazzy, с CLI-командами.
- Все практики и демонстрации подразумевают контейнерную среду (общий контейнер курса или контейнер `3_Robot/`).
- Для каждой темы указаны будущие файлы и каталоги, но без попытки создать готовый каркас.
- Для каждой темы зафиксированы типичные ошибки, источники и открытые вопросы.
- Для блоков, где робот может не запускаться (13-17), указан план Б: архитектурная схема, конфиги, фрагменты кода.
- Документ готов к использованию ИИ-агентами для углубления любого блока без повторного обсуждения архитектуры курса.
