#!/usr/bin/env bash
# Clones external ROS2 packages and applies patches for TIAGo workspace
set -e

WS_SRC="$1"
if [ -z "$WS_SRC" ]; then
    echo "Usage: $0 <workspace_src_dir>"
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# ---- moveit_ros_control_interface ----
# Not available as deb for Humble, built from moveit2 monorepo source
if [ ! -d "$WS_SRC/moveit_ros_control_interface" ]; then
    echo "--- Cloning moveit_ros_control_interface (sparse checkout from moveit2) ---"
    TMPDIR=$(mktemp -d)
    cd "$TMPDIR"
    git init -q
    git remote add origin https://github.com/moveit/moveit2.git
    git config core.sparseCheckout true
    echo "moveit_plugins/moveit_ros_control_interface/*" > .git/info/sparse-checkout
    git pull --depth 1 origin humble -q 2>&1
    cp -r moveit_plugins/moveit_ros_control_interface "$WS_SRC/"
    cd /
    rm -rf "$TMPDIR"
    echo "--- moveit_ros_control_interface cloned successfully ---"
else
    echo "--- moveit_ros_control_interface already exists, skipping ---"
fi

# ---- Patches for PAL Robotics launch files ----
# diagnostic_aggregator is ROS1-only, not available in ROS2 Humble
for LAUNCH_FILE in \
    "$WS_SRC/tiago_robot/tiago_bringup/launch/twist_mux.launch.py" \
    "$WS_SRC/omni_base_robot/omni_base_bringup/launch/twist_mux.launch.py" \
    "$WS_SRC/pmb2_robot/pmb2_bringup/launch/twist_mux.launch.py"; do
    if [ -f "$LAUNCH_FILE" ] && ! grep -q "diagnostic_aggregator.*not available" "$LAUNCH_FILE"; then
        echo "--- Patching $LAUNCH_FILE (disable diagnostic_aggregator) ---"
        python3 "$SCRIPT_DIR/patch_twist_mux.py" "$LAUNCH_FILE"
    fi
done
