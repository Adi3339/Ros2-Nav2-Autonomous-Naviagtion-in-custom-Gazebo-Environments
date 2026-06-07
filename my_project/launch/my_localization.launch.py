from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument, OpaqueFunction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    nav2_dir = get_package_share_directory('nav2_bringup')
    pkg_my_project = get_package_share_directory('my_project')

    map_file = os.path.join(pkg_my_project, 'maps', 'my_map_ver2.yaml')

    # Debug print
    def print_map(context):
        print("\n" + "="*70)
        print("📍 LOADING MAP:")
        print(map_file)
        print("="*70 + "\n")
        return []

    return LaunchDescription([
        DeclareLaunchArgument('map', default_value=map_file),
        DeclareLaunchArgument('use_sim_time', default_value='true'),
        DeclareLaunchArgument('autostart', default_value='true'),

        OpaqueFunction(function=print_map),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(nav2_dir, 'launch', 'localization_launch.py')
            ),
            launch_arguments={
                'map': map_file,
                'use_sim_time': 'true',
                'autostart': 'true'          
            }.items()
        )
    ])
