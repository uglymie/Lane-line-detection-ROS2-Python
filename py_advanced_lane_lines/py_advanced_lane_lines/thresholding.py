import cv2
import numpy as np

def threshold_rel(img, lo, hi):
    vmin = np.min(img)
    vmax = np.max(img)
    
    vlo = vmin + (vmax - vmin) * lo
    vhi = vmin + (vmax - vmin) * hi
    return np.uint8((img >= vlo) & (img <= vhi)) * 255

def threshold_abs(img, lo, hi):
    return np.uint8((img >= lo) & (img <= hi)) * 255

def threshold_yellow(img, lo, hi):
    th = 255 / np.max(img)
    # 如果没有黄色分量则不进行归一化
    if np.max(img) > 100:
        img = img * (255 / np.max(img))

    binary_output = np.zeros_like(img)
    if (th <= 1.5):
        # 根据大小阈值进行二值化
        binary_output[((img >= lo) & (img <= hi))] = 1

    return np.uint8(binary_output)*255

def threshold_white(img, lo, hi):
    img = img*(255/np.max(img))
    binary_output = np.zeros_like(img)
    binary_output[(img >= lo) & (img <= hi)] = 1
    return np.uint8(binary_output)*255


class Thresholding:
    """ This class is for extracting relevant pixels in an image.
    """
    def __init__(self):
        """ Init Thresholding."""
        pass

    def forward(self, img):
        """ Take an image and extract all relavant pixels.

        Parameters:
            img (np.array): Input image

        Returns:
            binary (np.array): A binary image represent all positions of relavant pixels.
        """
        hls = cv2.cvtColor(img, cv2.COLOR_RGB2HLS)
        hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2Lab)

        h_channel = hls[:,:,0]
        l_channel = hls[:,:,1]
        s_channel = hls[:,:,2]
        v_channel = hsv[:,:,2]
        b_channel = lab[:,:,2]

        #第一种方法
        # right_lane = threshold_rel(l_channel, 0.8, 1.0)
        # right_lane[:,:750] = 0

        # left_lane = threshold_abs(h_channel, 20, 30)
        # left_lane &= threshold_rel(v_channel, 0.7, 1.0)
        # left_lane = threshold_rel(v_channel, 0.7, 1.0)
        # left_lane[:,550:] = 0

        #第二种方法
        right_lane = threshold_white(l_channel, 220, 255)
        # right_lane[:,:750] = 0

        left_lane = threshold_yellow(b_channel, 195, 255)
        # left_lane[:,550:] = 0
        
        # combined_binary = np.zeros_like(right_lane)
        # combined_binary[(left_lane == 1) | (right_lane == 1)] = 1

        combined_binary = left_lane | right_lane
        return combined_binary
        
