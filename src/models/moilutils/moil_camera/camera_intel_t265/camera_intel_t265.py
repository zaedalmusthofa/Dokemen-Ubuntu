import os
import sys
import warnings
from typing import List, Tuple

import numpy as np
import pyrealsense2 as rs

sys.path.append(os.path.dirname(__file__))
from abstract_moil_camera import AbstractMoilCamera


class CameraIntelT265(AbstractMoilCamera):

    @classmethod
    def scan(cls) -> List[int] or List[str]:
        port_list = []
        try:
            pipe = rs.pipeline()
            pipe.start()
        except RuntimeError as e:
            print(e)
            return port_list
        for port in range(16):
            frame_set = pipe.wait_for_frames()
            frame_set = frame_set.get_fisheye_frame(port).as_video_frame()
            if frame_set:
                port_list.append(port)
                # pipe.stop()
            else:
                continue

        return port_list

    def __init__(self, cam_id: int, resolution: Tuple[int, int] = None):
        self.__cam_id = cam_id
        self.pipe = rs.pipeline()
        self.config = rs.config()
        self.profile = None

        self.__is_open: bool = False
        self.__current_resolution = resolution
        if self.__current_resolution:
            self.set_resolution(resolution)

        self.open()
        if resolution:
            self.set_resolution(resolution)

    def get_resolution(self) -> Tuple[int, int]:
        if self.__is_open:
            res = self.profile.get_stream(rs.stream.fisheye).as_video_stream_profile().get_intrinsics()
            w = int(res.width)
            h = int(res.height)
            self.__current_resolution = (w, h)

        return self.__current_resolution

    def set_resolution(self, resolution: Tuple[int, int]):
        warning_msg = '\nIntel T265 cannot change the resolution'
        warnings.warn(warning_msg)
        return None, None

    def frame(self) -> np.ndarray:
        frames = self.pipe.wait_for_frames()
        fisheye_frame = frames.get_fisheye_frame(self.__cam_id)
        frame = np.asanyarray(fisheye_frame.get_data())
        return frame

    def open(self) -> bool:
        if self.__cam_id not in self.scan():
            exception_msg = f'Invalid camera ID: "{self.__cam_id}", please check valid camera ID with "Moilcam.scan_id()"'
            raise Exception(exception_msg)

        if not self.__is_open:
            self.profile = self.pipe.start(self.config)

            self.__is_open = True

            if self.__current_resolution:
                self.set_resolution(self.__current_resolution)
            else:
                self.get_resolution()

        return self.__is_open

    def close(self) -> bool:
        if self.__is_open:
            self.pipe.stop()
            self.__is_open = False

        return self.__is_open

    def is_open(self) -> bool:
        if self.profile:
            self.__is_open = True

        if not self.profile:
            self.__is_open = False

        return self.__is_open
