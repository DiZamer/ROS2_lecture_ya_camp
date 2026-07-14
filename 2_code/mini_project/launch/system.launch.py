from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    config = PathJoinSubstitution([
        FindPackageShare('mini_project'),
        'config', 'system_params.yaml'
    ])

    threshold_arg = DeclareLaunchArgument(
        'threshold', default_value='7.0',
        description='Alarm threshold for processor_node'
    )

    sensor = Node(
        package='mini_project',
        executable='sensor_node',
        name='sensor_node',
        parameters=[config]
    )

    processor = Node(
        package='mini_project',
        executable='processor_node',
        name='processor_node',
        parameters=[config, {
            'threshold': LaunchConfiguration('threshold')
        }]
    )

    alarm = Node(
        package='mini_project',
        executable='alarm_server',
        name='alarm_server'
    )

    task = Node(
        package='mini_project',
        executable='task_server',
        name='task_server'
    )

    return LaunchDescription([threshold_arg, sensor, processor, alarm, task])