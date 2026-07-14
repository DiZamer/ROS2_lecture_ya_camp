#!/usr/bin/env python3
"""
Patches twist_mux.launch.py to disable diagnostic_aggregator node.
diagnostic_aggregator is a ROS1 package not available in ROS2 Humble.
"""
import sys

if len(sys.argv) < 2:
    print("Usage: patch_twist_mux.py <launch_file_path>")
    sys.exit(1)

path = sys.argv[1]

with open(path, 'r') as f:
    content = f.read()

old = '''    twist_mux_analyzer = Node(
        package='diagnostic_aggregator',
        executable='add_analyzer',
        namespace='twist_mux',
        output='screen',
        emulate_tty=True,
        parameters=[
            os.path.join(pkg_dir, 'config', 'twist_mux', 'twist_mux_analyzers.yaml')
        ],
    )
    launch_description.add_action(twist_mux_analyzer)'''

new = '''    # NOTE: diagnostic_aggregator is not available in ROS2 Humble (ROS1-only package).
    # The twist_mux_analyzer node is disabled to avoid launch failure.
    # See README (Known Issues) for details.
    # twist_mux_analyzer = Node(
    #     package='diagnostic_aggregator',
    #     executable='add_analyzer',
    #     namespace='twist_mux',
    #     output='screen',
    #     emulate_tty=True,
    #     parameters=[
    #         os.path.join(pkg_dir, 'config', 'twist_mux', 'twist_mux_analyzers.yaml')
    #     ],
    # )
    # launch_description.add_action(twist_mux_analyzer)'''

if old in content:
    content = content.replace(old, new)
    with open(path, 'w') as f:
        f.write(content)
    print("Patch applied successfully")
else:
    print("Patch pattern not found — may already be applied or file structure changed")
