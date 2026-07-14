# Шпаргалка: ROS2 CLI

> **Примеры команд приведены для робота TIAGo.** В режиме навигации (Gazebo) все топики, узлы, сервисы и actions активны — запустите симуляцию и выполняйте команды для исследования системы в реальном времени.
>
> Типовые топики TIAGo: `/scan` (LiDAR), `/odom` (одометрия), `/cmd_vel` (скорость), `/joint_states` (суставы), `/camera/image_raw` (камера).

## Проверка окружения

```bash
ros2 --help                         # справка по CLI
ros2 doctor --report                # диагностика окружения
printenv RMW_IMPLEMENTATION          # какой DDS используется
```

## Workspace и сборка

```bash
mkdir -p ~/ros2_ws/src              # создать workspace
cd ~/ros2_ws
ros2 pkg create --build-type ament_python <name> --dependencies rclpy std_msgs
colcon build                        # собрать workspace
colcon build --packages-select <pkg> # собрать один пакет
colcon build --symlink-install      # без пересборки при изменении Python
source install/setup.bash           # активировать workspace
```

## Nodes

```bash
ros2 run <pkg> <executable>         # запустить узел
ros2 node list                      # список узлов
ros2 node info /<node>              # подписки, публикации, сервисы
rqt_graph                           # визуализация ROS Graph

# TIAgo: типовые узлы в навигации
# ros2 node list покажет:
#   /camera_node  /lidar_node  /motor_controller
#   /planner_server  /controller_server  /bt_navigator
#   /amcl  /robot_state_publisher  /joint_state_broadcaster
ros2 node info /planner_server     # TIAgo: публикует /cmd_vel, подписан на /scan, /odom
```

## Topics

```bash
ros2 topic list                     # список topics
ros2 topic echo /<topic>            # читать в реальном времени
ros2 topic pub --once /<topic> <type> "<yaml>"  # вставить сообщение
ros2 topic hz /<topic>              # частота публикации
ros2 topic info /<topic>            # тип, количество pub/sub
ros2 topic bw /<topic>              # пропускная способность

# TIAgo: исследование топиков в навигации
ros2 topic list                     # TIAgo: /scan /odom /cmd_vel /joint_states /tf /tf_static ...
ros2 topic echo /scan               # TIAgo: LiDAR — sensor_msgs/LaserScan, 10 Гц
ros2 topic echo /odom               # TIAgo: одометрия — nav_msgs/Odometry
ros2 topic echo /cmd_vel            # TIAgo: команды скорости — geometry_msgs/Twist
ros2 topic echo /joint_states       # TIAgo: состояние суставов — sensor_msgs/JointState
ros2 topic echo /camera/image_raw   # TIAgo: видеопоток — sensor_msgs/Image
ros2 topic hz /scan                 # TIAgo: частота LiDAR — ~10 Гц
ros2 topic info /scan               # TIAgo: тип + количество pub/sub
```

## Services

```bash
ros2 service list                   # список services
ros2 service type /<service>        # тип service
ros2 service call /<service> <type> "<yaml>"  # вызвать из CLI
ros2 service find <type>            # найти все с заданным типом

# TIAgo: сервисы управления
ros2 service list                   # TIAgo: /emergency_stop /motor_power /reset_motors
ros2 service type /emergency_stop   # TIAgo: std_srvs/srv/SetBool
ros2 service call /emergency_stop std_srvs/srv/SetBool "{data: true}"
                                    # TIAgo: аварийная остановка
ros2 service call /motor_power std_srvs/srv/SetBool "{data: false}"
                                    # TIAgo: отключить моторы
```

## Actions

```bash
ros2 action list                    # список actions
ros2 action info /<action>          # тип, clients/servers
ros2 action send_goal /<action> <type> "<yaml>" --feedback  # отправить goal

# TIAgo: actions навигации Nav2
ros2 action list                    # TIAgo: /navigate_to_pose /follow_path /compute_path_to_pose
ros2 action info /navigate_to_pose  # TIAgo: nav2_msgs/action/NavigateToPose
ros2 action send_goal /navigate_to_pose nav2_msgs/action/NavigateToPose \
  "{pose: {pose: {position: {x: 2.0, y: 1.0, z: 0.0}, orientation: {w: 1.0}}}}" --feedback
                                    # TIAgo: отправить робота в точку (2.0, 1.0)
```

## Parameters

```bash
ros2 param list                     # список параметров
ros2 param get /<node> <param>      # прочитать значение
ros2 param set /<node> <param> <val> # изменить на лету
ros2 param dump /<node> > file.yaml # сохранить в YAML
ros2 param load /<node> file.yaml   # загрузить из YAML

# TIAgo: параметры навигации
ros2 param list /planner_server     # TIAgo: параметры planner_server
ros2 param get /controller_server controller_plugin
                                    # TIAgo: тип controller (DWB, MPPI...)
ros2 param set /controller_server max_vel_x 0.5
                                    # TIAgo: ограничить скорость на лету
ros2 param dump /controller_server > controller.yaml
                                    # TIAgo: сохранить параметры контроллера
```

## Launch

```bash
ros2 launch <pkg> <file.launch.py>                # запустить launch
ros2 launch <pkg> <file.launch.py> <arg>:=<val>   # с аргументом
ros2 launch <pkg> <file.launch.py> --show-args    # показать аргументы
```

## tf2

```bash
ros2 run tf2_ros tf2_echo <parent> <child>  # transform между frames
ros2 run tf2_tools view_frames              # PDF с деревом координат
ros2 topic echo /tf_static                  # статические transforms
ros2 topic echo /tf                         # динамические transforms

# TIAgo: дерево координат (20+ frames)
ros2 run tf2_ros tf2_echo map odom             # TIAgo: глобальный transform
ros2 run tf2_ros tf2_echo odom base_link       # TIAgo: одометрия → база
ros2 run tf2_ros tf2_echo base_link lidar_link # TIAgo: база → LiDAR
ros2 run tf2_ros tf2_echo base_link camera_link # TIAgo: база → камера
ros2 run tf2_ros tf2_echo base_link arm_1_link  # TIAgo: база → первый сустав руки
ros2 run tf2_tools view_frames                 # TIAgo: PDF со всем деревом
```

## Lifecycle

```bash
ros2 lifecycle list                    # список lifecycle nodes
ros2 lifecycle set /<node> configure   # переход: unconfigured → inactive
ros2 lifecycle set /<node> activate    # переход: inactive → active
ros2 lifecycle set /<node> deactivate  # переход: active → inactive
ros2 lifecycle set /<node> shutdown    # переход: → finalized

# TIAgo: управление жизненным циклом драйверов
ros2 lifecycle list                    # TIAgo: /lidar_node /camera_node /motor_controller
ros2 lifecycle set /lidar_node configure
                                    # TIAgo: настроить LiDAR (неактивен)
ros2 lifecycle set /lidar_node activate
                                    # TIAgo: запустить публикацию /scan
ros2 lifecycle set /lidar_node deactivate
                                    # TIAgo: остановить LiDAR
```

## Пакеты

```bash
ros2 pkg list                        # список пакетов
ros2 pkg xml <pkg>                   # package.xml пакета
rosdep update && rosdep install --from-paths src --ignore-src -r -y
```