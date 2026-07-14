from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    config = PathJoinSubstitution([
        FindPackageShare('params_launch_demo'),
        'config', 'params.yaml'
    ])

    rate_override = DeclareLaunchArgument(
        'publish_rate', default_value='-1.0',
        description='Override publish_rate from YAML (-1 to use YAML value)'
    )

    node = Node(
        package='params_launch_demo',
        executable='timed_talker',
        name='timed_talker',
        parameters=[config, {
            'publish_rate': LaunchConfiguration('publish_rate'),
        }]
    )

    return LaunchDescription([rate_override, node])