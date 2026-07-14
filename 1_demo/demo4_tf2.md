# Демонстрация: tf2 — дерево координат и визуализация

## Цель

Показать tf2 в действии: (1) `static_broadcaster` публикует transform `world → robot_base` (x=1.0, y=2.0), `tf_listener` читает и выводит координаты; (2) `tf2_echo world robot_base` — живой вывод transform из CLI; (3) `view_frames` — PDF с деревом координат; (4) добавление второго transform `robot_base → sensor` — tf2 автоматически вычисляет `world → sensor` как сумму transforms; (5) визуализация в rviz2 (если доступен GUI).

## Подготовка до лекции

1. Контейнер уровня 2 открыт и готов.
2. Пакет `tf2_demo` собран (код из [практики 07](../2_practice/07_tf2.md)).
3. Открыты два терминала.
4. Для `rviz2`: проверен X11-проброс (`echo $DISPLAY`).
5. Заранее сгенерирован `frames.pdf` и сохранен для показа, если `view_frames` не сработает.

## Контейнер

Dev Container уровня 2 — общий контейнер курса.

## Контекст для студентов

> «Робот — это не одна система координат. Лидар видит в `lidar_link`, моторы едут в `base_link`, карта — в `map`. tf2 связывает их в дерево и автоматически пересчитывает координаты между любыми frames. Увидим, как это работает.»

---

## Что показать

### 1. Запуск broadcast и listener

Терминал 1:

```bash
ros2 run tf2_demo static_broadcaster
# [INFO] [static_frame_publisher]: Static transform world → robot_base published
```

Терминал 2:

```bash
ros2 run tf2_demo tf_listener
# [INFO] [tf_listener]: robot_base in world: x=1.00, y=2.00, z=0.00
```

**Что сказать**: «Static transform `world → robot_base` с координатами (1.0, 2.0, 0.0). Listener запрашивает transform раз в секунду и выводит координаты. Эти же данные лежат в топике `/tf_static`.»

### 2. Живой вывод через tf2_echo

Остановить listener (`Ctrl+C`). Показать:

```bash
ros2 run tf2_ros tf2_echo world robot_base
# - Translation: [1.000, 2.000, 0.000]
# - Rotation: in Quaternion [0.000, 0.000, 0.000, 1.000]
```

**Что сказать**: «`tf2_echo` — главный инструмент отладки tf2. Показывает transform между любыми двумя frames в реальном времени. Если transform не найден — будет ждать или выведет ошибку.»

### 3. Дерево координат через view_frames

```bash
ros2 run tf2_tools view_frames
# Создает frames.pdf в текущей директории
```

**Что сказать**: «`view_frames` генерирует PDF с деревом координат. Сейчас — одно ребро: `world → robot_base`. В реальном роботе — 20+ frames от карты до кончиков пальцев манипулятора.»

**Показать PDF** — открыть `frames.pdf` в просмотрщике.

### 4. Цепочка transforms: добавление sensor

Добавить в код `static_broadcaster.py` второй transform (показать на слайде или в редакторе):

```python
# TransformStamped — полное описание transform между двумя фреймами
t2 = TransformStamped()
t2.header.stamp = self.get_clock().now().to_msg()  # Временная метка transform
t2.header.frame_id = 'robot_base'     # Родительский фрейм (откуда)
t2.child_frame_id = 'sensor'          # Дочерний фрейм (куда)
t2.transform.translation.x = 0.5      # Смещение по оси X, метры
t2.transform.translation.y = 0.0      # Смещение по оси Y
t2.transform.translation.z = 0.3      # Смещение по оси Z
t2.transform.rotation.w = 1.0         # Кватернион (0,0,0,1) — нет поворота
# Публикуем — tf2 автоматически свяжет world→robot_base + robot_base→sensor = world→sensor
self.broadcaster.sendTransform(t2)
```

Перезапустить static_broadcaster. Показать:

```bash
# tf2_echo <target_frame> <source_frame> — живые координаты source в системе target
# tf2 прошёл по цепочке: robot_base найден в world, sensor найден в robot_base → сложил transforms
ros2 run tf2_ros tf2_echo world sensor
# - Translation: [1.500, 2.000, 0.300]
```

**Что сказать**: «Смотрите: мы добавили sensor на (0.5, 0.0, 0.3) относительно robot_base. tf2 автоматически вычислил положение sensor в world: (1.0+0.5, 2.0+0.0, 0.0+0.3) = (1.5, 2.0, 0.3). tf2 автоматически идет по цепочке `world → robot_base → sensor`.»

```bash
# view_frames — генерирует PDF с графом transforms (теперь: world → robot_base → sensor)
ros2 run tf2_tools view_frames
# Теперь дерево: world → robot_base → sensor
```

### 5. Визуализация в rviz2 (если есть GUI)

```bash
# rviz2 — визуализатор ROS2. Добавить TF display → увидеть frames и их связи
rviz2
```

**Что сказать**: «Добавьте TF display в rviz2 — увидите все frames и связи между ними. Это же дерево используется в роботе TIAGo для навигации и манипуляции.»

Если rviz2 недоступен — показать иллюстрацию из `frames.pdf` или скриншот.

---

## Что сказать (ключевые фразы)

- «tf2 — это не просто `ros2 topic echo /tf`. Это база данных transforms, которая умеет ходить по цепочке и пересчитывать координаты.»
- «Без tf2 невозможна навигация. Лидар видит препятствие в `lidar_link`, а планировщику нужны координаты в `map`. tf2 автоматически пересчитывает.»
- «Дерево tf2 должно быть деревом — без циклов. Иначе `lookup_transform` упадет.»
- «Static transforms (`/tf_static`) публикуются один раз и не меняются. Dynamic transforms (`/tf`) обновляются постоянно — например, `odom → base_link` меняется при движении.»
- «`tf2_echo` и `view_frames` — два главных инструмента отладки. Если робот не понимает, где находится — первым делом проверьте tf2-дерево.»

## Ожидаемый результат

- `tf2_echo world robot_base` показывает Translation: [1.0, 2.0, 0.0]
- `tf2_echo world sensor` показывает Translation: [1.5, 2.0, 0.3] (автоматическая цепочка)
- `view_frames` генерирует PDF с деревом из 2-3 frames
- В rviz2 видна визуализация TF (если доступен GUI)

## Типичные проблемы

| Симптом | Причина | Исправление |
| --- | --- | --- |
| `tf2_echo` бесконечно ждет | Transform не опубликован | Проверить, что static_broadcaster запущен и в `spin()` |
| `view_frames` — pdf пустой или ошибка | Нет запущенных узлов | Запустить все узлы, затем выполнить `view_frames` |
| `rviz2` не запускается | Нет DISPLAY или X11-проброса | Проверить `echo $DISPLAY` |
| `tf2_echo` не находит второй frame | Разные frame_id | Регистр важен: `sensor` vs `Sensor` |

## План Б

Если GUI не работает (нет `rviz2`, невозможно открыть PDF):

1. Показать заранее сохраненный скриншот `frames.pdf` и rviz2.
2. Показать Mermaid-диаграмму дерева из статьи [tf2](../2_knowledge/tf2.md).
3. Объяснить: «На ваших компьютерах rviz2 покажет дерево вживую. Сейчас смотрим на схему: `world → robot_base → sensor`. Так же устроено дерево робота TIAGo — только frames больше.»

## Ссылки на материалы курса

- [tf2 — статья базы знаний](../2_knowledge/tf2.md)
- [Практика 07: tf2](../2_practice/07_tf2.md)

## Связь с роботом

В архитектуре робота TIAGo tf2-дерево содержит 20+ frames:

```
map → odom → base_footprint → base_link → chassis_link →
  lidar_link
  camera_link
  left_wheel_link
  right_wheel_link
  arm_1_link → arm_2_link → ... → arm_7_link → gripper_link
```

Это дерево используется:
- **Nav2** — для преобразования `/scan` из `lidar_link` в `map`;
- **MoveIt2** — для планирования движений руки из `base_link`;
- **rviz2** — для визуализации всего робота в одном окне.