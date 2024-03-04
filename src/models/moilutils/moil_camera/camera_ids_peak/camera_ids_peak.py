import cv2
import numpy as np
from typing import Tuple, List
from abstract_moil_camera import AbstractMoilCamera

from camera_ids_peak import ids_peak
from ids_peak_ipl import ids_peak_ipl

class CameraIDSpeak(AbstractMoilCamera):

    @classmethod
    def scan(cls) -> List[int] or List[str]:
        ids_peak.Library.Initialize()

        device_manager = ids_peak.DeviceManager.Instance()
        device_manager.Update()

        if device_manager.Devices().empty():
            print("No device found. Exiting Program.")
            return []

        device_num = 0
        for device in device_manager.Devices():
            device_num += 1

        ids_peak.Library.Close()

        return list(range(device_num))

    def __init__(self, cam_id: int, resolution: Tuple[int, int] = None):
        self.__cam_id = cam_id

        ids_peak.Library.Initialize()

        self.__device_manager = ids_peak.DeviceManager.Instance()
        self.__device_manager.Update()

        if resolution:
            if resolution != (4000, 3000):
                exception_msg = f'Invalid camera resolution: "{resolution}", ' \
                                f'please check valid camera resolution with "Moilcam.valid_resolution(\'ids_peak\')"'
                raise Exception(exception_msg)

        if self.__device_manager.Devices().empty():
            print("No device found.")
        else:
            self.open()

    def open(self) -> bool:
        if self.__cam_id not in self.scan():
            exception_msg = f'Invalid camera ID: "{self.__cam_id}", please check valid camera ID with "Moilcam.scan_id()"'
            raise Exception(exception_msg)

        self.__device = self.__device_manager.Devices()[self.__cam_id].OpenDevice(ids_peak.DeviceAccessType_Control)
        self.__node_map_remote_device = self.__device.RemoteDevice().NodeMaps()[self.__cam_id]

        # Set exposure time
        set_exposure_time = 31660  # micro seconds
        self.__node_map_remote_device.FindNode("ExposureTime").SetValue(set_exposure_time)

        # Set frame rate
        FPS_LIMIT = 30
        max_fps = self.__node_map_remote_device.FindNode("AcquisitionFrameRate").Maximum()
        target_fps = min(max_fps, FPS_LIMIT)
        self.__node_map_remote_device.FindNode("AcquisitionFrameRate").SetValue(target_fps)

        # Set gain
        self.__node_map_remote_device.FindNode("GainSelector").SetCurrentEntry("AnalogAll")
        self.__node_map_remote_device.FindNode("Gain").SetValue(2.0)
        self.__node_map_remote_device.FindNode("GainSelector").SetCurrentEntry("DigitalAll")
        self.__node_map_remote_device.FindNode("Gain").SetValue(2.5)


        # Flush queue and prepare all buffers for revoking
        self.__data_stream = self.__device.DataStreams()[self.__cam_id].OpenDataStream()
        self.__data_stream.Flush(ids_peak.DataStreamFlushMode_DiscardAll)

        # Clear all old buffers
        for buffer in self.__data_stream.AnnouncedBuffers():
            self.__data_stream.RevokeBuffer(buffer)

        # Get number of minimum required buffers
        num_buffers_min_required = self.__data_stream.NumBuffersAnnouncedMinRequired()

        self.__node_map_data_stream = self.__data_stream.NodeMaps()[self.__cam_id]
        payload_size = self.__node_map_data_stream.FindNode("PayloadSize").Value()

        # Alloc buffers
        for i in range(num_buffers_min_required):
            self.__buffer = self.__data_stream.AllocAndAnnounceBuffer(payload_size)
            self.__data_stream.QueueBuffer(self.__buffer)

        # Start Acquisition
        self.__data_stream.StartAcquisition()
        self.__node_map_remote_device.FindNode("TLParamsLocked").SetValue(1)
        self.__node_map_remote_device.FindNode("AcquisitionStart").Execute()
        self.__node_map_remote_device.FindNode("AcquisitionStart").WaitUntilDone()

    def frame(self) -> np.ndarray:
        buffer = self.__data_stream.WaitForFinishedBuffer(5000)

        # Create IDS peak IPL image from buffer
        image = ids_peak_ipl.Image_CreateFromSizeAndBuffer(
            buffer.PixelFormat(),
            buffer.BasePtr(),
            buffer.Size(),
            buffer.Width(),
            buffer.Height()
        )

        # Create IDS peak IPL image for debayering and convert it to RGBa8 format
        image_processed = image.ConvertTo(ids_peak_ipl.PixelFormatName_BGR8,
                                          ids_peak_ipl.ConversionMode_Fast)

        image_np_array = image_processed.get_numpy_3D()

        # After this method return, the bug will occur when cv2.imshow(image_np_array) without below .copy()
        image_np_array = image_np_array.copy()

        # Queue buffer again
        self.__data_stream.QueueBuffer(buffer)

        return image_np_array

    def close(self) -> bool:
        self.__node_map_remote_device.FindNode("TLParamsLocked").SetValue(0)
        self.__node_map_remote_device.FindNode("AcquisitionStop").Execute()
        self.__node_map_remote_device.FindNode("AcquisitionStop").WaitUntilDone()
        self.__device = None
        ids_peak.Library.Close()
        return True

    def is_open(self) -> bool:
        if self.__device:
            return True
        else:
            return False

    def get_resolution(self) -> Tuple[int, int]:
        return 4000, 3000

    def set_resolution(self, resolution: Tuple[int, int]) -> Tuple[int, int]:
        pass

    def set(self, cam_property: str = None, cam_value: str = None):
        if cam_property == "ExposureTime":
            set_exposure_time = float(cam_value)
            self.__node_map_remote_device.FindNode("ExposureTime").SetValue(set_exposure_time)
            return True

        else:
            exception_msg = f'Invalid camera property: "{cam_property}", camera property should be below:\n' \
                            f'1. \"ExposureTime\"\n' \
                            f'2. (Under Dev...)"'
            raise Exception(exception_msg)



if __name__ == "__main__":

    print(CameraIDSpeak.scan())

    cam = CameraIDSpeak(0)
    while True:

        img = cam.frame()
        img = cv2.resize(img.copy(), (1600, 1200))

        cv2.imshow('img', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.close()
