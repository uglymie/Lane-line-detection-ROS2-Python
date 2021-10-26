#!/usr/bin/env python

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

import cv2
# import numpy


class ImagePublisher(Node):

    def __init__(self):
        super().__init__('image_publisher')
        self.loadParam()
        
        self.publisher_ = self.create_publisher(Image, self.image_pub_topic_name, 3)
        timer_period = 0.01  # seconds
        self.timer = self.create_timer(timer_period, self.timerCallback)
        
        self.videoCapture()
        self.bridge = CvBridge()
        # self.msg = Image()

    def loadParam(self):
        self.declare_parameter('image_pub_topic_name','/camera/image_raw')
        self.declare_parameter('video_path','')
        
        self.image_pub_topic_name = self.get_parameter('image_pub_topic_name').value
        self.video_path = self.get_parameter('video_path').value

    def videoCapture(self):
        self.capture = cv2.VideoCapture(self.video_path)
        # self.capture = cv2.VideoCapture(0)
        if not self.capture.isOpened():
            self.get_logger().info('Read video Failed !')
        
        self.frame_num = self.capture.get(cv2.CAP_PROP_FRAME_COUNT)
        self.get_logger().info('frame num: "%s"' % self.frame_num)
        self.flag = 0


    def timerCallback(self):
        if self.flag == self.frame_num:
            self.videoCapture()
  
        ref, frame = self.capture.read()
        # msg.encoding = 'bgr8'
        # msg.height = frame.shape[0]
        # msg.width = frame.shape[1]
        # msg.step = frame.shape[1]*frame.shape[2]
        # msg.data = numpy.array(frame).tostring()
        # msg.header.stamp = self.get_clock().now().to_msg()
        
        msg = self.bridge.cv2_to_imgmsg(frame, encoding="bgr8")
        msg.header.frame_id = 'camera'
        msg.header.stamp = self.get_clock().now().to_msg()
        
        self.publisher_.publish(msg)
        # self.get_logger().info('Publishing: "%s"' % msg.data)
        self.flag = self.flag + 1

def main(args=None):
    rclpy.init(args=args)
    image_pub = ImagePublisher()
    
    rclpy.spin(image_pub)
    image_pub.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

