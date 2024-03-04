from fastapi import FastAPI
from fastapi.responses import FileResponse
import time


class CameraHttpServer(FastAPI):
    def __init__(self, module):
        super().__init__(title="CameraHttpServer")

        @self.get("/close_camera")
        def close_camera():
            return {"message": module.close_camera()}

        @self.get("/single_image")
        def single_image():
            module.frame()
            time.sleep(0.4)
            return FileResponse("single_image.png")

import uvicorn

from camera_module.camera_module_pyueye import CameraModulePyuEye

# app = CameraHttpServer(CameraModuleOpencvUSB(2048, 1536))  # twarm usb210
# app = CameraHttpServer(CameraModuleOpencvUSB(1920, 1080))  # endoscope ometop
# app = CameraHttpServer(CameraModuleOpencvUSB(800, 600)) # yochung animal endoscopy
# app = CameraHttpServer(CameraModulePySpinUSB(4000, 3000))  # narl pyspin cam (2.0)

# app = CameraHttpServer(CameraModuleOpencvURL(2592, 1944))  # !!! Error !!! raspi url
# app = CameraHttpServer(CameraModuleOpencvURL(1920, 1920))  # vivotek url
# app = CameraHttpServer(CameraModuleIntelRealSense(cam_num=1))  # intel usb cam (3.0)
app = CameraHttpServer(CameraModulePyuEye())

uvicorn.run(app, host="192.168.113.56", port=8002, log_level="info")
