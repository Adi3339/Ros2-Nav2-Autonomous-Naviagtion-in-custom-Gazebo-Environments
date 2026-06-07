from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():

    nav2_dir = get_package_share_directory('nav2_bringup')
    pkg_my_project = get_package_share_directory('my_project')

    params_file = os.path.join(
        pkg_my_project,
        'params',
        'my_params.yaml'
    )
    print("\n" + "="*60)
    print("NAV2 PARAMS FILE:")
    print(params_file)
    print("="*60 + "\n")

    return LaunchDescription([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(
                    nav2_dir,
                    'launch',
                    'navigation_launch.py'
                )
            ),
            launch_arguments={
                'params_file': params_file,
                'use_sim_time': 'true',
                'autostart' : 'true'
            }.items()
        )
    ])
