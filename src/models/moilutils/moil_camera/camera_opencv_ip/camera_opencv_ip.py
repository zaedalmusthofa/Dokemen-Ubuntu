import os
import sys
import threading
from typing import Tuple
import cv2
import numpy as np

sys.path.append(os.path.dirname(__file__))
from abstract_moil_camera import AbstractMoilCamera
import ip_url_scaner


""" [ Bug Issue ]
The following "Bug" occurs, When running "continuously" :
    1. Scan mac (Scapy) with admin permission.
    2. Second time to open camera(OpenCV) through HTTP mjpg URL(RaspberryPi).

ERROR message:
[tcp @ 0x2b4f9c0] Connection to tcp://192.168.113.37:8000 failed: Connection timed out
[ERROR:0@7.720] global cap.cpp:164 open VIDEOIO(CV_IMAGES): raised OpenCV exception:
OpenCV(4.8.0) /io/opencv/modules/videoio/src/cap_images.cpp:253: error: (-5:Bad argument)
CAP_IMAGES: can't find starting number (in the name of file): http://<camera-address>:8000/<suffix> in function 'icvExtractPattern'


Bug Code ( For RaspberryPi: http://<url>/stream.mjpg )

print(ip_url_scaner.scan('<admin-password>'))  # Give admin password of system

cam = CameraOpencvIP('http://192.168.113.37:8000/stream.mjpg')

while True:
    frame = cam.frame()
    frame = cv2.resize(frame, (1600, 1200), interpolation=cv2.INTER_AREA)
    cv2.imshow('image_display', frame)

    if cv2.waitKey(1) == ord('q'):
        cam.close()
        break
"""


class CameraOpencvIP(AbstractMoilCamera):

    @classmethod
    def scan(cls, admin_pwd: str = None):
        if admin_pwd is None:
            err_msg = 'Admin password is None, Please give second argument <admin_pwd> '\
                      'When scan URL of IP camera. '\
                      'MoilCam.scan(\'opencv_ip_cam\', <admin_pwd>)'
            raise ValueError(err_msg)
        return ip_url_scaner.scan(admin_pwd)

    def __init__(self, stream_url: str):
        self.__stream_url = stream_url
        # Ex: 'http://192.168.113.37:8000/stream.mjpg'
        # Ex: 'rtsp://192.168.113.93:554/live.sdp'

        self.__cap = None
        self.__is_open = False
        self.__single_frame = None
        self.__current_resolution = None

        self.open()
        self.get_resolution()

    def open(self) -> bool:

        if not self.__is_open:

            self.__cap = cv2.VideoCapture(self.__stream_url)
            self.__is_open = True

        return self.__is_open

    def frame(self) -> np.ndarray:
        t = threading.Thread(target=self.thread_get_frame)
        t.start()
        t.join()
        return self.__single_frame

    def thread_get_frame(self):
        self.__ret, self.__single_frame = self.__cap.read()

    def close(self) -> bool:
        if self.__cap.isOpened():
            self.__cap.release()
            self.__is_open = False

        return self.__is_open

    def is_open(self) -> bool:
        if self.__cap.isOpened():
            self.__is_open = True
        else:
            self.__is_open = False

        return self.__is_open


    def get_resolution(self) -> Tuple[int, int]:
        if self.__is_open:
            w = int(self.__cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            h = int(self.__cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            self.__current_resolution = (w, h)

        return self.__current_resolution

    def set_resolution(self, resolution: Tuple[int, int]):

        print('Resolution of IP camera should be set through website.')

        return None, 'Resolution of IP camera should be set through website.'


# print(ip_url_scaner.scan('<admin-password>'))  # Give admin password of system
