from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    # Get package directories
    pkg_gazebo_ros = get_package_share_directory('gazebo_ros')
    launch_file_dir = os.path.join(get_package_share_directory('turtlebot3_gazebo'), 'launch')
    pkg_my_project = get_package_share_directory('my_project')

    # Launch Arguments
    use_sim_time = DeclareLaunchArgument(
        'use_sim_time', default_value='true', description='Use simulation time'
    )

    world_arg = DeclareLaunchArgument(
        'world',
        default_value=os.path.join(pkg_my_project, 'worlds', 'office_small_4.world'),
        description='Full path to world file'
    )

    x_pose = DeclareLaunchArgument('x_pose', default_value='0.0')
    y_pose = DeclareLaunchArgument('y_pose', default_value='0.0')
    z_pose = DeclareLaunchArgument('z_pose', default_value='0.02')

    # Launch Configurations
    world = LaunchConfiguration('world')

    # ==================== GAZEBO ====================
    gzserver_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_ros, 'launch', 'gzserver.launch.py')
        ),
        launch_arguments={'world': world}.items()
    )

    gzclient_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_ros, 'launch', 'gzclient.launch.py')
        )
    )

    # ==================== ROBOT ====================
    robot_state_publisher_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(launch_file_dir, 'robot_state_publisher.launch.py')
        ),
        launch_arguments={'use_sim_time': LaunchConfiguration('use_sim_time')}.items()
    )

    spawn_turtlebot_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(launch_file_dir, 'spawn_turtlebot3.launch.py')
        ),
        launch_arguments={
            'x_pose': LaunchConfiguration('x_pose'),
            'y_pose': LaunchConfiguration('y_pose'),
            'z_pose': LaunchConfiguration('z_pose'),
        }.items()
    )

    # ==================== Launch Description ====================
    ld = LaunchDescription()

    ld.add_action(use_sim_time)
    ld.add_action(world_arg)
    ld.add_action(x_pose)
    ld.add_action(y_pose)
    ld.add_action(z_pose)

    ld.add_action(gzserver_cmd)
    ld.add_action(gzclient_cmd)
    ld.add_action(robot_state_publisher_cmd)
    ld.add_action(spawn_turtlebot_cmd)

    return ld
