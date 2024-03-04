import sys
import os
sys.path.append(os.path.dirname(__file__))

from camera_opencv_usb.camera_opencv_usb import CameraOpencvbUsb
from camera_opencv_ip.camera_opencv_ip import CameraOpencvIP

file_path = os.path.abspath(__file__)
is_print_init_path = False


def print_init_file_path(is_print_init_path):
    if not is_print_init_path:
        print('[Camera Import Error]', file_path)
        return True


# try:
#     from camera_ids_peak.camera_ids_peak import CameraIDSpeak
# except Exception as exception_msg:
#     is_print_init_path = print_init_file_path(is_print_init_path)
#
#     dir_path = os.path.dirname(file_path)
#     ids_readme_path = file_path + '/README.md'
#     print('    "IDS Peak SDK" is not installed.\n'
#           '        If need to install, follow: "' + ids_readme_path + '"')

# try:
#     from camera_intel_t265.camera_intel_t265 import CameraIntelT265
# except Exception as exception_msg:
#     is_print_init_path = print_init_file_path(is_print_init_path)
#
#     print('    "Intel RealSense SDK" is not installed.\n'
#           '        If need to install, use: "pip3 install pyrealsense2"')
