import os

from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    # Define LaunchDescription variable
    ld = LaunchDescription()

    # use:
    #  - 'zed' for "ZED" camera
    #  - 'zedm' for "ZED mini" camera
    #  - 'zed2' for "ZED2" camera
    camera_model = 'zed2'

    # Camera name
    camera_name = 'zed2'

    # URDF file to be loaded by Robot State Publisher
    urdf = os.path.join(
        get_package_share_directory('zed_wrapper'),
        'urdf', camera_model + '.urdf'
    )

    # ZED Configurations to be loaded by ZED Node
    config_common = os.path.join(
        get_package_share_directory('zed_wrapper'),
        'config',
        'common.yaml'
    )

    config_camera = os.path.join(
        get_package_share_directory('zed_wrapper'),
        'config',
        camera_model + '.yaml'
    )

    # Set LOG format
    os.environ['RCUTILS_CONSOLE_OUTPUT_FORMAT'] = '{time} [{name}] [{severity}] {message}'

    # Robot State Publisher node
    rsp_node = Node(
        package='robot_state_publisher',
        namespace="/"+camera_name,
        executable='robot_state_publisher',
        name=camera_name+'_state_publisher',
        output='screen',
        arguments=[urdf],
    )

    svo_file_arg = DeclareLaunchArgument('svo_file', default_value='', description='Launch zed with the specified svo file')

    # ZED Wrapper node
    zed_wrapper_node = Node(
        package='zed_wrapper',
        namespace="/"+camera_name,
        executable='zed_wrapper',
        name='zed_node',
        output='screen',
        parameters=[
            {'general.svo_file' : LaunchConfiguration('svo_file')},
            config_common,  # Common parameters
            config_camera,  # Camera related parameters
        ]
    )

    # Add nodes to LaunchDescription
    ld.add_action(rsp_node)
    ld.add_action(svo_file_arg)
    ld.add_action(zed_wrapper_node)

    return ld
