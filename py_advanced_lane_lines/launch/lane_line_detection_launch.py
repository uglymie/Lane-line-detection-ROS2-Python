from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    pkg_share_dir = get_package_share_directory('py_advanced_lane_lines')

    camera_matrix = [[1156.60712, 0.0, 668.960301],
                     [0.0, 1151.64235, 388.057003],
                     [0.0, 0.0, 1.0]]
    dist_coeff = [-0.23185387, -0.11832052, -
                  0.00116561,  0.00023902,  0.15356154]
    cm0 = [1156.60712, 0.0, 668.960301]
    cm1 = [0.0, 1151.64235, 388.057003]
    cm2 = [0.0, 0.0, 1.0]

    yaml_path = pkg_share_dir + '/configs/lines_detect.yaml'

    return LaunchDescription([
        Node(
            package='py_advanced_lane_lines',
            executable='pub_image',
            parameters=[
                {"image_pub_topic_name": '/camera/image_raw'},
                {"video_path": '/program/ros1_projects/shuttle_bus_ws/src/advanced_lane_lines/res/project_video.mp4'}
            ]
        ),

        Node(
            package='py_advanced_lane_lines',
            executable='lane_line_detection',

            # parameters=[
            #     {"res_dir": pkg_share_dir + '/images/'},
            #     {"image_sub_topic_name": '/camera/image_raw'},
            #     # camera_matrix
            #     {"cm0": cm0},
            #     {"cm1": cm1},
            #     {"cm2": cm2},

            #     {"dist_coeff": dist_coeff},

            # ],

            # 通过加载符合规则的yaml参数文件
            parameters=[
                yaml_path,
            ]
        )
    ])
