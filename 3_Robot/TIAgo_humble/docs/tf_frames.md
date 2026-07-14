# TF-дерево TIAGo — координатные системы

tf2 хранит и вычисляет преобразования между всеми coordinate frames робота: от глобальной карты (`map`) до кончика пальца (`gripper_link`). Без tf2 робот не знает, где лазер относительно базы, а база относительно карты.

> Связь с теорией: [`2_knowledge/tf2.md`](../../2_knowledge/tf2.md) — tf2 как база данных transforms.

---

## TF-дерево TIAGo

```
map  (глобальная система координат — SLAM/AMCL)
  └── odom  (одометрия — DiffDriveController или DLO)
        └── base_footprint  (проекция робота на пол — Nav2 base_frame_id)
              └── base_link  (корневой фрейм робота)
                    ├── torso_lift_link  (выдвижной торс)
                    │     ├── head_1_link → head_2_link (голова, pan/tilt)
                    │     │     └── camera_link (RGB-D камера)
                    │     └── arm_1_link → arm_7_link (манипулятор 7-DOF)
                    │           └── wrist_ft_link → gripper_link (эндектор)
                    └── base_laser_link (лазерный сканер)
```

**Ключевые связи:**
- `map` → `odom` — публикуется AMCL или slam_toolbox (меняется при перелокализации)
- `odom` → `base_footprint` — публикуется DiffDriveController (public) или DLO (private)
- `base_footprint` → `base_link` — публикуется robot_state_publisher (статический transform)
- `base_link` → сенсоры/рука — публикуется robot_state_publisher (из URDF)

**Узлы, публикующие transforms:**

| Узел | Публикует | Частота |
|---|---|---|
| `robot_state_publisher` | `base_footprint→base_link→...→gripper_link` | 50 Гц |
| `DiffDriveController` | `odom→base_footprint` | 50 Гц |
| `amcl` | `map→odom` | 50 Гц |
| `slam_toolbox` | `map→odom` | 10–20 Гц |

---

## Команды проверки

```bash
# Визуализация дерева (генерирует PDF)
ros2 run tf2_tools view_frames

# Трансформ между двумя фреймами
ros2 run tf2_ros tf2_echo map base_link

# Трансформ в реальном времени (через топик)
ros2 topic echo /tf --once | head -30

# Статический трансформ
ros2 topic echo /tf_static --once | head -30

# Проверить все фреймы в данный момент
ros2 run tf2_ros tf2_frames
```

---

## Типичные ошибки

| Ошибка | Симптом | Исправление |
|---|---|---|
| Frame_id не совпадает | transform пустой, rqt_tf_tree не показывает связь | Все топики должны иметь `header.frame_id` из существующего узла дерева |
| Разные timestamp | tf2_echo показывает ошибку extrapolation | Все transform-ы должны быть в одном времени (use_sim_time) |
| Нет `robot_state_publisher` | Дерево обрывается на `base_link` | Добавить узел в launch |
| Дублирующиеся transforms | rqt_tf_tree показывает два источника одного frame | Проверить, не публикуют ли два узла один transform |

---

## Расширяющий материал

### Почему `map → odom → base_footprint → base_link`, а не `map → base_link`

Nav2 разделяет `map` (глобальная система, фиксирована) и `odom` (локальная, дрейфует). `map → odom` — это оценка положения робота на карте (от AMCL или SLAM). `odom → base_footprint` — одометрия, которая со временем накапливает ошибку. Разделение позволяет AMCL корректировать позицию рывком (`map → odom` прыгает), а одометрия остаётся гладкой.

`base_footprint` — это проекция `base_link` на пол (x,y,yaw — без z, roll, pitch). Nav2 использует `base_footprint` как `base_frame_id` для costmaps, потому что планировщик работает в 2D.

### Отладка через `view_frames`

`view_frames` создаёт PDF-файл с полным деревом transform-ов. Если дерево обрывается — ищите недостающий узел или неправильный `parent_frame_id`. Команда требует `tf2_tools`:

```bash
sudo apt install ros-humble-tf2-tools
ros2 run tf2_tools view_frames
evince frames.pdf
```

---

## Ссылки

- [tf2 Introduction](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Tf2/Tf2-Main.html)
- [TIAgo_configuration.md — TF-дерево](../TIAgo_configuration.md#5-tf-дерево)
- [REP-105: Coordinate Frames](https://www.ros.org/reps/rep-0105.html)
