# QoS — качество доставки сообщений

## Коротко

QoS (Quality of Service) — настройки, которые говорят DDS, как доставлять сообщения: надежно или быстро, хранить историю или нет, как долго сообщение актуально.

> *Официальное определение*: «ROS 2 предлагает богатый набор политик Quality of Service (QoS), которые позволяют настраивать общение между узлами.» — [QoS](https://docs.ros.org/en/jazzy/Concepts/Intermediate/About-Quality-of-Service-Settings.html)

## Что такое QoS

Когда вы создаете publisher или subscriber, вы можете указать QoS-профиль — набор правил доставки. По умолчанию ROS2 использует надежную доставку с очередью на 10 сообщений. Но для разных данных нужны разные правила.

## Зачем нужно

- **Данные лидара (`/scan`)** — публикуются 10 раз в секунду. Если кадр потерялся, следующий придет через 0.1 с. Не страшно. QoS: **best effort** (не тратим время на переотправку).
- **Команда скорости (`/cmd_vel`)** — если команда потерялась, робот не остановится перед препятствием. QoS: **reliable** (гарантированная доставка).
- **Карта** — новый subscriber должен получить последнюю версию карты, даже если подписался позже. QoS: **transient local** (хранить последнее сообщение для новых подписчиков).

## Аналогия

QoS — **выбор службы доставки**:
- **Reliable** — заказное письмо с уведомлением. Дороже, медленнее, но точно дойдет.
- **Best effort** — обычное письмо. Быстро и дешево, но может потеряться.

Для счета за электричество (reliable) — нужно подтверждение. Для рекламной листовки (best effort) — не страшно, если не дойдет.

## Главные настройки QoS

### Reliability — надежность

| Значение | Описание | Когда использовать |
| --- | --- | --- |
| `RELIABLE` | DDS гарантирует доставку каждого сообщения. Переотправляет потерянные. | `/cmd_vel`, goal для action, `/emergency_stop` |
| `BEST_EFFORT` | DDS отправляет и забывает. Потерянные сообщения не переотправляются. | `/scan`, `/camera/image_raw`, высокочастотные сенсоры |

### Durability — долговечность

| Значение | Описание | Когда использовать |
| --- | --- | --- |
| `VOLATILE` | Сообщения не хранятся. Новый subscriber не получает старые данные. | Потоковые данные — `/scan`, `/cmd_vel` |
| `TRANSIENT_LOCAL` | Publisher хранит последнее сообщение. Новый subscriber сразу получает его. | Карта, конфигурация, параметры системы |

### History — история

| Параметр | Описание |
| --- | --- |
| `KEEP_LAST` + `depth: N` | Хранить последние N сообщений. По умолчанию depth=10. |
| `KEEP_ALL` | Хранить все сообщения (осторожно — память!). |

## Как задать QoS в коде

```python
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy

# QoS для /scan (LiDAR): best effort — потеря кадра не критична
qos_scan = QoSProfile(
    depth=10,                                    # хранить 10 последних сообщений
    reliability=ReliabilityPolicy.BEST_EFFORT,   # без гарантии доставки — быстрее
    durability=DurabilityPolicy.VOLATILE         # не хранить для новых подписчиков
)

# QoS для карты: reliable, сохранить последнее для новых узлов
qos_map = QoSProfile(
    depth=1,                                     # хранить только 1 сообщение
    reliability=ReliabilityPolicy.RELIABLE,      # гарантировать доставку
    durability=DurabilityPolicy.TRANSIENT_LOCAL  # новый подписчик получит последнюю карту
)

# передаём QoS-профиль вместо depth при создании publisher
self.pub = self.create_publisher(LaserScan, '/scan', qos_scan)
```

## QoS для topics робота TIAGo

| Topic               | Reliability | Durability      | Depth | Почему                                    |
| ------------------- | ----------- | --------------- | ----- | ----------------------------------------- |
| `/scan`             | Best effort | Volatile        | 10    | Поток данных, потеря кадра не критична    |
| `/cmd_vel`          | Reliable    | Volatile        | 10    | Нельзя терять команды управления          |
| `/odom`             | Reliable    | Volatile        | 10    | Навигация зависит от точной одометрии     |
| `/camera/image_raw` | Best effort | Volatile        | 5     | Высокая частота, потеря кадра не критична |
| `/detections`       | Reliable    | Volatile        | 10    | Нельзя терять факт обнаружения объекта    |
| Карта (map)         | Reliable    | Transient local | 1     | Новый узел должен сразу получить карту    |

## Совместимость QoS

**Важно**: publisher и subscriber должны иметь совместимые QoS. ROS2 проверяет это автоматически.

```python
# Publisher: reliable — гарантирует доставку каждого сообщения
pub = self.create_publisher(String, '/test', QoSProfile(
    reliability=ReliabilityPolicy.RELIABLE, depth=10))

# Subscriber: best effort — согласен терять сообщения
sub = self.create_subscription(String, '/test', callback, QoSProfile(
    reliability=ReliabilityPolicy.BEST_EFFORT, depth=10))

# Результат: BEST_EFFORT «слабее» RELIABLE — соединение НЕ СОСТОИТСЯ
# ros2 topic info /test покажет 0 subscriber
```

Правило: subscriber может быть «слабее» publisher, но не «сильнее». Если publisher RELIABLE, subscriber может быть BEST_EFFORT (получать без гарантий). Но если publisher BEST_EFFORT, subscriber не может требовать RELIABLE.

## Привязка к трем уровням

- **Уровень 1 (лекция)**: преподаватель объясняет разницу reliable/best effort на примере `/scan` vs `/cmd_vel`.
- **Уровень 2 (самостоятельно)**: эта статья + демонстрация mismatched QoS (pub и sub не соединяются).
- **Уровень 3 (робот TIAGo)**: таблица QoS для всех topics робота (см. выше).

## Типичные ошибки

| Ошибка | Симптом | Исправление |
| --- | --- | --- |
| Разные reliability у pub и sub | Соединения нет, `ros2 topic info` — 0 subscriber | Использовать совместимые QoS |
| Best effort для важных команд | Команда может потеряться | `/cmd_vel`, goals — только reliable |
| Reliable для высокочастотных сенсоров | Задержки, потеря производительности | Для `/scan`, `/camera/image_raw` — best effort |
| Забыли depth | Очередь по умолчанию (10) | Явно задавать depth под задачу |
| Transient local без необходимости | Расход памяти на хранение | Только для карт и конфигураций |

### Пример в реальном роботе

В TIAGo каждый топик использует свои QoS-настройки: `/scan` — BEST_EFFORT (лазер можно терять),
`/cmd_vel` — RELIABLE (нельзя терять команды скорости),
`/camera/image_raw` — BEST_EFFORT (потоковое видео).
В [`3_Robot/TIAgo_humble/docs/qos_profiles.md`](../../3_Robot/TIAgo_humble/docs/qos_profiles.md) описаны профили QoS
для всех ключевых топиков TIAGo.

## Связанные темы

- [Topics](topics.md) — publisher/subscriber с QoS
- [Lifecycle](lifecycle.md) — управляемый жизненный цикл узла
- [tf2](tf2.md) — координатные преобразования

## Источники

- [About QoS settings](https://docs.ros.org/en/jazzy/Concepts/Intermediate/About-Quality-of-Service-Settings.html)
- [DDS QoS specification](https://www.omg.org/spec/DDS/1.4/PDF)