import os
import time

import cv2
import win32api

from abstract_class.abstract_camera_module import AbstractCameraModule


class CameraModulePyuEye(AbstractCameraModule):

    def __init__(self, gain: int = 50, exposure: int = 50):
        self.gain = gain
        self.exposure = exposure

    def single_image(self):
        # 執行 exe
        # 把text.png改名成 single_image.png

        self.gain = 25
        self.exposure = 50

        os.system('C:\\Users\\user\\PycharmProjects\\230calibration-system\\device_http_server'
                  '\\camera_module\\20221003_narl_ueye_cpp_save_img.exe ' + str(self.gain) + ' ' + str(self.exposure))
        # win32api.ShellExecute(0, 'open',
        #                       'C:\\Users\\user\\PycharmProjects\\230calibration-system\\device_http_server'
        #                       '\\camera_module\\20220926_narl_ueye_cpp_save_img.exe',
        #                       '25 25', '', 0)
        return True

    def close_camera(self):
        pass
