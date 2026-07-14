# TIAGo ROS2 Simulation Environment (DevContainer)

<p align="center">
  <img src="https://www.pal-robotics.com/wp-content/uploads/2018/06/tiago_platform.jpg" alt="TIAGo Robot" width="400"/>
</p>

Этот репозиторий содержит среду для симуляции популярного робота **TIAGo** от компании PAL Robotics. Проект упакован в `devcontainer` и готов к запуску на Ubuntu, Windows и macOS.

Среда предназначена для образовательных целей и быстрого начала работы с ROS2 Humble и симуляцией TIAGo.

---

## 📖 Оглавление

- [📖 Оглавление](#-оглавление)
- [Краткое описание проекта TIAGo](#краткое-описание-проекта-tiago)
- [Что из себя представляет модель робота и почему он используется как образовательный](#что-из-себя-представляет-модель-робота-и-почему-он-используется-как-образовательный)
  - [🔹 **Навигация (Navigation)**](#-навигация-navigation)
  - [🔹 **Манипуляция (Manipulation)**](#-манипуляция-manipulation)
  - [🔹 **Восприятие (Perception)**](#-восприятие-perception)
  - [🔹 **Интеграция систем**](#-интеграция-систем)
  - [🔹 **Междисциплинарность**](#-междисциплинарность)
- [Все источники и полезные ссылки](#все-источники-и-полезные-ссылки)
  - [📚 Основная документация и учебные материалы](#-основная-документация-и-учебные-материалы)
  - [🛠️ Инструменты и альтернативные симуляторы](#️-инструменты-и-альтернативные-симуляторы)
  - [🚀 Расширенные модификации TIAGo](#-расширенные-модификации-tiago)
  - [🎥 Видео и демонстрации](#-видео-и-демонстрации)
  - [🔗 Дополнительно](#-дополнительно)
- [Установка и настройка](#установка-и-настройка)
  - [📦 Использование DevContainer](#-использование-devcontainer)
  - [🐳 Использование Docker напрямую](#-использование-docker-напрямую)
- [Как настроить GUI-вывод приложения в вашей ОС](#как-настроить-gui-вывод-приложения-в-вашей-ос)
  - [🐧 Настройка на Linux (Ubuntu)](#-настройка-на-linux-ubuntu)
  - [🪟 Настройка на Windows](#-настройка-на-windows)
  - [🍏 Настройка на macOS](#-настройка-на-macos)
- [Быстрый старт](#быстрый-старт)
  - [Запуск симуляции в Gazebo](#запуск-симуляции-в-gazebo)
  - [Запуск навигации](#запуск-навигации)
  - [Запуск манипуляции через MoveIt](#запуск-манипуляции-через-moveit)
  - [Запуск всех туториалов](#запуск-всех-туториалов)
- [🧪 Примеры лабораторных работ для студентов](#-примеры-лабораторных-работ-для-студентов)
- [📝 Лицензия](#-лицензия)
- [🤝 Вклад в проект](#-вклад-в-проект)
- [📧 Контакты](#-контакты)

---

## Краткое описание проекта TIAGo

**TIAGo (Take It And Go)** — это полнофункциональный мобильный манипулятор, разработанный компанией PAL Robotics для исследований и образования. Робот сочетает в себе:

- Мобильную платформу с дифференциальным или омниколесным приводом
- 7-степенной манипулятор с захватом
- Стереокамеры и RGB-D сенсоры (например, Intel RealSense)
- 2D/3D лидары для навигации и построения карт
- Встроенный компьютер с ROS2

TIAGo широко используется в университетах и исследовательских центрах благодаря своей открытой архитектуре на базе ROS, модульности и надежности.

---

## Что из себя представляет модель робота и почему он используется как образовательный

TIAGo является идеальной платформой для изучения широкого спектра задач робототехники:

### 🔹 **Навигация (Navigation)**
Изучение алгоритмов автономного перемещения, построения карт (SLAM), планирования маршрутов и избегания препятствий. Студенты могут экспериментировать с различными стратегиями навигации в симулированной среде.

### 🔹 **Манипуляция (Manipulation)**
Планирование траекторий для руки с помощью MoveIt 2, захват объектов, управление в замкнутом контуре и силовое управление. Это позволяет изучать как классические, так и современные подходы к роботизированной манипуляции.

### 🔹 **Восприятие (Perception)**
Обработка данных с камер и лидаров для распознавания объектов, семантической сегментации, отслеживания и взаимодействия с окружающей средой. Студенты могут применять методы компьютерного зрения и машинного обучения.

### 🔹 **Интеграция систем**
Объединение всех вышеперечисленных систем в едином фреймворке, что дает понимание полного цикла разработки роботизированных систем — от восприятия до действия.

### 🔹 **Междисциплинарность**
TIAGo позволяет изучать робототехнику с разных сторон: механика, электроника, программирование, управление, AI и HRI (Human-Robot Interaction).

---

## Все источники и полезные ссылки

Ниже представлена полная таблица всех актуальных источников, разделенная по типам и с указанием применения для студентов.

### 📚 Основная документация и учебные материалы

| № | Источник | Тип | Краткое описание | Применение студентами |
|---|----------|-----|------------------|------------------------|
| 1 | [Официальная страница робота](https://robots.ros.org/tiago/) | Веб-сайт | Общее описание TIAGo, спецификации, области применения | Знакомство с роботом и его возможностями |
| 2 | [TIAGo ROS repo (индекс ROS)](https://index.ros.org/r/tiago_simulation/) | Документация | Главный репозиторий с инструкциями по установке | Настройка рабочего окружения и запуск симуляции |
| 3 | [pal-robotics/tiago_simulation (GitHub)](https://github.com/pal-robotics/tiago_simulation) | Исходный код | Код симуляции для Gazebo, launch-файлы | Изучение архитектуры симулятора |
| 4 | [Официальные туториалы PAL Robotics](https://pal-robotics.github.io/tiago-tutorial/autonomous_navigation/navigation/index.html) | Документация | **Основной учебный материал** по навигации, манипуляции и восприятию | Выполнение лабораторных работ по ROS2 |
| 5 | [Современная документация PAL Simulator](https://docs.pal-robotics.com/sdk/24.09/general/getting-started-simulator.html) | Документация | Актуальное SDK для симулятора | Использование новейших функций |
| 6 | [pal-robotics/tiago_tutorials (GitHub)](https://github.com/pal-robotics/tiago_tutorials) | Исходный код | Учебные материалы и примеры кода | Заимствование готовых решений |
| 7 | [Docker Hub palroboticssl](https://hub.docker.com/r/palroboticssl/tiago_tutorials) | Инструмент | Официальный Docker-образ | Быстрый старт без установки ROS2 |
| 8 | [Wiki ROS - TIAGo Tutorials](https://wiki.ros.org/Robots/TIAGo/Tutorials) | Документация | Классическая вики с туториалами (может быть устаревшей) | Понимание фундаментальных концепций |
| 11 | [Официальная документация PAL Robotics (TIAGo)](https://docs.pal-robotics.com/25.01/tiago.html#tiago-first-steps) | Документация | **Самый актуальный официальный источник** | Единственный источник для официальных процедур |

### 🛠️ Инструменты и альтернативные симуляторы

| № | Источник | Тип | Краткое описание | Применение студентами |
|---|----------|-----|------------------|------------------------|
| 9 | [Gazebo](https://gazebosim.org/home) | Инструмент | Основной симулятор | Изучение возможностей симулятора |
| 10 | [MoveIt 2](https://moveit.ai/) | Инструмент | Фреймворк для планирования движений | Изучение алгоритмов планирования траекторий |
| 13 | [webots_ros2_tiago (ROS Index)](https://index.rosdabbler.com/p/webots_ros2_tiago/) | Инструмент | Симуляция в Webots | Альтернатива Gazebo для Windows/Mac |

### 🚀 Расширенные модификации TIAGo

| № | Источник | Тип | Краткое описание | Применение студентами |
|---|----------|-----|------------------|------------------------|
| 12 | [TIAGo Base AI](http://mirror-ap.wiki.ros.org/Robots(2f)tiago(2d)base(2d)ai.html) | Документация | Модификация с NVIDIA Jetson | Изучение AI-ускорения на роботах |
| 14 | [TIAGo OMNI Base](http://mirror-ap.wiki.ros.org/Robots(2f)TIAGo(2d)OMNI(2d)base.html) | Документация | Омниколесное шасси | Изучение кинематики мобильных роботов |
| 16 | [TIAGo Pro](https://docs.pal-robotics.com/sdk-dev/tiagopro) | Документация | Версия с полным контролем крутящего момента | Изучение силового управления |

### 🎥 Видео и демонстрации

| № | Источник | Тип | Краткое описание | Применение студентами |
|---|----------|-----|------------------|------------------------|
| 17 | **YouTube-канал PAL Robotics** | Видео | Демонстрации TIAGo (компенсация гравитации, обучение с демонстрации и др.) | Визуальное понимание работы робота |

### 🔗 Дополнительно

| № | Источник | Тип | Краткое описание | Применение студентами |
|---|----------|-----|------------------|------------------------|
| 15 | [PAL Developer Center](https://docs.pal-robotics.com/25.01/index.html) | Документация | Центральный портал разработчиков | Общий вход в экосистему PAL |

---

## Установка и настройка

### 📦 Использование DevContainer

Проект использует DevContainer на базе `osrf/ros:humble-desktop`. При первом запуске контейнер собирает все пакеты TIAGo из исходников — это **единоразовый процесс**, занимающий 20-40 минут.

**Для начала работы:**

1. Убедитесь, что у вас установлены:
   - [Docker](https://docs.docker.com/get-docker/)
   - [Visual Studio Code](https://code.visualstudio.com/)
   - Расширение [Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

2. Клонируйте репозиторий (на **хосте**):
   ```bash
   cd <папка-проекта>
   git clone <url-вашего-репозитория>

   ```

3. Откройте папку в VS Code (на **хосте**):
   ```bash
   code .
   ```
   При появлении запроса выберите **"Reopen in Container"**.

4. **Первый запуск (20-40 минут)** — всё происходит автоматически внутри контейнера:
   - `Dockerfile` собирает образ с ROS2 и зависимостями (~1-2 мин)
   - `vcs import` клонирует 18 репозиториев TIAGo из GitHub
   - `fetch_external.sh` клонирует пакеты, недоступные через apt (`moveit_ros_control_interface`)
   - `rosdep install` устанавливает недостающие deb-пакеты
   - `colcon build` собирает все пакеты TIAGo из исходников (~15-35 мин)

5. **Все последующие запуски — мгновенно.**

6. После сборки откройте два терминала внутри VS Code:

   **Терминал 1 (в контейнере)** — запустить виртуальный дисплей:
   ```bash
   start_gui.sh
   ```
   Откройте в браузере на **хосте**: [http://localhost:6080](http://localhost:6080)

   **Терминал 2 (в контейнере)** — запустить симуляцию:
   ```bash
   ros2 launch tiago_gazebo tiago_gazebo.launch.py is_public_sim:=True
   ```
   Gazebo и RViz появятся в браузере на странице noVNC.

### 🐳 Использование Docker напрямую
Если вы не используете VS Code, можно собрать и запустить образ вручную.

Сборка образа (на **хосте**):
```bash
cd .devcontainer
docker build -t tiago_humble -f Dockerfile ..
```

Запуск контейнера (на **хосте**):
```bash
docker run -it --rm \
  --name tiago_dev \
  --privileged \
  --shm-size=1g \
  -e DISPLAY=:99 \
  -e QT_X11_NO_MITSHM=1 \
  -e LIBGL_ALWAYS_SOFTWARE=1 \
  -e ROS_LOCALHOST_ONLY=1 \
  -p 6080:6080 \
  -v $(pwd)/..:/workspaces/TIAgo_humble \
  tiago_humble \
  bash
```

После входа в контейнер выполните по порядку (в **контейнере**):
```bash
source /opt/ros/humble/setup.bash
cd /workspaces/TIAgo_humble/ros2_ws
vcs import src < tiago.repos
bash fetch_external.sh src
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install
source install/setup.bash
```
Теперь GUI и симуляция — как в DevContainer (см. шаг 6 выше).

## Работа с GUI (Gazebo, RViz)

Контейнер использует **виртуальный дисплей (Xvfb)** с доступом через VNC/браузер. Это работает на всех ОС без установки X11-сервера на хосте.

В `devcontainer.json` заложены 5 вариантов настройки — по умолчанию активен **Вариант 1 (VNC/браузер)**. Чтобы переключиться на прямой X11, откройте `.devcontainer/devcontainer.json` и следуйте инструкции в комментариях.

> **Файлы конфигурации:**
> - `devcontainer.json` — текущая версия (та же, что и на момент разработки)
> - `devcontainer_prod.json` — production-версия со всеми 5 вариантами (VNC по умолчанию)
> - `devcontainer_dev.json` — пример с активным Вариантом 5 (Ubuntu X11 + NVIDIA GPU)

---

### Виртуальный дисплей (через браузер) — по умолчанию

Подходит для **всех ОС**. Не требует X11 на хосте.

**Одна вкладка** — все окна (Gazebo, RViz) на одном экране:

```bash
# Терминал 1 (в контейнере): запустить виртуальный дисплей
start_gui.sh

# Браузер на хосте: http://localhost:6080

# Терминал 2 (в контейнере): запустить приложения
ros2 launch tiago_gazebo tiago_gazebo.launch.py is_public_sim:=True
```

**Две вкладки** — Gazebo и RViz2 на отдельных экранах:

```bash
# Терминал 1
start_gui.sh --displays 2
```

| Дисплей | DISPLAY | VNC | Web | Для |
|---------|---------|-----|-----|-----|
| 0 | `:99` | 5900 | **6080** | Gazebo |
| 1 | `:100` | 5901 | **6081** | RViz2 |

```bash
# Терминал 2 — Gazebo на дисплее 0
DISPLAY=:99 ros2 launch tiago_gazebo tiago_gazebo.launch.py is_public_sim:=True

# Терминал 3 — RViz2 на дисплее 1
DISPLAY=:100 rviz2
```

Любое количество дисплеев: `--displays 3` → порты 6080, 6081, 6082 и т.д.

> **Примечание:** каждый Xvfb потребляет ~60 MB видеопамяти.

Если порт 6080 занят:
```bash
NOVNC_PORT=6081 start_gui.sh
# http://localhost:6081
```

**Как это работает:**
1. **Xvfb** — виртуальный X-сервер (дисплей `:99` / `:100` / ..., 1920x1080)
2. **x11vnc** — VNC-сервер на порту 5900 / 5901 / ...
3. **websockify** — WebSocket-proxy для noVNC на порту 6080 / 6081 / ...
4. **Fluxbox** — оконный менеджтор (позволяет перемещать окна, сворачивать)

Через noVNC в браузере вы видите виртуальный экран контейнера. Все GUI-приложения (Gazebo, RViz) рендерятся на этом экране.

---

### Альтернатива: VNC Viewer (меньше RAM, выше FPS)

Вместо браузера можно подключиться напрямую к x11vnc через VNC-клиент.

**Плюсы:**
- Нет прослойки браузер + noVNC + websockify — экономия 200-500 MB RAM
- Нативный VNC-протокол — выше частота кадров, меньше задержка
- Те же порты, что у noVNC: 5900 (дисплей 0), 5901 (дисплей 1) и т.д.

**Бесплатные кроссплатформенные VNC-клиенты:**

| Клиент | Сайт | ОС |
|--------|------|----|
| TigerVNC | https://tigervnc.org | Linux, Windows, macOS |
| RealVNC Viewer | https://www.realvnc.com/en/connect/download/viewer/ | Linux, Windows, macOS |

**Подключение:** `localhost:5900` (или `localhost:5901` для второго дисплея).

`start_gui.sh` продолжает работать как обычно — VNC-сервер уже запущен, можно подключаться и через браузер, и через VNC Viewer одновременно.

---

### Прямой вывод на хост (без VNC)

Окна Gazebo и RViz появляются прямо на хосте, как обычные приложения. **Быстрее и удобнее**, но требует X11-сервера на хосте и переключения варианта в `devcontainer.json`.

**Как переключиться:**
1. Откройте `.devcontainer/devcontainer.json`
2. Закомментируйте блок `containerEnv` + `runArgs` + `forwardPorts` **Варианта 1**
3. Раскомментируйте блок `containerEnv` + `runArgs` + `forwardPorts` для своей ОС
4. Выполните **Rebuild Container**

#### Ubuntu (X11) — Docker Desktop или native Docker Engine

Проверено на Ubuntu 24.04 + Docker Desktop 29.6.0. Работает и с native Docker Engine.

1. Проверьте номер дисплея на **хосте**:
   ```bash
   echo $DISPLAY
   # :1 — если Docker Desktop (он занимает :0 под свой X-сервер)
   # :0 — если native Docker Engine или нет конфликта дисплеев
   ```

2. Разрешите контейнеру подключаться к X-серверу (**хост**, один раз):
   ```bash
   xhost +local:docker
   ```

3. Откройте `.devcontainer/devcontainer.json`, раскомментируйте **Вариант 2**.
   Если `echo $DISPLAY` показал не `:1` — исправьте значение `DISPLAY` в `containerEnv`.

4. **Rebuild Container**. После пересборки проверьте X11:
   ```bash
   gedit
   # Должно открыться окно gedit на хосте
   ```

5. Запуск симуляции — без `start_gui.sh`:
   ```bash
   ros2 launch tiago_gazebo tiago_gazebo.launch.py is_public_sim:=True
   # Gazebo и RViz появляются как обычные окна на хосте
   ```

**Типичные ошибки:**
- `cannot open display :1` → забыли `xhost +local:docker`
- `cannot open display :0` → Docker Desktop, нужно `DISPLAY=:1`

#### Ubuntu (Wayland)

Gazebo и RViz используют X11 API и автоматически работают через **XWayland** —
встроенный X11-совместимый слой, присутствующий в каждом Wayland-окружении.
Поэтому настройка полностью идентична разделу «Ubuntu (X11)» — выполните
те же шаги с `xhost +local:docker`, проверкой `echo $DISPLAY`
и раскомментированием Варианта 2.

Нативные Wayland-приложения из контейнера на хост не пробросить, но для
Gazebo/RViz/Rviz2 это не требуется — все они используют X11.

#### Windows (VcXsrv)

1. Скачайте и установите [VcXsrv](https://sourceforge.net/projects/vcxsrv/) (бесплатно, open source)
2. Запустите **XLaunch**:
   - `Multiple windows`
   - `Display number: -1`
   - `Start no client`
   - Отметьте `Disable access control`
3. Сохраните конфигурацию для быстрого запуска в следующий раз

#### macOS (XQuartz)

1. Скачайте и установите [XQuartz](https://www.xquartz.org/) (бесплатно)
2. XQuartz → **Preferences → Security** → отметьте `Allow connections from network clients`
3. Перезапустите XQuartz
4. В терминале хоста (один раз):
```bash
xhost +localhost
```

#### Ubuntu + NVIDIA GPU (Вариант 5)

Для владельцев NVIDIA-видеокарт — аппаратный рендеринг Gazebo (60 FPS вместо 5).

**Требования:**
- Native Docker Engine (`docker-ce`), не Docker Desktop
- NVIDIA-драйвер и `nvidia-container-toolkit` на хосте

**Настройка хоста (однократно):**
```bash
# Установить nvidia-container-toolkit
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | \
  sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
sudo apt update && sudo apt install -y nvidia-container-toolkit
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker

# Переключиться на native Docker Engine
docker context use default

# Проверить GPU-проброс
docker run --rm --gpus all nvidia/cuda:12.8.0-runtime-ubuntu22.04 nvidia-smi
```

**В devcontainer.json:**
1. Закомментируйте блок **Варианта 1**
2. Раскомментируйте блок **Варианта 5**
3. Выполните **Rebuild Container**

После сборки — прямой X11 на `DISPLAY=:1`, Gazebo рендерится на GPU.
```bash
xhost +local:docker
ros2 launch tiago_gazebo tiago_gazebo.launch.py is_public_sim:=True
```

## Быстрый старт
После того как вы настроили окружение, проверьте его работу. Все команды выполняются в **контейнере**:

### Запуск симуляции в Gazebo
Перед запуском — убедитесь, что `start_gui.sh` запущен в соседнем терминале (если вы используете первый вариант запуска).
```bash
ros2 launch tiago_gazebo tiago_gazebo.launch.py is_public_sim:=True
```

### Запуск навигации
```bash
ros2 launch tiago_navigation nav2_bringup.launch.py
```

### Запуск манипуляции через MoveIt
```bash
ros2 launch tiago_moveit moveit.launch.py
```

### Запуск всех туториалов
```bash
ros2 launch tiago_tutorials <название_туториала>.launch.py
```
Все туториалы доступны в репозитории tiago_tutorials и описаны в официальной документации.

### ⚠️ `diagnostic_aggregator` — ROS1 пакет, отсутствующий в ROS2

Пакет `diagnostic_aggregator` (из стека `ros-perception/diagnostics`) **не был портирован в ROS2 Humble**. PAL Robotics использует его во внутренних launch-файлах:

- `tiago_bringup/launch/twist_mux.launch.py` — закомментирован
- `omni_base_bringup/launch/twist_mux.launch.py` — закомментирован
- `pmb2_bringup/launch/twist_mux.launch.py` — закомментирован

**Назначение:** `diagnostic_aggregator::add_analyzer` загружает YAML-конфиг с иерархией анализаторов (`AnalyzerGroup`, `GenericAnalyzer`), группирует diagnostic статусы от компонентов (джойстик, twist_mux) и публикует агрегированный результат в `/diagnostics`.

**Почему не критичен для симуляции:** twist_mux продолжает работать без aggregator'а — теряется только визуализация диагностики в RViz (вкладка Diagnostics). На управление колёсами не влияет.

Если потребуется полноценная реализация:
1. Создать пакет `diagnostic_aggregator` (ROS2-совместимый), реализующий `add_analyzer`, который загружает analyzers из YAML и публикует в `/diagnostics`.
2. Раскомментировать узлы в трёх launch-файлах выше.
3. Проверить совместимость формата `twist_mux_analyzers.yaml` с новым API.

### ⚠️ `moveit_ros_control_interface` — не доступен через apt для Humble

Пакет `moveit_ros_control_interface` (ROS2-интеграция MoveIt с `ros2_control`) **не выпущен в виде deb-пакета для ROS2 Humble**. Он автоматически собирается из исходников `moveit2` (sparse checkout) скриптом `ros2_ws/fetch_external.sh` при первом запуске контейнера.

**Где используется:** `tiago_moveit_config/config/controllers/*.yaml` — все конфиги контроллеров.

**Статус:** работает — `Ros2ControlManager` загружается, все контроллеры (arm, torso, head, gripper, ft_sensor, mobile_base) конфигурируются и активируются.

## 🧪 Примеры лабораторных работ для студентов
На основе TIAGo можно построить следующие учебные задания:

| Тема | Описание | Используемые источники |
|------|----------|------------------------|
| Введение в ROS2 | Создание узлов, топиков, сервисов, действий | №4, №6 |
| Навигация | Построение карты, планирование маршрута, избегание препятствий | №4, №5, №11 |
| Манипуляция | Планирование траекторий, захват объектов, Pick-and-Place | №4, №6, №10 |
| Восприятие | Распознавание объектов, семантическая сегментация | №4, №12 |
| Интеграция | Объединение навигации и манипуляции в комплексном сценарии | №4, №5, №11 |

## 📝 Лицензия
Этот проект использует ПО PAL Robotics, распространяемое под лицензией Apache 2.0. Подробности см. в официальной документации.

## 🤝 Вклад в проект
Если вы нашли ошибку или хотите дополнить документацию, создайте Issue или Pull Request в этом репозитории.

## 📧 Контакты
Официальная поддержка PAL Robotics: support@pal-robotics.com

Сообщество ROS: answers.ros.org

После выполнения всех шагов вы окажетесь в готовом окружении с TIAGo и сможете начать использовать робота в своих проектах и демонстрациях! 🚀
