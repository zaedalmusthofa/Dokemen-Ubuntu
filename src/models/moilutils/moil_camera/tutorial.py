"""
!!! Do This First !!!
Please move this Python file to the parent directory of "moil_camera/".
(Same layer with "moil_camera/")

!!! Before run this python code !!!
"""

# Camera type (MoilCam have supported)
# print('[Cam-Type]', MoilCam.supported_cam_type())
#
# USB Camera
from moilcam import MoilCam

print('[Cam-ID]', MoilCam.scan(cam_type='opencv_usb_cam'))
cam = MoilCam(cam_type='opencv_usb_cam', cam_id=0)  # Give USB Camera number

# # IP Camera
# from moilcam import MoilCam
# print('[Cam-ID]', MoilCam.scan(cam_type='opencv_ip_cam', admin_pwd='<admin_password>'))  # Give your system admin password
# cam = MoilCam(cam_type='opencv_ip_cam', cam_id='<protocol>://<ip><suffix>')  # Give IP Camera URL
# Example of "cam_id":
# rtsp://192.168.113.73:554/live.sdp
# http://192.168.13.73:554/stream.mjpg

import cv2

prev_fps = 0
while True:
    frame = cam.frame()
    frame = cv2.resize(frame, (640, 480), interpolation=cv2.INTER_AREA)
    fps = cam.get_fps(0.5)  # set how long you want return fps / unit seconds
    if fps is not None:  # if is None need wait so just print last fps
        prev_fps = fps
        cv2.putText(frame, str(fps), (7, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (100, 255, 0), 3, cv2.LINE_AA)
    else:
        cv2.putText(frame, str(prev_fps), (7, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (100, 255, 0), 3, cv2.LINE_AA)

    cv2.imshow('image_display', frame)
    if cv2.waitKey(1) == ord('q'):
        cam.close()
        break
