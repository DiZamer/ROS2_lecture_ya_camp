#!/usr/bin/env bash
# Start virtual display for headless GUI access via VNC/noVNC
# This allows Gazebo and RViz to render without a physical X11 display.
#
# Usage:
#   start_gui.sh                    — one display (:99, VNC 5900, Web 6080)
#   start_gui.sh --displays N       — N displays (:99.., VNC 5900.., Web 6080..)

# Parse arguments
NUM_DISPLAYS=1
while [ $# -gt 0 ]; do
    case "$1" in
        --displays)
            NUM_DISPLAYS="$2"
            shift 2
            ;;
        *)
            echo "Usage: $0 [--displays N]"
            exit 1
            ;;
    esac
done

# Validate
if ! [[ "$NUM_DISPLAYS" =~ ^[1-9][0-9]*$ ]]; then
    echo "Error: --displays must be a positive integer"
    exit 1
fi

ALL_PIDS=""

# Create fluxbox config once (shared by all displays)
setup_fluxbox_config() {
    mkdir -p ~/.fluxbox
    cat > ~/.fluxbox/menu << 'FBMENU'
[begin] (TIAGo)
  [exec] (Terminal) { x-terminal-emulator }
  [exec] (RViz2) { rviz2 }
  [exec] (Gazebo) { gzclient }
  [separator]
  [exec] (Reload config) { fluxbox-remote reconfigure }
  [exec] (Restart fluxbox) { fluxbox-remote restart }
  [exec] (Exit) { fluxbox-remote exit }
[end]
FBMENU
    if ! grep -q "toolbar.onTop" ~/.fluxbox/init 2>/dev/null; then
        echo "session.screen0.toolbar.onTop: false" >> ~/.fluxbox/init
        echo "session.screen0.toolbar.visible: true" >> ~/.fluxbox/init
    fi
}

setup_fluxbox_config

# Deploy custom noVNC index page if available
if [ -f /workspaces/TIAgo_humble/ros2_ws/novnc_index.html ]; then
    sudo cp /workspaces/TIAgo_humble/ros2_ws/novnc_index.html /usr/share/novnc/index.html
fi

start_display() {
    local i="$1"
    local dpy_num="$((99 + i))"
    local vnc_port="$((5900 + i))"
    local web_port="$((6080 + i))"

    # ── Xvfb ──
    if ! xdpyinfo -display ":$dpy_num" >/dev/null 2>&1; then
        echo "[$i] Starting Xvfb on display :$dpy_num ..."
        Xvfb ":$dpy_num" -screen 0 1920x1080x24 -nolisten tcp &
        ALL_PIDS="$ALL_PIDS $!"
        sleep 0.5
    fi

    # ── x11vnc ──
    echo "[$i] Starting x11vnc on port $vnc_port ..."
    x11vnc -display ":$dpy_num" -forever -nopw -quiet -rfbport "$vnc_port" &
    ALL_PIDS="$ALL_PIDS $!"

    # ── noVNC web proxy ──
    echo "[$i] Starting noVNC on port $web_port (http://localhost:$web_port) ..."
    websockify --web /usr/share/novnc "$web_port" localhost:"$vnc_port" &
    ALL_PIDS="$ALL_PIDS $!"

    # ── fluxbox window manager ──
    DISPLAY=":$dpy_num" fluxbox 2>/dev/null &
    ALL_PIDS="$ALL_PIDS $!"
}

# Start all displays
for i in $(seq 0 $((NUM_DISPLAYS - 1))); do
    start_display "$i"
done

# Wait a moment for everything to settle
sleep 0.5

echo ""
echo "GUI server ready — $NUM_DISPLAYS display(s)"
for i in $(seq 0 $((NUM_DISPLAYS - 1))); do
    echo "  [$i] DISPLAY=:$((99 + i))  Web: http://localhost:$((6080 + i))"
done
echo ""
echo "Press Ctrl+C to stop all"

# Trap Ctrl+C and clean up
cleanup() {
    kill $ALL_PIDS 2>/dev/null
    wait
}
trap cleanup INT TERM

# Wait for any process to exit
wait
