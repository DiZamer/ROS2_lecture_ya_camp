# RMW: ROS Middleware Wrapper

## Коротко

RMW (ROS Middleware) — тонкий слой-адаптер между ROS2 API (rcl/rclcpp/rclpy) и конкретной реализацией DDS. Благодаря RMW можно сменить транспортный протокол, не меняя ни строчки кода узлов.

> *Официальное определение*: «Чтобы использовать реализацию DDS/RTPS с ROS 2, необходимо создать пакет «интерфейса ROS Middleware» (RMW), который реализует абстрактный интерфейс ROS middleware с помощью API и инструментов данной реализации DDS/RTPS.» — [RMW](https://docs.ros.org/en/jazzy/Concepts/Intermediate/About-Different-Middleware-Vendors.html)

## Что это

RMW — это абстрактный интерфейс, который определяет, как:

- создать publisher/subscriber;
- сериализовать и отправить сообщение;
- подписаться на topic;
- объявить service/action;
- запустить discovery.

Каждый RMW — это отдельный ROS2-пакет, реализующий этот интерфейс для конкретного DDS-продукта.

## Зачем нужно

- **Независимость от вендора**. ROS2 не привязан к одному DDS: можно переключаться между Fast DDS, Cyclone DDS, Connext DDS.
- **Гибкость деплоя**. Для учебного робота — Fast DDS, для сертифицированной системы — Connext DDS, для embedded — Cyclone DDS.
- **Тестирование**. Один набор тестов ROS2 прогоняется на всех RMW — гарантия, что API не зависит от реализации.

## Аналогия

RMW — **стойка приёма отправлений** в офисе. Вы пишете письмо (сообщение), кладёте на стойку (RMW), а какой перевозчик (DDS) его заберёт — определяется контрактом с курьерской службой. Перевозчика можно сменить, стойка остаётся той же.

## Как работает в ROS2 Jazzy

### Место в архитектуре

```
┌─────────────────────────────┐
│      Ваш узел (C++/Python)  │
│  ┌───────────────────────┐  │
│  │ rclcpp / rclpy        │  │
│  └───────┬───────────────┘  │
└──────────┼──────────────────┘
           │
┌──────────▼──────────────────┐
│          rcl                │  <- ROS Client Library (общий C-API)
└──────────┬──────────────────┘
           │
┌──────────▼──────────────────┐
│   RMW Interface (rmw.h)     │  <- абстрактный адаптер
└──────────┬──────────────────┘
           │
┌──────────▼──────────────────┐
│  rmw_fastrtps_cpp           │  <- конкретная реализация
│  или rmw_cyclonedds_cpp     │
│  или rmw_connextdds         │
└──────────┬──────────────────┘
           │
┌──────────▼──────────────────┐
│  Fast DDS / Cyclone DDS /   │
│  Connext DDS API            │
└─────────────────────────────┘
```

### Поддерживаемые RMW в Jazzy

| RMW-пакет | DDS-реализация | Статус | Когда использовать |
|---|---|---|---|
| `rmw_fastrtps_cpp` | Fast DDS (eProsima) | **Полная поддержка, дефолт** | Учебные и большинство задач |
| `rmw_cyclonedds_cpp` | Cyclone DDS (Eclipse) | Полная поддержка | Production, embedded |
| `rmw_connextdds` | Connext DDS (RTI) | Полная поддержка | Safety-critical |
| `rmw_gurumdds_cpp` | GurumDDS (GurumNetworks) | Полная поддержка | IoT, малые устройства |
| `rmw_zenoh_cpp` | Zenoh (Eclipse) | Экспериментальная | Cloud/remote |

### Правило выбора дефолта

Если в системе установлено несколько RMW, ROS2 выбирает так:

1. Если есть `rmw_fastrtps_cpp` — он дефолт.
2. Иначе — первый по алфавиту среди установленных.
3. `RMW_IMPLEMENTATION` всегда переопределяет автоматический выбор.

## Команды

```bash
# проверить текущий RMW
printenv RMW_IMPLEMENTATION
ros2 doctor --report

# явно переключить RMW
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp

# установить другой RMW
sudo apt update
sudo apt install ros-jazzy-rmw-cyclonedds-cpp

# запустить с одним узлом на Fast DDS, другим на Cyclone DDS
# (они НЕ увидят друг друга)
# терминал 1:
RMW_IMPLEMENTATION=rmw_fastrtps_cpp ros2 run demo_nodes_cpp talker
# терминал 2:
RMW_IMPLEMENTATION=rmw_cyclonedds_cpp ros2 run demo_nodes_cpp listener
```

## Ожидаемый результат

- `ros2 doctor --report` показывает выбранный RMW.
- Два узла на разных RMW **не обнаруживают друг друга** (разные DDS-реализации несовместимы «из коробки»).
- Узлы на одном RMW работают вне зависимости от `RMW_IMPLEMENTATION` в переменной.

## Типичные ошибки

| Симптом | Причина | Исправление |
|---|---|---|
| Узлы на одном хосте не видят друг друга | Разные `RMW_IMPLEMENTATION` | Выставить одинаковый RMW |
| `ros2 doctor` жалуется на отсутствие RMW | Не установлен ни один RMW-пакет | `sudo apt install ros-jazzy-rmw-fastrtps-cpp` |
| Демо работает на Fast DDS, но отказывается на Cyclone | Разные настройки QoS по умолчанию | Проверить совместимость QoS (см. [qos.md](qos.md)) |

### Пример в реальном роботе

TIAGo использует `RMW_IMPLEMENTATION=rmw_cyclonedds_cpp` — CycloneDDS, рекомендованный PAL Robotics.
В [`3_Robot/TIAgo_humble/docs/rmw_dds.md`](../../3_Robot/TIAgo_humble/docs/rmw_dds.md) показана настройка RMW,
фиксированный ROS_DOMAIN_ID=56 и конфигурация Shared Memory Transport в контейнере.

## Связанные темы

- [DDS: протокол, транспорт и выбор реализации](dds_protocol.md) — подробное сравнение DDS-реализаций
- [Discovery: автоматическое обнаружение узлов](discovery.md) — как узлы находят друг друга
- [QoS: настройки доставки сообщений](qos.md) — reliability, history, durability
- [Архитектура ROS2](ros_architecture.md) — общая схема middleware

## Источники

- [About Different Middleware Vendors (ROS2 Jazzy)](https://docs.ros.org/en/jazzy/Concepts/Intermediate/About-Different-Middleware-Vendors.html)
- [RMW Implementations (ROS2 Jazzy)](https://docs.ros.org/en/jazzy/Installation/RMW-Implementations.html)
- [REP-2000: DDS/RMW vendors](https://www.ros.org/reps/rep-2000.html)
- [rmw_fastrtps_cpp docs (Jazzy)](https://docs.ros.org/en/jazzy/p/rmw_fastrtps_cpp/)
- [rmw_cyclonedds_cpp docs (Jazzy)](https://docs.ros.org/en/jazzy/p/rmw_cyclonedds_cpp/)
