#!/usr/bin/env python
# import roslib; roslib.load_manifest('common_msgs')
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from lane_line_msgs.msg import Line
from std_msgs.msg import Int64MultiArray

# from common_msgs.msg import Obstacle    # 自定义消息
# from common_msgs.srv import ModuleCmd
import numpy as np
import cv2

from py_advanced_lane_lines.thresholding import *
from py_advanced_lane_lines.perspective_transformation import *
from py_advanced_lane_lines.lane_lines import *
# from camera_calibration import CameraCalibration
from py_advanced_lane_lines.distortion_correction import CameraCalibration


class FindLaneLines(Node):

    def __init__(self):
        super().__init__('lines_detect')
        self.loadParam()
        
        self.image_sub = self.create_subscription(Image, self.image_sub_topic_name, self.imageCallback, 3)
        self.processed_image_pub = self.create_publisher(Image, '/image/lines', 3)
        self.line_pub = self.create_publisher(Line, '/line/info', 1000)


        """ Init Application"""
        # self.calibration = CameraCalibration(res, 9, 6)
        self.calibration = CameraCalibration(self.cameraMatrix, self.distCoeff)
        self.thresholding = Thresholding()
        self.transform = PerspectiveTransformation()
        self.lanelines = LaneLines(self.res_dir)

        self.bridge = CvBridge()
        
    def loadParam(self):
        self.declare_parameter('image_sub_topic_name','/camera/image_raw')
        self.declare_parameter('res_dir','res_dir')
        self.declare_parameter('cm0', [])
        self.declare_parameter('cm1', [])
        self.declare_parameter('cm2', [])
        self.declare_parameter('dist_coeff', [])
        # self.declare_parameter('camera_matrix', [])

        self.res_dir = self.get_parameter('res_dir').value
        self.image_sub_topic_name = self.get_parameter('image_sub_topic_name').value
        # dc = self.get_parameter('dist_coeff').value
        # cm = self.get_parameter('camera_matrix').value
        # self.get_logger().info('dist_coeff: %s' % dc)   # ROS2打印，print在roslaunch启动时无法打印

        cm0 = self.get_parameter('cm0').value
        cm1 = self.get_parameter('cm1').value
        cm2 = self.get_parameter('cm2').value
        
        self.cameraMatrix = np.array([cm0, cm1, cm2])
        self.distCoeff = np.array(self.get_parameter('dist_coeff').value)


    def forward(self, img):  # 传入图像，按照流程处理
        out_img = np.copy(img)
        img = self.calibration.undistort(img)
        img = self.transform.forward(img)
        img = self.thresholding.forward(img)
        img = self.lanelines.forward(img)
        img = self.transform.backward(img)

        out_img = cv2.addWeighted(out_img, 1, img, 0.6, 0)
        out_img, self.curvature, self.deviate = self.lanelines.plot(out_img)
        
        return out_img

    def imageCallback(self, msg):
        imput_img = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        out_img = self.forward(imput_img)
        self.processed_image_pub.publish(self.bridge.cv2_to_imgmsg(out_img, "bgr8"))
        line_msg = Line()
        line_msg.curvature = self.curvature
        line_msg.deviate  = self.deviate
        self.line_pub.publish(line_msg)


# 输出： 偏离中心点的距离，道路线边缘以及道路掩膜

def main(args=None):
    rclpy.init(args=args)
    find_lines = FindLaneLines()
    rclpy.spin(find_lines)

    find_lines.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
