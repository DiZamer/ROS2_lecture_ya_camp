# QoS-профили TIAGo — настройки доставки сообщений

Каждый топик в TIAGo использует свои настройки QoS (Quality of Service). Неправильный QoS приводит к тому, что publisher и subscriber не соединяются, или данные теряются там, где потеря недопустима.

> Связь с теорией: [`2_knowledge/qos.md`](../../2_knowledge/qos.md) — reliability, durability, history, depth.

---

## QoS-профили ключевых топиков TIAGo

| Топик | Reliability | Durability | Depth | Зачем |
|---|---|---|---|---|
| `/scan`, `/scan_raw` | `BEST_EFFORT` | `VOLATILE` | 10 | Лазер 10 Гц — потеря кадра не страшна |
| `/head_front_camera/rgb/image_raw` | `BEST_EFFORT` | `VOLATILE` | 5 | Видеопоток — важна скорость, не надёжность |
| `/cmd_vel` | `RELIABLE` | `VOLATILE` | 10 | Команда скорости — нельзя терять |
| `/odom` | `RELIABLE` | `VOLATILE` | 10 | Одометрия — важна каждая публикация |
| `/joint_states` | `RELIABLE` | `VOLATILE` | 10 | Состояние суставов — нельзя терять |
| `/map` | `RELIABLE` | `TRANSIENT_LOCAL` | 1 | Карта — новый подписчик должен получить её сразу |
| `/detections` | `RELIABLE` | `VOLATILE` | 10 | Детекции — нельзя терять факт обнаружения |
| `/tf`, `/tf_static` | `RELIABLE` | `VOLATILE` | 100 | Transform-ы — высокая частота, большая очередь |

---

## Команды проверки

```bash
# Посмотреть QoS топика
ros2 topic info /scan --verbose

# Подписаться с нестандартным QoS
ros2 topic echo /scan --qos-reliability best_effort

# Проверить, соединяются ли pub и sub
ros2 topic info /cmd_vel --verbose
# Смотреть: Publisher count и Subscription count
```

---

## Типичные ошибки

| Ошибка | Симптом | Исправление |
|---|---|---|
| Pub и sub не соединяются | `ros2 topic info` показывает 0 subscribers, хотя узел подписан | Проверить совместимость QoS: reliability, durability должны совпадать |
| Новый подписчик не получает карту | `/map` пустой после подписки | Использовать `TRANSIENT_LOCAL` durability |
| Потеря команд скорости | Робот игнорирует часть `/cmd_vel` | Использовать `RELIABLE` |
| Лаги видео | Задержка `/image_raw` | Использовать `BEST_EFFORT` + малый depth |

---

## Расширяющий материал

### `/scan_raw` vs `/scan` — raw vs filtered

TIAGo публикует два лазерных топика:
- `/scan_raw` — сырые данные от Gazebo-плагина (BEST_EFFORT, depth 10)
- `/scan` — фильтрованные данные (после laser_filters, RELIABLE)

Nav2 подписывается на `/scan_raw` для costmaps и `/scan` для AMCL-локализации. Фильтрация может удалять «шумные» точки, что важно для стабильной локализации, но может скрывать мелкие препятствия на costmap.

### RELIABLE для E-stop и команд безопасности

Топик `/emergency_stop` использует RELIABLE с depth 1 — потеря даже одной команды E-stop недопустима. Это пример, когда надёжность абсолютно приоритетнее скорости.

### BEST_EFFORT для video stream

Видеопоток с камеры TIAGo публикуется с BEST_EFFORT. Если бы он был RELIABLE — при потере пакета DDS ждал бы переотправки, создавая задержку. Для видео лучше потерять кадр, чем показать старый.

---

## Ссылки

- [About QoS (Jazzy)](https://docs.ros.org/en/jazzy/Concepts/Intermediate/About-Quality-of-Service-Settings.html)
- [QoS Compatibility](https://docs.ros.org/en/jazzy/Concepts/Intermediate/About-QoS-Compatibility.html)
