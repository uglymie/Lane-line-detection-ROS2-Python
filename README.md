# Line-line-detection-ROS2/Python
借鉴优达学城（Udacity）[无人驾驶工程师学位的第二个项目-车道线检测](https://github.com/udacity/CarND-Advanced-Lane-Lines)
将其开发为一个ROS2功能包，ROS2版本为Foxy，开发语言为Python。

# 实现功能

其中pub_image.py为使用openCV读取指定路径下的视频文件，然后实时发布sensor_msgs/msg/Image消息类型数据。

image_processing.py为订阅图像数据，然后进行车道线检测流程，最后得到并发布处理后的图像，以及车道线的曲率半径、车辆偏离车道中心点的距离。

lane_line_msgs功能包为单独创建的消息类型包，用于定义车道线的曲率半径、车辆偏离车道中心点的距离两个数据。

功能包使用Python开发，涉及到ROS2的图像数据发布订阅，roslaunch的编写，参数文件的编写和加载，消息文件的编写和加载。

# 一些改进

将原项目中加载棋盘格图像计算相机矩阵以及畸变系数，改为事先计算好，通过launch文件或yaml文件的参数形式加载。

# 编译运行

将功能包复制到自己的工作空间，运行编译命令：
```
colcon build
```
修改launch文件里面视频文件的路径：
```
Node(
    package='py_advanced_lane_lines',
    executable='pub_image',
    parameters=[
        {"image_pub_topic_name": '/camera/image_raw'},
        {"video_path": 'your video path'}
    ]
),
```
这里使用的视频文件可以在最开始提到的优达学城的仓库里下载，其他的资源文件均在编译时复制到share相关目录下，便于加载。
最后刷新. install/setup.bash文件，使用launch文件启动：
```
ros2 launch py_advanced_lane_lines lane_line_detection_launch.py 
```

# 消息订阅

![image](https://user-images.githubusercontent.com/47886076/138822518-6dbdc429-f854-4255-bcf0-d0d3300795e1.png)

# 图像订阅

![image](https://user-images.githubusercontent.com/47886076/138821359-2cbb1257-d2ba-48a7-8489-d2daa2562f26.png)

![image](https://user-images.githubusercontent.com/47886076/138822490-588a524e-3a42-4ed6-bf30-8621774bb488.png)

![image](https://user-images.githubusercontent.com/47886076/138822505-4c3f341d-36c2-4a54-b0dc-88dec5e32757.png)
