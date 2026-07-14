FROM osrf/ros:humble-desktop

ENV DEBIAN_FRONTEND=noninteractive
ENV PIP_NO_CACHE_DIR=1

# Add ubuntu user with same UID and GID as your host system, if it doesn't already exist
# Since Ubuntu 24.04, a non-root user is created by default with the name vscode and UID=1000
ARG USERNAME=ubuntu
ARG USER_UID=1000
ARG USER_GID=$USER_UID
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    clang-format \
    gdb \
    gedit \
    gazebo \
    ros-${ROS_DISTRO}-gazebo-ros-pkgs \
    ros-${ROS_DISTRO}-turtlesim \
    sudo \
    git \
    pkg-config \
    usbutils \
    udev \
    python3-pip \
    python3-serial \
    python3-venv \
    python3-opencv \
    python3-colcon-common-extensions \
    python3-rosdep \
    python3-vcstool \
    python3-setuptools \
    python3-wheel \
    tree \
    curl \
    ca-certificates \
    lsb-release \
    gnupg \
    stockfish \
    && rm -rf /var/lib/apt/lists/* && \
    if ! id -u $USER_UID >/dev/null 2>&1; then \
        groupadd --gid $USER_GID $USERNAME && \
        useradd -s /bin/bash --uid $USER_UID --gid $USER_GID -m $USERNAME; \
    fi && \
    echo "$USERNAME ALL=(root) NOPASSWD:ALL" > /etc/sudoers.d/$USERNAME && \
    chmod 0440 /etc/sudoers.d/$USERNAME && \
    usermod --append --groups video,dialout,plugdev $USERNAME

# Switch from root to user
USER $USERNAME

# Source the ROS setup file
RUN echo "source /opt/ros/${ROS_DISTRO}/setup.bash" >> ~/.bashrc

# --- Install TIAGo dependencies (MoveIt2, Nav2, ros2_control, etc.)
RUN sudo apt-get update && sudo apt-get install -y --no-install-recommends \
    ros-humble-moveit \
    ros-humble-navigation2 \
    ros-humble-nav2-bringup \
    ros-humble-slam-toolbox \
    ros-humble-robot-localization \
    ros-humble-ros2-control \
    ros-humble-ros2-controllers \
    ros-humble-gazebo-ros2-control \
    ros-humble-xacro \
    ros-humble-joint-state-publisher-gui \
    ros-humble-twist-mux \
    ros-humble-sophus \
    ros-humble-robot-state-publisher \
    ros-humble-tf-transformations \
    ros-humble-joint-trajectory-controller \
    ros-humble-forward-command-controller \
    ros-humble-velocity-controllers \
    ros-humble-position-controllers \
    ros-humble-effort-controllers \
    ros-humble-imu-sensor-broadcaster \
    ros-humble-force-torque-sensor-broadcaster \
    ros-humble-backward-ros \
    && sudo rm -rf /var/lib/apt/lists/*

# Install X Virtual Framebuffer for headless GUI (works with Docker Desktop)
RUN sudo apt-get update && sudo apt-get install -y --no-install-recommends \
    xvfb \
    x11vnc \
    novnc \
    python3-websockify \
    net-tools \
    fluxbox \
    && sudo rm -rf /var/lib/apt/lists/*

# Copy VNC startup script and noVNC index page
COPY ros2_ws/start_gui.sh /usr/local/bin/start_gui.sh
COPY ros2_ws/novnc_index.html /usr/share/novnc/index.html
RUN sudo chmod +x /usr/local/bin/start_gui.sh

RUN echo 'source /usr/share/gazebo/setup.sh' >> ~/.bashrc