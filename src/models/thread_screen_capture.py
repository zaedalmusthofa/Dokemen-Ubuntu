import os
from datetime import datetime

from PyQt6.QtCore import pyqtSignal, QObject, QTimer, QThread
from PyQt6 import QtWidgets
import cv2
import numpy as np


class Worker(QObject):
    get_image = pyqtSignal(object)

    def __init__(self):
        """
        Initializes the ScreenImageWorker class.

        Args:
            None

        Returns:
            None

        Raises:
            None
        """
        QObject.__init__(self)
        self.out = None
        self.event = None
        self.timer = None
        self.__record = False
        index = QtWidgets.QApplication.primaryScreen().grabWindow()
        try:
            image = self.qt_pixmap_to_cv_img(index)
            self.size_wind = (image.shape[1], image.shape[0])
        except:
            pass
        _time = datetime.now()
        self._time = _time.strftime("record_%H_%M_%S")

    def initialize_record_screen(self):
        """
        Initializes the screen recording by creating a VideoWriter object.

        If the VideoWriter object has not been created yet, this function creates it and sets the output video file path and codec.
        If the directory to store the recorded file does not exist, it will create it.

        Args:
            None

        Returns:
            None

        Raises:
            None
        """
        if self.out is None:
            fourcc = cv2.VideoWriter_fourcc(*'MJPG')
            path_file = os.path.normpath(os.getcwd() + os.sep + os.pardir)
            dst_directory = path_file + "/file_recorded/"
            if not os.path.isdir(dst_directory):
                os.makedirs(os.path.dirname(dst_directory))
            file_record = dst_directory + self._time + ".avi"
            self.out = cv2.VideoWriter(file_record, fourcc, 10.0, self.size_wind)

    @property
    def record_state(self):
        """
        A getter method for the private variable __record.

        Args:
            None

        Returns:
            bool: The current state of the recording (True for active, False for inactive).

        Raises:
            None
        """
        return self.__record

    @record_state.setter
    def record_state(self, state):
        """
        A setter method for the private variable __record.

        Args:
            state (bool): The state to set the recording to (True for active, False for inactive).

        Returns:
            None

        Raises:
            None
        """
        self.__record = state

    def get_event(self, event):
        """
        Stores the given event position.

        Args:
            event (QPoint): The QPoint object containing the event position.

        Returns:
            None

        Raises:
            None
        """
        self.event = event

    def update_label(self):
        """
        Updates the label with the current screen image.

        If recording is active, it writes the current screen image to the output video file.

        Args:
            None

        Returns:
            None

        Raises:
            None
        """
        if self.event is not None:
            index = QtWidgets.QApplication.screenAt(self.event)
            if index is not None:
                index = index.grabWindow()
                image = self.qt_pixmap_to_cv_img(index)
                if self.record_state:
                    self.out.write(image)

    @classmethod
    def qt_pixmap_to_cv_img(cls, qt_pixmap):
        """
        Converts a QPixmap object to a numpy array.

        Args:
            qt_pixmap (QPixmap): The QPixmap object to convert.

        Returns:
            numpy.ndarray: The converted image as a numpy array.

        Raises:
            None
        """
        q_img = qt_pixmap.toImage()
        temp_shape = (q_img.height(), q_img.bytesPerLine() * 8 // q_img.depth())
        temp_shape += (4,)
        ptr = q_img.bits()
        ptr.setsize(q_img.bytesPerLine() * q_img.height())
        result = np.array(ptr, dtype=np.uint8).reshape(temp_shape)
        result = result[..., :3]
        return result

    def main(self):
        """
        The main function of the VideoRecorder class.

        Initializes the QTimer object and sets the interval to 1/30 of a second.
        Connects the QTimer object to the update_label function.
        """
        self.timer = QTimer()
        self.timer.setInterval(int(1000 / 10))
        self.timer.timeout.connect(self.update_label)


class UpdaterImage:
    def __init__(self):
        self.thread = QThread()

        self.worker = Worker()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.update_label)
