import os
from glob import glob
from setuptools import setup

package_name = 'mini_project'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'),
            glob('launch/*.launch.py')),
        (os.path.join('share', package_name, 'config'),
            glob('config/*.yaml')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Student',
    maintainer_email='student@example.com',
    description='Integration mini-project',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'sensor_node = mini_project.sensor_node:main',
            'processor_node = mini_project.processor_node:main',
            'alarm_server = mini_project.alarm_server:main',
            'task_server = mini_project.task_server:main',
        ],
    },
)