from typing import Tuple

from import_module import *
from abstract_moil_camera import AbstractMoilCamera


class MoilCam(object):

    def __new__(cls, cam_type: str, cam_id: int or str, resolution: Tuple[int, int] = None) -> AbstractMoilCamera:
        """

        :param cam_type: str
        :param cam_id: int or str
        :param resolution: Tuple[width: int, height: int]

        :return: AbstractMoilCamera
        """

        MoilCam.__raise_exception_invalid_cam_type(cam_type)

        if cam_type == 'opencv_usb_cam':
            return CameraOpencvbUsb(cam_id, resolution)

        if cam_type == 'opencv_ip_cam' or cam_type == 'camera_url':
            return CameraOpencvIP(cam_id)

        # if cam_type == 'intel_t265':
        #     return CameraIntelT265(cam_id, resolution)

        if cam_type == 'ids_peak':
            return CameraIDSpeak(cam_id, resolution)

    @staticmethod
    def supported_cam_type():
        """ List all supported camera type

        :return: list
        """

        # Other camera type under developing
        supported_cam_type = [
            'opencv_usb_cam',
            'opencv_ip_cam',
            # 'intel_t265',
            # 'ids_peak',
            'camera_url'
        ]

        return supported_cam_type

    @staticmethod
    def scan(cam_type: str, admin_pwd: str = None) -> list or dict:
        """
        Detect valid camera ID by cam_type

        :param admin_pwd: str
        :param cam_type: str
        :return: list
        """
        MoilCam.__raise_exception_invalid_cam_type(cam_type)
        list_uab_cam_type = MoilCam.supported_cam_type()

        for usb_cam_type_name in list_uab_cam_type:
            if usb_cam_type_name in cam_type.lower():
                if cam_type == 'opencv_usb_cam':
                    return CameraOpencvbUsb.scan()

                if cam_type == 'opencv_ip_cam':
                    return CameraOpencvIP.scan(admin_pwd)

                # if cam_type == 'intel_t265':
                #     return CameraIntelT265.scan()
                #
                # if cam_type == 'ids_peak':
                #     return CameraIDSpeak.scan()

    @staticmethod
    def __raise_exception_invalid_cam_type(cam_type):
        if cam_type not in MoilCam.supported_cam_type():
            exception_msg = f'Invalid cam_type "{cam_type}", ' \
                            f'please check valid cam_type with "MoilCam.supported_cam_type()"'
            raise Exception(exception_msg)


"""
Testing Code
"""
if __name__ == "__main__":

    import cv2

    # !!! Change Camera Type you want !!!
    cam_id = 'revodata_i7063phs_1'

    print('[Cam-type]', MoilCam.supported_cam_type())
    dict_url = MoilCam.scan('opencv_ip_cam', 'mcut1234')
    print('[Dict-url]', dict_url)

    cam_url = dict_url[cam_id]
    print('[Cam-url]', cam_url)

    cam = MoilCam('opencv_ip_cam', cam_url, (4000, 3000))

    print('[Cam-open]', cam.is_open())
    print('[Cam-resolution]', cam.get_resolution())

    while True:

        img = cam.frame()
        # img = cv2.resize(img.copy(), (1600, 1200))

        cv2.imshow('img', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.close()
    print(cam.is_open())
