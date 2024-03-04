import cv2
import numpy as np
import pyrealsense2 as rs

from abstract_class.abstract_camera_module import AbstractCameraModule


class CameraModuleIntelRealSense(AbstractCameraModule):

    def __init__(self, width: int = 640, height: int = 480, cam_num: int = 1):
        self.cam_num = cam_num
        self.pipe = rs.pipeline()
        self.cfg = rs.config()
        self.pipe.start(self.cfg)

    def single_image(self):
        frameset = self.pipe.wait_for_frames()
        f = frameset.get_fisheye_frame(self.cam_num).as_video_frame()
        image = np.asanyarray(f.get_data())
        cv2.imwrite("single_image.png", image)
        return True

    def close_camera(self):
        self.pipe.stop()
