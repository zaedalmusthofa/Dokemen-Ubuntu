import cv2
import EasyPySpin

from abstract_class.abstract_camera_module import AbstractCameraModule


class CameraModulePySpinUSB(AbstractCameraModule):

    def __init__(self, width: int = 640, height: int = 480):
        self.cap = EasyPySpin.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.cap.set(cv2.CAP_PROP_EXPOSURE, -1)
        self.cap.set(cv2.CAP_PROP_GAIN, -1)

    def single_image(self):
        if self.cap.isOpened():
            ret, frame = self.cap.read()
            cv2.imwrite("single_image.png", frame)
            return True
        return False

    def close_camera(self):
        self.cap.release()