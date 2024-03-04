
"""
!!! Do This First !!!
Please move this Python file to the parent directory of "moil_camera/".
(Same layer with "moil_camera/")

!!! Before run this python code !!!
"""

# For OpenCV USB Camera
# from moil_camera import CameraOpencvbUsb
# print(CameraOpencvbUsb.scan())
# cam = CameraOpencvbUsb('0')  # Give USB Camera number

# For OpenCV IP Camera
from moil_camera.camera_opencv_ip.camera_opencv_ip import CameraOpencvIP
import cv2
print(CameraOpencvIP.scan("admin"))  # Give your system admin password
# cam = CameraOpencvIP('<protocol>://<ip><suffix>')
# rtsp://192.168.113.73:554/live.sdp 
# http://192.168.13.73:554/stream.mjpg


# while True:
#     print(cam.get_resolution())
#     frame = cam.frame()
#     frame = cv2.resize(frame, (1600, 1200), interpolation=cv2.INTER_AREA)
#     cv2.imshow('image_display', frame)
#
#     if cv2.waitKey(1) == ord('q'):
#         cam.close()
#         break
