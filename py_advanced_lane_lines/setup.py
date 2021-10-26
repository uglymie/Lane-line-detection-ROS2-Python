from setuptools import setup
from glob import glob
import os

package_name = 'py_advanced_lane_lines'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/lane_line_detection_launch.py']),
        # (os.path.join('share', package_name), glob('./launch/*launch.py')), # Multiple files
        (os.path.join('share', package_name + '/images'), glob('./resource/images/*.png')),
        (os.path.join('share', package_name + '/configs'), glob('./configs/*.yaml')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='uglybaa',
    maintainer_email='uglybaa@todo.todo',
    # description='TODO: Package description',
    # license='TODO: License declaration',
    keywords=['ROS'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Topic :: Software Development',
    ],
    description='Examples of minimal publishers using rclpy.',
    license='Apache License, Version 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        'pub_image = py_advanced_lane_lines.pub_image:main',
        'lane_line_detection = py_advanced_lane_lines.image_processing:main'
        ],
    },
)
