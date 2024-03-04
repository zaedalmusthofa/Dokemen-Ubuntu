import os
import sys
import time
import warnings
from typing import List, Tuple

import cv2
import numpy as np

sys.path.append(os.path.dirname(__file__))
from abstract_moil_camera import AbstractMoilCamera


class CameraOpencvbUsb(AbstractMoilCamera):

    @classmethod
    def scan(cls) -> List[int] or List[str]:
        port_list = []
        for port in range(10):
            if os.name == 'nt':
                cv2_cap = cv2.VideoCapture(port, cv2.CAP_DSHOW)

            else:
                cv2_cap = cv2.VideoCapture(port)

            if cv2_cap.isOpened():
                port_list.append(port)
                cv2_cap.release()

            else:
                continue

        return port_list

    def __init__(self, cam_id: int, resolution: Tuple[int, int] = None):
        self.prev_frame_time = time.time()
        self.frame_count = 0
        self.__cam_id = cam_id
        self.__cap = None

        self.__is_open: bool = False
        self.__current_resolution = resolution
        if self.__current_resolution:
            self.set_resolution(resolution)

        self.open()
        if resolution:
            self.set_resolution(resolution)

    def get_resolution(self) -> Tuple[int, int]:
        if self.__is_open:
            w = int(self.__cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            h = int(self.__cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            self.__current_resolution = (w, h)

        return self.__current_resolution

    def set_resolution(self, resolution: Tuple[int, int]) -> Tuple[int, int]:

        set_w, set_h = resolution
        self.__current_resolution = (set_w, set_h)

        if self.__is_open:
            self.__cap.set(cv2.CAP_PROP_FRAME_WIDTH, set_w)
            self.__cap.set(cv2.CAP_PROP_FRAME_HEIGHT, set_h)
            real_w, real_h = self.get_resolution()
            if set_w != real_w or real_h != set_h:
                invalid_resolution_msg = f'Invalid resolution "({set_w}, {set_h})", ' \
                                         f'real resolution be set as "({int(real_w)}, {int(real_h)})", ' \
                                         f'check valid resolution with "MoilCam.valid_resolution()"'
                warnings.warn(invalid_resolution_msg)
                self.__current_resolution = (real_w, real_h)

        return self.__current_resolution

    def frame(self) -> np.ndarray:
        _, frame = self.__cap.read()
        return frame

    def open(self) -> bool:
        if self.__cam_id not in self.scan():
            exception_msg = f'Invalid camera ID: "{self.__cam_id}", please check valid camera ID with ' \
                            f'"Moilcam.scan_id()" '
            raise Exception(exception_msg)

        if not self.__is_open:
            if os.name == 'nt':
                self.__cap = cv2.VideoCapture(self.__cam_id, cv2.CAP_DSHOW)
            else:
                self.__cap = cv2.VideoCapture(self.__cam_id)
            self.__cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('M', 'J', 'P', 'G'))
            self.__is_open = True

            if self.__current_resolution:
                self.set_resolution(self.__current_resolution)
            else:
                self.get_resolution()

        return self.__is_open

    def close(self) -> bool:
        if self.__cap.isOpened():
            self.__cap.release()
            self.__is_open = False

        return self.__is_open

    def is_open(self) -> bool:
        if self.__cap.isOpened():
            self.__is_open = True

        if not self.__cap.isOpened():
            self.__is_open = False

        return self.__is_open

    def set(self, cam_property, cam_value):
        self.__cap.set(cam_property, cam_value)

    def get(self, cam_property):
        return self.__cap.get(cam_property)

    def get_fps(self, update_frequency):
        current_time = time.time()
        elapsed_time = current_time - self.prev_frame_time

        self.frame_count += 1

        if elapsed_time >= update_frequency:
            fps = self.frame_count / elapsed_time
            self.prev_frame_time = current_time
            self.frame_count = 0
            return int(fps)
        else:
            return None
