# Демонстрация: Service — запрос-ответ в реальном времени

## Цель

Показать service server `/add_two_ints` (тип `example_interfaces/srv/AddTwoInts`) в действии: запуск server, проверка `ros2 service list`, вызов через `ros2 service call` с JSON-аргументами `"{a: 5, b: 3}"`, получение ответа `sum: 8`. Продемонстрировать отличие от topic (запрос-ответ vs поток) и показать ошибку «service not available» при вызове без запущенного server.

## Подготовка до лекции

1. Контейнер уровня 2 открыт и готов.
2. Workspace `~/ros2_ws` создан и активирован.
3. Пакет `service_demo` собран (код из [практики 04](../2_practice/04_service.md)).
4. Открыты два терминала.

## Контейнер

Dev Container уровня 2 — общий контейнер курса.

## Контекст для студентов

> «Topic — это поток сообщений. А если нужен конкретный ответ на конкретный запрос? Например, "сколько сейчас батарея?" или "активируй emergency stop". Для этого нужен service — запрос-ответ. Увидим вживую.»

---

## Что показать

### 1. Запуск service server

Терминал 1:

```bash
# Запускаем service server — ждёт запросов на /add_two_ints
ros2 run service_demo server
# [INFO] [add_two_ints_server]: Service ready
```

**Что сказать**: «Server готов принимать запросы. Он не публикует данные непрерывно — он ждет, пока кто-то вызовет service.»

### 2. Проверка доступности service

Терминал 2:

```bash
# ros2 service list — все доступные сервисы (только те, чей server запущен)
ros2 service list
# Вывод:
# /add_two_ints
# ... (служебные services)
```

**Что сказать**: «`ros2 service list` показывает все доступные services. `/add_two_ints` — наш. Обратите внимание: в отличие от topic, service не шлет данные, пока его не вызовут.»

### 3. Узнать тип service

```bash
# ros2 service type <service> — структура request/response (нужно знать, чтобы вызвать)
ros2 service type /add_two_ints
# example_interfaces/srv/AddTwoInts
```

**Что сказать**: «У каждого service есть тип — структура запроса и ответа. `AddTwoInts` принимает два целых числа `a` и `b`, возвращает `sum`. Узнать тип нужно, чтобы правильно вызвать service из CLI.»

### 4. Вызов service из CLI

```bash
# ros2 service call <service> <тип> <аргументы> — вызов сервиса из CLI
# Аргументы в JSON-формате: {поля_запроса}
# server складывает a и b, возвращает sum
ros2 service call /add_two_ints example_interfaces/srv/AddTwoInts "{a: 5, b: 3}"
# Ожидаемый вывод:
# sum: 8
```

В терминале 1 (server) появляется лог:

```
[INFO] [add_two_ints_server]: 5 + 3 = 8
```

**Что сказать**: «Мы вызвали service из командной строки. Server получил запрос, сложил числа и вернул ответ — `sum: 8`. Это точка-точка: один client, один server, один ответ.»

### 5. Еще один вызов — другие числа

```bash
# Каждый вызов — независимый запрос-ответ. Server не хранит состояние между вызовами
ros2 service call /add_two_ints example_interfaces/srv/AddTwoInts "{a: 100, b: 200}"
# sum: 300
```

**Что сказать**: «Service обрабатывает каждый запрос независимо. Результат зависит от аргументов.»

### 6. Вызов service до запуска server (демонстрация ошибки)

Остановить server (`Ctrl+C` в терминале 1). Вызвать service:

```bash
# Без запущенного server вызов падает — в отличие от topic, где publisher может работать без subscriber
ros2 service call /add_two_ints example_interfaces/srv/AddTwoInts "{a: 5, b: 3}"
# Ожидаемый вывод: service not available
```

**Что сказать**: «Если server не запущен — вызов падает. Это главное отличие от topic: publisher может работать без subscriber, но service client не может вызвать service без server. Поэтому в коде client всегда есть `wait_for_service()`.»

Снова запустить server:

```bash
ros2 run service_demo server &
```

### 7. Сравнение topic и service

Запустить параллельно publisher из topic-демо (если есть):

```bash
# Терминал 3: topic — поток сообщений (непрерывно, без запроса)
ros2 topic echo /chatter
# Терминал 4: service — запрос-ответ (вызвали → получили ответ → связь завершена)
ros2 service call /add_two_ints example_interfaces/srv/AddTwoInts "{a: 7, b: 2}"
```

**Что сказать**: «Смотрите: слева topic — данные идут непрерывно, без запроса. Справа service — вызвали, получили ответ. Это два разных механизма для разных задач. Topic — для потоков (`/scan`, `/cmd_vel`). Service — для команд с подтверждением (`/emergency_stop`, диагностика).»

---

## Что сказать (ключевые фразы)

- «Service — это запрос-ответ. Не поток. Не непрерывно. Вызвали — получили ответ — связь завершена.»
- «`ros2 service call` позволяет вызвать любой service в системе прямо из терминала. Без написания кода client.»
- «Server не публикует данные заранее. Он ждет запроса. Это экономит ресурсы для операций, которые нужны редко.»
- «Если server не запущен — вызов service падает. В коде client всегда добавляйте `wait_for_service()` для безопасного ожидания.»
- «В роботе service используется для команд: emergency stop, сброс ошибки моторов, включение датчика. Все это — не потоки, а разовые запросы с подтверждением.»

## Ожидаемый результат

- `ros2 service list` показывает `/add_two_ints`
- `ros2 service type /add_two_ints` → `example_interfaces/srv/AddTwoInts`
- `ros2 service call ... "{a: 5, b: 3}"` → `sum: 8`
- Server в логах показывает: `5 + 3 = 8`
- Вызов без server → ошибка «service not available»

## Типичные проблемы

| Симптом | Причина | Исправление |
| --- | --- | --- |
| `ros2 service call` — service not available | Server не запущен | Запустить `ros2 run service_demo server` |
| Service виден, но не отвечает | Server забыл `spin()` | Проверить `rclpy.spin(node)` в коде |
| `ros2 service call` — wrong type | Неправильно указан тип | `example_interfaces/srv/AddTwoInts` |
| Пустой ответ | Неправильные имена полей в запросе | Поля: `a`, `b`, `sum` (строчные) |
| `ros2 service list` не показывает service | Пакет не собран или не активирован | `colcon build && source install/setup.bash` |

## План Б

Если контейнер не позволяет запустить два терминала:

1. Использовать `&` для запуска server в фоне: `ros2 run service_demo server &`
2. Показать скриншоты каждого шага с выделением ключевого вывода.
3. Объяснить сравнение topic и service на схеме:
   ```
   Topic:    publisher ──→ [поток] ──→ subscriber
   Service:  client ──→ request ──→ server ──→ response
   ```

## Ссылки на материалы курса

- [Services — статья базы знаний](../2_knowledge/services.md)
- [Практика 04: Service Server и Client](../2_practice/04_service.md)
- [Topics — демонстрация](demo2_topics.md) — сравнение с topic

## Связь с роботом

В архитектуре робота TIAGo services используются для команд, требующих подтверждения:

```bash
# В контейнере робота:
ros2 service list | grep emergency
# /emergency_stop

ros2 service type /emergency_stop
# std_srvs/srv/Trigger

ros2 service call /emergency_stop std_srvs/srv/Trigger
# success: True
# message: 'Emergency stop activated'
```

Тот же принцип: вызвали из CLI — получили подтверждение. Service-команды проходят через safety layer перед выполнением.