# Line-line-detection-ROS2
借鉴优达学城（Udacity）无人驾驶工程师学位的第二个项目-车道线检测，（具体参考https://s3.amazonaws.com/udacity-sdc/github/shield-carnd.svg）。
将其开发为一个ROS2功能包，ROS2版本为Foxy。


其中pub_image.py为使用openCV读取指定路径下的视频文件，然后实时发布sensor_msgs/Image消息类型数据。

image_processing.py为订阅图像数据，然后进行车道线检测流程，最后得到并发布处理后的图像，以及车道线的曲率半径、车辆偏离车道中心点的距离。

lane_line_msgs功能包为单独创建的消息类型包，用于定义车道线的曲率半径、车辆偏离车道中心点的距离两个数据。

功能包使用Python开发，涉及到ROS2的图像数据发布订阅，roslaunch的编写，参数文件的编写以及加载，消息文件的编写以及加载。


