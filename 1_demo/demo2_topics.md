# Демонстрация: Topic — обмен сообщениями в реальном времени

## Цель

Показать живой обмен данными publisher→subscriber через topic `/chatter`: publisher (`talker`) отправляет `std_msgs/String` раз в секунду, subscriber (`listener`) получает и выводит. Продемонстрировать 5 CLI-команд: `ros2 topic list` (список), `ros2 topic echo` (чтение потока), `ros2 topic info` (тип + счётчики), `ros2 topic hz` (частота), `ros2 topic pub --once` (ручная вставка). Показать, что один publisher может обслуживать несколько subscriber-ов.

## Подготовка до лекции

1. Контейнер уровня 2 открыт и готов.
2. Workspace `~/ros2_ws` создан и активирован.
3. Пакет `topic_demo` собран (код из [практики 03](../2_practice/03_topic.md)).
4. Открыты три терминала.

## Контейнер

Dev Container уровня 2 — общий контейнер курса.

## Контекст для студентов

> «Topic — основной способ обмена данными в ROS2. Publisher отправляет сообщения в именованный канал, subscriber читает. Сейчас увидим это вживую: publisher, subscriber и CLI-инструменты для отладки.»

---

## Что показать

### 1. Запуск publisher и subscriber

Терминал 1 — publisher:

```bash
# Запускаем publisher: публикует std_msgs/String в /chatter каждую секунду
ros2 run topic_demo talker
# [INFO] [talker]: Published: Message #0
# [INFO] [talker]: Published: Message #1
```

Терминал 2 — subscriber:

```bash
# Запускаем subscriber: подписан на /chatter, выводит каждое полученное сообщение
ros2 run topic_demo listener
# [INFO] [listener]: I heard: Message #1
# [INFO] [listener]: I heard: Message #2
```

**Что сказать**: «Publisher отправляет сообщение каждую секунду. Subscriber получает их асинхронно. Они не знают друг о друге — только об имени topic `/chatter` и типе сообщения `String`. Обратите внимание: subscriber начал с Message #1, а не #0. Пока subscriber не запущен, сообщения не накапливаются (при стандартных настройках QoS).»

### 2. CLI-проверка: список topics

Терминал 3:

```bash
# ros2 topic list — все активные topics в системе
# /chatter — наш topic, /parameter_events и /rosout — служебные (их создаёт сам ROS2)
ros2 topic list
# Вывод:
# /chatter
# /parameter_events
# /rosout
```

**Что сказать**: «`ros2 topic list` показывает все активные topics в системе. `/chatter` — наш. `/parameter_events` и `/rosout` — служебные topics самого ROS2.»

### 3. CLI-проверка: чтение из topic

```bash
# ros2 topic echo <topic> — подписывается на topic и выводит каждое сообщение
# Как tail -f для ROS2: видно формат, содержимое, периодичность
ros2 topic echo /chatter
# data: 'Message #5'
# ---
# data: 'Message #6'
# ---
```

**Что сказать**: «`ros2 topic echo` — как `tail -f` для ROS2. Читает сообщения из topic и выводит в терминал. Полезно для отладки: видно, что publisher действительно отправляет данные, и какого они формата.»

### 4. CLI-проверка: информация о topic

```bash
# ros2 topic info <topic> — тип сообщения + сколько publisher/subscriber подключено
ros2 topic info /chatter
# Type: std_msgs/msg/String
# Publisher count: 1
# Subscription count: 1
```

**Что сказать**: «`ros2 topic info` показывает тип сообщения, количество publisher-ов и subscriber-ов. Если subscriber не запущен — `Subscription count: 0`. Это быстрый способ проверить, все ли соединения установлены.»

### 5. CLI-проверка: частота публикации

```bash
# ros2 topic hz <topic> — замер частоты публикации (средняя за последние N сообщений)
ros2 topic hz /chatter
# average rate: 1.0 Hz
```

**Что сказать**: «`ros2 topic hz` измеряет частоту. В роботе `/scan` публикуется с частотой 10 Гц, `/camera/image_raw` — 30 Гц. Если частота падает — проблема с publisher-ом.»

### 6. Ручная вставка сообщения

Не останавливая publisher:

```bash
# ros2 topic pub --once <topic> <тип> <данные> — вставка сообщения в topic из CLI
# --once — одно сообщение (без --once будет публиковать непрерывно)
# std_msgs/String — тип сообщения, "data: '...'" — содержимое
ros2 topic pub --once /chatter std_msgs/String "data: 'Hello from CLI'"
```

Subscriber немедленно показывает:

```
[INFO] [listener]: I heard: Hello from CLI
```

**Что сказать**: «`ros2 topic pub` вставляет сообщение в topic с клавиатуры. Это сообщение пришло не от publisher-а, а от CLI. Subscriber не заметил разницы — для него все сообщения равны. Это мощный инструмент: можно вручную отправить `/cmd_vel` и проверить, как робот реагирует.»

### 7. Множественные subscriber-ы

Запустить еще два subscriber-а (через `&` — в фоне):

```bash
# Два дополнительных subscriber-а — всего 3 подписчика на один topic
ros2 run topic_demo listener &
ros2 run topic_demo listener &
```

Терминал 3:

```bash
# ros2 topic info показывает 3 subscriber-а — все получают одни и те же сообщения
ros2 topic info /chatter
# Subscription count: 3
```

**Что сказать**: «Одно сообщение от publisher-а получают все три subscriber-а одновременно. Topic — это широковещательный канал. В роботе данные лидара `/scan` читают и SLAM, и safety-узел, и визуализатор — все одновременно.»

---

## Что сказать (ключевые фразы)

- «Publisher и subscriber не знают друг о друге. Их связывает только имя topic и тип сообщения. Discovery делает это автоматически.»
- «`ros2 topic echo` — главный инструмент отладки. Если робот не реагирует на команды — первым делом проверьте, идет ли поток в нужном topic.»
- «`ros2 topic pub` позволяет вручную вставить сообщение. В реальном роботе это способ проверить реакцию на команду без перезапуска узлов.»
- «Topic — связь "многие ко многим". Один publisher, много subscriber-ов. Или много publisher-ов, много subscriber-ов. Или вообще без subscriber-ов — publisher все равно публикует.»

## Ожидаемый результат

- `ros2 topic list` показывает `/chatter`
- `ros2 topic echo` показывает поток сообщений
- `ros2 topic hz` показывает ~1.0 Гц
- `ros2 topic pub` вставляет сообщение, subscriber его получает
- `ros2 topic info` показывает 1 pub, 1-3 sub

## Типичные проблемы

| Симптом | Причина | Исправление |
| --- | --- | --- |
| `ros2 topic list` пустой | Узлы не запущены | Запустить talker и listener |
| `ros2 topic echo` пустой | Publisher не публикует | Проверить `spin()` в коде publisher |
| `ros2 topic info` — Sub count: 0 | Subscriber не запущен | Запустить listener |
| «Command not found» для `topic_demo` | Пакет не собран | `colcon build && source install/setup.bash` |

## План Б

Если контейнер не позволяет запустить несколько терминалов:

1. Показать три терминала в одном окне через `tmux` или вкладки VS Code.
2. Если и это невозможно — показать скриншоты каждого шага с выделением ключевого вывода.
3. Объяснить: «У себя вы сможете запустить все три терминала. Сейчас смотрим на примере скриншотов. Обратите внимание: publisher печатает, subscriber читает, CLI показывает topic.»

## Ссылки на материалы курса

- [Topics — статья базы знаний](../2_knowledge/topics.md)
- [Практика 03: Publisher и Subscriber](../2_practice/03_topic.md)

## Связь с роботом

Те же команды работают для topics робота TIAGo:

```bash
ros2 topic echo /scan          # данные лидара
ros2 topic echo /odom          # одометрия
ros2 topic hz /camera/image_raw # частота кадров камеры
ros2 topic info /cmd_vel       # кто отправляет команды базе
```

В архитектуре робота topics — основной транспорт для потоковых данных между подсистемами. `/scan` читают SLAM (строит карту), safety_node (проверяет препятствия) и rviz2 (визуализирует) — три subscriber-а на один topic.