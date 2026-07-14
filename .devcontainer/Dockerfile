FROM osrf/ros:jazzy-desktop

ENV DEBIAN_FRONTEND=noninteractive
ENV PIP_NO_CACHE_DIR=1

ARG USERNAME=ubuntu
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    gdb \
    git \
    curl \
    ca-certificates \
    gnupg \
    lsb-release \
    tree \
    sudo \
    python3-pip \
    python3-colcon-common-extensions \
    python3-rosdep \
    python3-vcstool \
    python3-setuptools \
    python3-wheel \
    python3-venv \
    && rm -rf /var/lib/apt/lists/* \
    && if ! id -u $USER_UID >/dev/null 2>&1; then \
        groupadd --gid $USER_GID $USERNAME && \
        useradd -s /bin/bash --uid $USER_UID --gid $USER_GID -m $USERNAME; \
    fi \
    && echo "$USERNAME ALL=(root) NOPASSWD:ALL" > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME \
    && usermod --append --groups video,dialout,plugdev $USERNAME

USER $USERNAME

RUN echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc