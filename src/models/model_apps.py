"""
This Class is to provide model for moilapp application. to make it not make confuse on the plugin class
"""
import datetime
import re
import time

import cv2
import os

import git
import yaml
from PyQt6.QtGui import QCursor, QImage, qRgb
from PyQt6.QtCore import pyqtSignal, QObject, Qt, QTimer, QRect
from PyQt6.QtWidgets import QMessageBox
import numpy as np
from .model_main import Model
from .plugins_model import MoilFisheyeMarker


class ModelApps(QObject):
    signal_image_original = pyqtSignal(object)
    image_result = pyqtSignal(object)
    git_repository_info = pyqtSignal(dict)
    config_view_info = pyqtSignal(dict)
    alpha_beta = pyqtSignal(list)
    alpha_beta_in_recenter_image = pyqtSignal(list)
    slider_time_value = pyqtSignal(float)
    timer_video_info = pyqtSignal(list)
    timer_status = pyqtSignal(bool)
    recent_media_source = pyqtSignal(str)
    recenter_image = pyqtSignal(object)
    value_coordinate = pyqtSignal(list)
    value_coordinate_in_recenter_image = pyqtSignal(list)

    def __init__(self):
        """Initializes an instance of the class.

        Args:
            model: An instance of the `Model` class.

        Attributes:
            __model (`Model`): An instance of the `Model` class.
            __image (None): The current image being displayed.
            __moildev (None): An instance of the `Moildev` class.
            __media_source (None): The path to the media source file.
            __parameter_name (None): The name of the parameter used.
            __angle_rotate (None): The angle to rotate the image by.
            __map_x_anypoint (None): The x-coordinate of the point to display.
            __map_y_anypoint (None): The y-coordinate of the point to display.
            __map_x_pano (None): The x-coordinate of the panorama.
            __map_y_pano (None): The y-coordinate of the panorama.
            __configuration_view (None): The configuration view settings.
            __config_file (None): The path to the configuration file.
            __ratio_x (None): The ratio of the x-coordinate of the mouse click.
            __ratio_y (None): The ratio of the y-coordinate of the mouse click.
            __pos_x (None): The x-coordinate of the mouse click.
            __pos_y (None): The y-coordinate of the mouse click.
            __image_original (None): The original image.
            repo_github (None): The URL of the GitHub repository.
            __width_image_result (None): The width of the resulting image.
            __draw_polygon (True): Indicates whether to draw the polygon.
            __state_rubberband (False): Indicates whether the rubberband is active.
            __state_view ("FisheyeView"): The current view state.
            __pano_mode ("car"): The current panorama mode.
            __anypoint_mode ("mode_1"): The current anypoint mode.
            __size_rubberband (None): The size of the rubberband.
            __pos_video_image_saved ([]): The position of the video in the saved image.
            load_saved_image (False): Indicates whether to load a saved image.
            saved_image_list ([]): A list of saved images.
            cap (None): An instance of the OpenCV `VideoCapture` class.
            video (False): Indicates whether the video is active.
            fps (25): The frames per second of the video.
            i_camera (0): The index of the camera.

            timer (`QTimer`): A timer for the next frame signal.
        """
        super().__init__()
        self.__model = Model()
        self.__marker = MoilFisheyeMarker()
        self.__image = None
        self.__image_resize = None
        self.__moildev = None
        self.__moildev_recenter = None
        self.__moildev_recenter_a = None
        self.__media_source = None
        self.__parameter_name = None
        self.__angle_rotate = None
        self.__map_x_anypoint = None
        self.__map_y_anypoint = None
        self.__map_x_pano = None
        self.__map_y_pano = None
        self.__map_recenter = [None] * 4
        self.__configuration_view = None
        self.__config_file = None
        self.__ratio_x, self.__ratio_y = None, None
        self.__pos_x, self.__pos_y = None, None
        self.__image_original = None

        self.__raspi = False

        self.__cr_left_car_color = None
        self.__cr_right_car_color = None
        self.video_writer = None
        self.fps = 20

        self.repo_github = None
        self.__recenter_image_state = False
        self.rec_image = None

        self.__width_image_result = None
        self.__draw_polygon = True
        self.__state_rubberband = False
        self.__state_view = "FisheyeView"
        self.__pano_mode = "car"
        self.__anypoint_mode = "mode_1"

        self.__size_rubberband = None
        self.__pos_video_image_saved = []
        self.load_saved_image = False

        self.saved_image_list = []
        self.cap = None
        self.video = False
        self.fps = 25
        self.i_camera = 0

        self.ratio_resize = [1, 0.9, 0.8, 0.75, 0.6, 0.5, 0.4]
        self.resolution_option = []
        self.resolution_active_index = 0
        self.virtual_parameter = {}

        self.timer = QTimer()
        self.timer.timeout.connect(self.next_frame_signal)

    def save_image_file(self, image, dst_directory, type_camera=None):
        """
        Save an image file to the specified directory and add metadata to the configuration view.

        Args:
            image: A NumPy array containing the image data to be saved.
            dst_directory: A string representing the destination directory to save the image file.
            type_camera: An optional string representing the type of camera used to capture the image.

        Returns:
            A string representing the timestamp in the format "mmdd_HHMMSS" used in the saved image file name.

        Raises:
            None
        """
        ss = datetime.datetime.now().strftime("%m%d_%H%M%S")
        name = dst_directory + str(ss) + ".png"

        if not os.path.isdir(dst_directory):
            os.makedirs(os.path.dirname(dst_directory))
        cv2.imwrite(name, image)

        self.__configuration_view["Image_saved"][name] = {}
        self.__configuration_view["Image_saved"][name]["parent_path"] = self.__configuration_view["Media_path"]
        self.__configuration_view["Image_saved"][name]["is_video"] = self.video
        self.__configuration_view["Image_saved"][name]["state_view"] = self.state_recent_view
        if self.video:
            self.__configuration_view["Image_saved"][name]["pos_frame"] = self.pos_frame

        self.saved_image_list = list(self.__configuration_view["Image_saved"].keys())
        with open(self.__config_file, "w") as outfile:
            yaml.dump(self.__configuration_view, outfile, default_flow_style=False)

        if type_camera is not None:
            self.__model.write_camera_type(name, type_camera)
        return ss

    def add_position_video_on_saved_image(self):
        """Adds the current position of the video to the list of positions.

        If there is an active video, this method appends the current position of
        the video to the list of positions stored in the `__pos_video_image_saved`
        attribute. This list can be used later to create a map of where images were
        saved in the video.
        """
        if self.video:
            self.__pos_video_image_saved.append(self.pos_frame)

    def reopen_saved_image(self, file_name):
        """
        Reopen saved image file

        Args:
            file_name:

        Returns:

        """
        if self.timer.isActive():
            self.timer.stop()
            self.timer_status.emit(self.timer.isActive())
        self.image = cv2.imread(file_name)
        print("reopen_saved_image")
        self.calculate_resolution()
        self.resize_image()
        self.load_saved_image = True
        self.signal_image_original.emit(self.image_resize)
        self.image_result.emit(self.image_resize)

    def set_position_frame_save_image(self, file_name, original=False):
        """
        This function sets the position of a saved frame from the `Image_saved` list in the configuration view.
        If the timer is active, it will be stopped and the status will be emitted. If the parent path of the saved image
        is the same as the media source, the position of the frame will be set and the next frame signal
        will be emitted. If the parent path is different, the saved image will be reopened.

        Args:
            file_name (str): The name of the saved file.
            original (bool, optional): Flag to indicate if the view is in original or not. Defaults to False.


        Returns:
            None
        """
        if self.timer.isActive():
            self.timer.stop()
            self.timer_status.emit(self.timer.isActive())

        if self.__configuration_view["Image_saved"][file_name]["parent_path"] == self.__media_source:
            if self.__configuration_view["Image_saved"][file_name]["is_video"]:
                pos = self.__configuration_view["Image_saved"][file_name]["pos_frame"]
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, pos)
                if original:
                    self.state_recent_view = "FisheyeView"
                self.next_frame_signal()

        else:
            self.reopen_saved_image(file_name)

    def update_file_config(self):
        """
        This function updates the configuration file located in the cached directory.
        It sets the `__config_file` attribute to the path of the configuration file
        and loads the configuration data into the `__configuration_view` attribute.
        The function also updates the `parameter_name` attribute with the value of "Parameter_name"
        in the configuration data and sets the `saved_image_list` attribute with a list of keys
        from the "Image_saved" dictionary in the configuration data.

        Returns:
            None

        """
        path_file = os.path.dirname(os.path.realpath(__file__))
        self.__config_file = path_file + "/cached/cache_config.yaml"
        if os.path.exists(self.__config_file):
            with open(self.__config_file, "r") as file:
                self.__configuration_view = yaml.safe_load(file)
            self.parameter_name = self.__configuration_view["Parameter_name"]
            self.saved_image_list = list(self.__configuration_view["Image_saved"].keys())

    def set_media_source(self, source_type, cam_type, media_source, parameter_name):
        """
        Set up the media source for processing in this application.

        Args:
            cam_type: type of camera used
            media_source: the media source such as image, video or camera
            parameter_name: the parameter name

        Returns:
            None
        """
        if self.__configuration_view is not None:
            self.__configuration_view["Source_type"] = source_type
            self.__configuration_view["Cam_type"] = cam_type
            self.__configuration_view["Media_path"] = media_source
            self.__configuration_view["Parameter_name"] = parameter_name

            with open(self.__config_file, "w") as outfile:
                yaml.dump(self.__configuration_view, outfile, default_flow_style=False)
            self.load_saved_image = False
            # self.configuration_view = self.__configuration_view
        self.create_moildev()
        self.create_image_original()

    @property
    def recenter_image_state(self):
        return self.__recenter_image_state

    @recenter_image_state.setter
    def recenter_image_state(self, mode):
        self.__recenter_image_state = mode

    @property
    def image(self):
        """
        Original fisheye image of the application

        Returns:
            Image

        """
        return self.__image

    @image.setter
    def image(self, _image):
        """
        Setter original fisheye image

        Args:
            _image: original image

        Returns:
            None

        """
        self.__image = _image

    @property
    def image_resize(self):
        return self.__image_resize

    @image_resize.setter
    def image_resize(self, image):
        self.__image_resize = image

    @property
    def change_panorama_mode(self):
        """Get the current panorama mode.

        Returns:
            The current panorama mode as a string.
        """
        return self.__pano_mode

    @change_panorama_mode.setter
    def change_panorama_mode(self, mode):
        """Set the current panorama mode.

        Args:
            mode (str): The new panorama mode to set.
        """
        self.__pano_mode = mode

    @property
    def change_anypoint_mode(self):
        """Get the current anypoint mode.

        Returns:
            The current anypoint mode as a string.
        """
        return self.__anypoint_mode

    @change_anypoint_mode.setter
    def change_anypoint_mode(self, mode):
        """Set the current anypoint mode.

        Args:
            mode (str): The new anypoint mode to set.
        """
        self.__anypoint_mode = mode

    @property
    def state_recent_view(self):
        """Get the state of the recent view.

        Returns:
            True if the recent view is enabled, False otherwise.
        """
        return self.__state_view

    @state_recent_view.setter
    def state_recent_view(self, state_view):
        """Set the state of the recent view.

        Args:
            state_view (bool): The new state of the recent view.
        """
        self.__state_view = state_view
        # self.create_image_result()

    @property
    def state_rubberband(self):
        """Get the state of the rubberband.

        Returns:
            True if the rubberband is enabled, False otherwise.
        """
        return self.__state_rubberband

    @state_rubberband.setter
    def state_rubberband(self, state_rubberband):
        """
        int: The state of the rubber band.
        """
        self.__state_rubberband = state_rubberband

    @property
    def set_draw_polygon(self):
        """
        Sets the state of the rubber band.
        """
        return self.__draw_polygon

    @set_draw_polygon.setter
    def set_draw_polygon(self, state):
        """
        bool: Whether to draw a polygon.
        """
        self.__draw_polygon = state
        self.create_image_result()

    @property
    def set_angle_rotate(self):
        """
        Sets whether to draw a polygon and creates the image result.
        """
        return self.__angle_rotate

    @set_angle_rotate.setter
    def set_angle_rotate(self, angle_rotate):
        """
        int: The angle of rotation.
        """
        self.__angle_rotate = angle_rotate

    def set_width_image_on_label_result(self, width):
        """
        Sets the angle of rotation.
        """
        self.__width_image_result = width

    # Mouse Events Area +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def label_original_mouse_move_event(self, label, event):
        """Update the display and configuration in response to mouse movement.

        Args:
            label: A PyQt5.QtWidgets.QLabel object representing the label being displayed.
            event: A PyQt5.QtGui.QMouseEvent object representing the mouse event.

        Returns:
            None

        Raises:
            None
        """
        if self.image_resize is None:
            return

        if self.state_rubberband:
            return

        if self.load_saved_image:
            return

        self.__ratio_x, self.__ratio_y = self.__model.calculate_ratio_image2label(label, self.image_resize)
        x = round(int(event.position().x()) * self.__ratio_x)
        y = round(int(event.position().y()) * self.__ratio_y)
        self.value_coordinate.emit([x, y])

        if self.recenter_image_state:
            alpha, beta = self.__moildev.get_alpha_beta(x, y, 1)
            self.alpha_beta.emit([alpha, beta])

        else:
            if event.buttons() == Qt.MouseButton.NoButton:
                if self.__state_view == "FisheyeView":
                    image = self.__marker.point(self.image_resize.copy(), (x, y))
                    alpha, beta = self.__moildev.get_alpha_beta(x, y, 1)
                    self.alpha_beta.emit([alpha, beta])

                elif self.__state_view == "AnypointView":
                    label.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
                    image = self.__marker.point(self.__image_original.copy(), (x, y))
                    if self.change_anypoint_mode == "mode_1":
                        alpha, beta = self.__moildev.get_alpha_beta(x, y, 1)
                    else:
                        alpha, beta = self.__moildev.get_alpha_beta(x, y, 2)
                    self.alpha_beta.emit([alpha, beta])

                else:
                    image = self.__marker.point(self.__image_original.copy(), (x, y))
                    alpha, beta = self.__moildev.get_alpha_beta(x, y, 1)
                    self.alpha_beta.emit([alpha, beta])
                self.draw_crosshair_on_the_original_image(image)

            elif event.buttons() == Qt.MouseButton.LeftButton:
                if self.__state_view == "AnypointView":
                    label.setCursor(QCursor(Qt.CursorShape.ClosedHandCursor))
                    if self.change_anypoint_mode == "mode_1":
                        self.__configuration_view["Mode_1"]["coord"][0] = x
                        self.__configuration_view["Mode_1"]["coord"][1] = y
                        alpha, beta = self.__moildev.get_alpha_beta(x, y, 1)

                        if alpha is not None:
                            self.__configuration_view["Mode_1"]["alpha"] = round(alpha, 2)
                            self.__configuration_view["Mode_1"]["beta"] = round(beta, 2)
                        self.alpha_beta.emit([alpha, beta])
                        with open(self.__config_file, "w") as outfile:
                            yaml.dump(self.__configuration_view, outfile, default_flow_style=False)
                        self.create_maps_anypoint_mode_1()

                    else:
                        self.__configuration_view["Mode_2"]["coord"][0] = x
                        self.__configuration_view["Mode_2"]["coord"][1] = y
                        alpha, beta = self.__moildev.get_alpha_beta(x, y, 2)
                        if alpha is not None:
                            self.__configuration_view["Mode_2"]["pitch"] = round(alpha, 2)
                            self.__configuration_view["Mode_2"]["yaw"] = round(beta, 2)
                        self.alpha_beta.emit([alpha, beta])
                        with open(self.__config_file, "w") as outfile:
                            yaml.dump(self.__configuration_view, outfile, default_flow_style=False)
                        self.create_maps_anypoint_mode_2()

    def label_original_mouse_leave_event(self):
        """Handle the mouse leave event on the original image label.

        This method is called when the mouse leaves the original image label in the
        UI. It performs different actions depending on the current view state:
        - If the state is "AnypointView", it draws a crosshair on the original image
          and emits an alpha_beta signal with the calculated alpha and beta values
          based on the mode and configuration.
        - If the state is "PanoramaView", it draws a crosshair on the original image
          and emits an alpha_beta signal with the calculated alpha and beta values
          based on the mode and configuration.
        - Otherwise, it simply draws a crosshair on the current image.

        Returns:
            None
        """
        if self.image_resize is None:
            return

        if self.state_rubberband:
            return

        if self.load_saved_image:
            return

        if self.recenter_image_state:
            self.value_coordinate.emit([self.__configuration_view["Recenter_coord"][0],
                                        self.__configuration_view["Recenter_coord"][1]])

            icx = self.__configuration_view["Recenter_coord"][0]
            icy = self.__configuration_view["Recenter_coord"][1]
            alpha, beta = self.__moildev_recenter.get_alpha_beta(icx, icy)
            self.alpha_beta.emit([alpha, beta])

        else:
            if self.__state_view == "AnypointView":
                self.draw_crosshair_on_the_original_image(self.__image_original.copy())
                if self.change_anypoint_mode == "mode_1":
                    if self.__configuration_view["Mode_1"]["coord"][0] is None:
                        alpha, beta = 0, 0
                    else:
                        alpha, beta = self.__moildev.get_alpha_beta(
                            self.__configuration_view["Mode_1"]["coord"][0],
                            self.__configuration_view["Mode_1"]["coord"][1], 1)

                        self.value_coordinate.emit([self.__configuration_view["Mode_1"]["coord"][0],
                                                    self.__configuration_view["Mode_1"]["coord"][1]])
                else:
                    if self.__configuration_view["Mode_2"]["coord"][0] is None:
                        alpha, beta = 0, 0
                    else:
                        alpha, beta = self.__moildev.get_alpha_beta(
                            self.__configuration_view["Mode_2"]["coord"][0],
                            self.__configuration_view["Mode_2"]["coord"][1], 2)
                        self.value_coordinate.emit([self.__configuration_view["Mode_2"]["coord"][0],
                                                    self.__configuration_view["Mode_2"]["coord"][1]])
                self.alpha_beta.emit([alpha, beta])

            elif self.__state_view == "PanoramaView":
                self.draw_crosshair_on_the_original_image(self.__image_original.copy())
                if self.change_panorama_mode == "car":
                    if self.__configuration_view["Pano_car"]["coord"][0] is None:
                        alpha, beta = 0, 0
                    else:
                        alpha, beta = self.__moildev.get_alpha_beta(
                            self.__configuration_view["Pano_car"]["coord"][0],
                            self.__configuration_view["Pano_car"]["coord"][1], 1)
                        self.value_coordinate.emit([self.__configuration_view["Pano_car"]["coord"][0],
                                                    self.__configuration_view["Pano_car"]["coord"][1]])
                else:
                    alpha, beta = 0, 0
                    self.value_coordinate.emit([self.__moildev.icx, self.__moildev.icy])

                self.alpha_beta.emit([alpha, beta])

            else:
                self.draw_crosshair_on_the_original_image(self.image_resize.copy())
                if self.recenter_image_state:
                    self.value_coordinate.emit([self.__configuration_view["Recenter_coord"][0],
                                                self.__configuration_view["Recenter_coord"][1]])
                    alpha, beta = self.__moildev.get_alpha_beta(
                        self.__configuration_view["Recenter_coord"][0],
                        self.__configuration_view["Recenter_coord"][1], 1)
                    self.alpha_beta.emit([alpha, beta])

                else:
                    x = self.__moildev.icx
                    y = self.__moildev.icy
                    self.value_coordinate.emit([x, y])
                    self.alpha_beta.emit([0, 0])

    def label_original_mouse_double_click_anypoint_mode_1(self):
        """Handle double-click events on the original label image in Anypoint Mode 1.

        This function sets the Anypoint Mode 1 configuration values to their defaults and emits the `alpha_beta` signal with
        values `[0, 0]`. It then saves the new configuration to the configuration file and calls `create_maps_anypoint_mode_1()`
        to update the view.

        Args:
            self: The object itself, implicitly passed.

        Returns:
            None
        """
        self.__configuration_view["Mode_1"]["alpha"] = 0
        self.__configuration_view["Mode_1"]["beta"] = 0
        self.__configuration_view["Mode_1"]["zoom"] = 4
        self.__configuration_view["Mode_1"]["coord"][0] = self.__moildev.icx
        self.__configuration_view["Mode_1"]["coord"][1] = self.__moildev.icy
        if self.recenter_image_state:
            self.alpha_beta_in_recenter_image.emit([0, 0])
        else:
            self.alpha_beta.emit([0, 0])

        with open(self.__config_file, "w") as outfile:
            yaml.dump(self.__configuration_view, outfile, default_flow_style=False)
        self.create_maps_anypoint_mode_1()

    def label_original_mouse_double_click_anypoint_mode_2(self):
        """Resets the configuration view for Anypoint Mode 2 and emits alpha and beta values of [0, 0].

        Resets the pitch, roll, yaw, and zoom values to their default values, sets the coordinates of the view to the
        current image center, and saves the updated configuration to a file. Additionally, emits alpha and beta values
        of [0, 0] to signal that the view has been reset.
        """
        self.__configuration_view["Mode_2"]["pitch"] = 0
        self.__configuration_view["Mode_2"]["roll"] = 0
        self.__configuration_view["Mode_2"]["yaw"] = 0
        self.__configuration_view["Mode_2"]["zoom"] = 4
        self.__configuration_view["Mode_2"]["coord"][0] = self.__moildev.icx
        self.__configuration_view["Mode_2"]["coord"][1] = self.__moildev.icy
        if self.recenter_image_state:
            self.alpha_beta_in_recenter_image.emit([0, 0])
        else:
            self.alpha_beta.emit([0, 0])

        with open(self.__config_file, "w") as outfile:
            yaml.dump(self.__configuration_view, outfile, default_flow_style=False)
        self.create_maps_anypoint_mode_2()

    def label_original_mouse_press_event_anypoint_mode_1(self, event):
        """Updates the configuration view for the first mode when a mouse press event occurs.

        Args:
            event (QMouseEvent): The mouse press event.
        Returns:
            None.

        Raises:
            None.
        """
        try:
            pos_x = round(int(event.position().x()) * self.__ratio_x)
            pos_y = round(int(event.position().y()) * self.__ratio_y)
            self.__configuration_view["Mode_1"]["coord"][0] = pos_x
            self.__configuration_view["Mode_1"]["coord"][1] = pos_y
            alpha, beta = self.__moildev.get_alpha_beta(round(pos_x), round(pos_y), 1)
            self.alpha_beta.emit([alpha, beta])
            if alpha is not None:
                self.__configuration_view["Mode_1"]["alpha"] = round(alpha, 2)
                self.__configuration_view["Mode_1"]["beta"] = round(beta, 2)
            with open(self.__config_file, "w") as outfile:
                yaml.dump(self.__configuration_view, outfile, default_flow_style=False)

        except:
            pass

    def label_original_mouse_press_event_anypoint_mode_2(self, event):
        """Update configuration for Mode 2 when clicking on original image.

        Args:
            event: A QMouseEvent object representing the mouse press event.

        Returns:
            None.

        Raises:
            None.
        """
        pos_x = round(int(event.position().x()) * self.__ratio_x)
        pos_y = round(int(event.position().y()) * self.__ratio_y)
        self.__configuration_view["Mode_2"]["coord"][0] = round(pos_x)
        self.__configuration_view["Mode_2"]["coord"][1] = round(pos_y)
        alpha, beta = self.__moildev.get_alpha_beta(round(pos_x), round(pos_y), 2)
        self.alpha_beta.emit([alpha, beta])
        if alpha is not None:
            self.__configuration_view["Mode_2"]["pitch"] = round(alpha, 2)
            self.__configuration_view["Mode_2"]["yaw"] = round(beta, 2)
        with open(self.__config_file, "w") as outfile:
            yaml.dump(self.__configuration_view, outfile, default_flow_style=False)

    def label_original_recenter_mode(self, event):
        try:
            pos_x = round(int(event.position().x()) * self.__ratio_x)
            pos_y = round(int(event.position().y()) * self.__ratio_y)
            self.__configuration_view["Recenter_coord"][0] = round(pos_x)
            self.__configuration_view["Recenter_coord"][1] = round(pos_y)
            with open(self.__config_file, "w") as outfile:
                yaml.dump(self.__configuration_view, outfile, default_flow_style=False)

            self.create_maps_recenter()
            self.create_image_result()
        except:
            QMessageBox.warning(None, "Warning", "Can't process, the coordinate out of bound!!")

    def label_original_mouse_press_event_panorama_car(self, event):
        """Updates the configuration of the car panorama mode with the mouse press event.

        Args:
            event (QMouseEvent): The mouse press event.

        Returns:
            None.
        """
        pos_x = round(int(event.position().x()) * self.__ratio_x)
        pos_y = round(int(event.position().y()) * self.__ratio_y)
        self.__configuration_view["Pano_car"]["coord"][0] = round(pos_x)
        self.__configuration_view["Pano_car"]["coord"][1] = round(pos_y)

        alpha, beta = self.__moildev.get_alpha_beta(round(pos_x), round(pos_y), 1)
        if alpha is not None:
            self.__configuration_view["Pano_car"]["alpha"] = round(alpha, 2)
            self.__configuration_view["Pano_car"]["beta"] = round(beta, 2)
        with open(self.__config_file, "w") as outfile:
            yaml.dump(self.__configuration_view, outfile, default_flow_style=False)

    def label_recenter_mouse_move_event(self, label, event):
        if self.image_resize is None:
            return

        if self.state_rubberband:
            return

        if self.load_saved_image:
            return

        self.__ratio_x, self.__ratio_y = self.__model.calculate_ratio_image2label(label, self.image_resize)
        x = round(int(event.position().x()) * self.__ratio_x)
        y = round(int(event.position().y()) * self.__ratio_y)
        self.value_coordinate_in_recenter_image.emit([x, y])

        if event.buttons() == Qt.MouseButton.NoButton:
            if self.__state_view == "FisheyeView":
                image = self.__marker.point(self.rec_image.copy(), (x, y))
                self.recenter_image.emit(self.draw_crosshair_on_center_image(image))

            elif self.__state_view == "AnypointView":
                label.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
                if self.change_anypoint_mode == "mode_1":
                    alpha, beta = self.__moildev.get_alpha_beta(x, y, 1)
                else:
                    alpha, beta = self.__moildev.get_alpha_beta(x, y, 2)
                self.alpha_beta_in_recenter_image.emit([alpha, beta])

            else:
                alpha, beta = self.__moildev.get_alpha_beta(x, y, 1)
                self.alpha_beta_in_recenter_image.emit([alpha, beta])

    def label_recenter_mouse_leave_event(self):
        if self.image_resize is None:
            return

        if self.state_rubberband:
            return

        if self.load_saved_image:
            return

        if self.__state_view == "AnypointView":
            if self.change_anypoint_mode == "mode_1":
                if self.__configuration_view["Mode_1"]["coord"][0] is None:
                    alpha, beta = 0, 0
                else:
                    alpha = self.__configuration_view["Mode_1"]["alpha"]
                    beta = self.__configuration_view["Mode_1"]["beta"]
                    self.value_coordinate_in_recenter_image.emit([self.__configuration_view["Mode_1"]["coord"][0],
                                                                  self.__configuration_view["Mode_1"]["coord"][1]])
            else:
                if self.__configuration_view["Mode_2"]["coord"][0] is None:
                    alpha, beta = 0, 0
                else:
                    alpha = self.__configuration_view["Mode_2"]["pitch"]
                    beta = self.__configuration_view["Mode_2"]["yaw"]
                    self.value_coordinate_in_recenter_image.emit([self.__configuration_view["Mode_2"]["coord"][0],
                                                                  self.__configuration_view["Mode_2"]["coord"][1]])
            self.alpha_beta_in_recenter_image.emit([alpha, beta])

        elif self.__state_view == "PanoramaView":
            if self.change_panorama_mode == "car":
                if self.__configuration_view["Pano_car"]["coord"][0] is None:
                    alpha, beta = 0, 0
                else:
                    alpha = self.__configuration_view["Pano_car"]["alpha"]
                    beta = self.__configuration_view["Pano_car"]["beta"]
                    self.value_coordinate_in_recenter_image.emit([self.__configuration_view["Pano_car"]["coord"][0],
                                                                  self.__configuration_view["Pano_car"]["coord"][1]])
            else:
                alpha, beta = 0, 0

            self.alpha_beta_in_recenter_image.emit([alpha, beta])

        else:
            self.recenter_image.emit(self.draw_crosshair_on_center_image(self.rec_image.copy()))

    def label_recenter_mouse_press_event_anypoint_mode_1(self, event):
        """Updates the configuration view for the first mode when a mouse press event occurs.

        Args:
            event (QMouseEvent): The mouse press event.
        Returns:
            None.

        Raises:
            None.
        """
        try:
            pos_x = round(int(event.position().x()) * self.__ratio_x)
            pos_y = round(int(event.position().y()) * self.__ratio_y)
            self.__configuration_view["Mode_1"]["coord"][0] = pos_x
            self.__configuration_view["Mode_1"]["coord"][1] = pos_y
            alpha, beta = self.__moildev.get_alpha_beta(round(pos_x), round(pos_y), 1)
            self.alpha_beta_in_recenter_image.emit([alpha, beta])
            if alpha is not None:
                self.__configuration_view["Mode_1"]["alpha"] = round(alpha, 2)
                self.__configuration_view["Mode_1"]["beta"] = round(beta, 2)
            with open(self.__config_file, "w") as outfile:
                yaml.dump(self.__configuration_view, outfile, default_flow_style=False)

        except:
            pass

    def label_recenter_mouse_press_event_anypoint_mode_2(self, event):
        """Update configuration for Mode 2 when clicking on original image.

        Args:
            event: A QMouseEvent object representing the mouse press event.

        Returns:
            None.

        Raises:
            None.
        """
        pos_x = round(int(event.position().x()) * self.__ratio_x)
        pos_y = round(int(event.position().y()) * self.__ratio_y)
        self.__configuration_view["Mode_2"]["coord"][0] = round(pos_x)
        self.__configuration_view["Mode_2"]["coord"][1] = round(pos_y)
        alpha, beta = self.__moildev.get_alpha_beta(round(pos_x), round(pos_y), 2)
        self.alpha_beta_in_recenter_image.emit([alpha, beta])
        if alpha is not None:
            self.__configuration_view["Mode_2"]["pitch"] = round(alpha, 2)
            self.__configuration_view["Mode_2"]["yaw"] = round(beta, 2)
        with open(self.__config_file, "w") as outfile:
            yaml.dump(self.__configuration_view, outfile, default_flow_style=False)

    def label_result_mouse_press_event(self):
        """Mouse press event handler for the label displaying the image result.

        Does nothing if `self.image` is `None`.
        """
        if self.image_resize is not None:
            pass

    def mouse_press_event_handler_recenter(self, event):
        try:
            pos_x = round(int(event.position().x()) * self.__ratio_x)
            pos_y = round(int(event.position().y()) * self.__ratio_y)
            self.__configuration_view["Recenter_coord"][0] = round(pos_x)
            self.__configuration_view["Recenter_coord"][1] = round(pos_y)
            with open(self.__config_file, "w") as outfile:
                yaml.dump(self.__configuration_view, outfile, default_flow_style=False)
            self.create_maps_recenter()
            self.create_image_result()
        except:
            QMessageBox.warning(None, "Warning", "Can't process, the coordinate out of bound!!")

    def reset_coordinate_recenter_to_default(self):
        self.draw_crosshair_on_the_original_image(self.image_resize.copy())
        x = self.__moildev.icx
        y = self.__moildev.icy
        self.value_coordinate.emit([x, y])

    def update_properties_config_when_change_view_mode(self):
        if self.__state_view == "AnypointView":
            if self.change_anypoint_mode == "mode_1":
                if self.__configuration_view["Mode_1"]["coord"][0] is None:
                    alpha, beta = 0, 0
                    x, y = self.__moildev.icx, self.__moildev.icy
                else:
                    alpha, beta = self.__moildev.get_alpha_beta(
                        self.__configuration_view["Mode_1"]["coord"][0],
                        self.__configuration_view["Mode_1"]["coord"][1], 1)

                    x = self.__configuration_view["Mode_1"]["coord"][0]
                    y = self.__configuration_view["Mode_1"]["coord"][1]
            else:
                if self.__configuration_view["Mode_2"]["coord"][0] is None:
                    alpha, beta = 0, 0
                    x, y = self.__moildev.icx, self.__moildev.icy
                else:
                    alpha, beta = self.__moildev.get_alpha_beta(
                        self.__configuration_view["Mode_2"]["coord"][0],
                        self.__configuration_view["Mode_2"]["coord"][1], 2)
                    x = self.__configuration_view["Mode_2"]["coord"][0]
                    y = self.__configuration_view["Mode_2"]["coord"][1]

        elif self.__state_view == "PanoramaView":
            if self.change_panorama_mode == "car":
                if self.__configuration_view["Pano_car"]["coord"][0] is None:
                    alpha, beta = 0, 0
                    x, y = self.__moildev.icx, self.__moildev.icy
                else:
                    alpha, beta = self.__moildev.get_alpha_beta(
                        self.__configuration_view["Pano_car"]["coord"][0],
                        self.__configuration_view["Pano_car"]["coord"][1], 1)
                    x = self.__configuration_view["Pano_car"]["coord"][0]
                    y = self.__configuration_view["Pano_car"]["coord"][1]
            else:
                alpha, beta = 0, 0
                x, y = self.__moildev.icx, self.__moildev.icy

        else:
            alpha, beta = 0, 0
            x, y = self.__moildev.icx, self.__moildev.icy

        if self.recenter_image_state:
            self.value_coordinate_in_recenter_image.emit([x, y])
            self.alpha_beta_in_recenter_image.emit([alpha, beta])
        else:
            self.value_coordinate.emit([x, y])
            self.alpha_beta.emit([alpha, beta])

    def create_recenter_image(self):
        image = cv2.remap(self.image_resize.copy(), self.__map_recenter[0], self.__map_recenter[1], cv2.INTER_CUBIC)
        self.rec_image = cv2.remap(image, self.__map_recenter[2], self.__map_recenter[3], cv2.INTER_CUBIC)

    def create_maps_recenter(self, alpha=None, beta=None, reset=False):
        if alpha is None and beta is None:
            if reset:
                icx = self.__moildev_recenter.icx
                icy = self.__moildev_recenter.icy

            else:
                icx = self.__configuration_view["Recenter_coord"][0]
                icy = self.__configuration_view["Recenter_coord"][1]
            alpha, beta = self.__moildev_recenter.get_alpha_beta(icx, icy)
            self.alpha_beta.emit([alpha, beta])
        else:
            alpha = alpha
            beta = beta
        self.__map_recenter[0], self.__map_recenter[1] = self.__moildev_recenter.maps_panorama_rt(110, alpha, beta)
        self.__map_recenter[2], self.__map_recenter[3] = self.__moildev_recenter_a.maps_recenter(110, beta)

    @property
    def size_rubberband(self):
        """Returns the current size of the rubber band selection area.

        Returns:
            The size of the rubber band selection area.
        """
        return self.__size_rubberband

    @size_rubberband.setter
    def size_rubberband(self, size_rubberband):
        """Get the size of the rubberband.

        Returns:
            int: The size of the rubberband.
        """
        self.__size_rubberband = size_rubberband

    def crop_image(self, image_ori):
        """
        Crop the image according to the selected rubberband area.

        Args:
            image_ori (np.ndarray): Original image.

        Returns:
            None
        """
        image = self.convert_cv2_to_q_image(image_ori)
        height = self.__model.calculate_height(image_ori, self.__width_image_result)
        ratio_x = self.image_width / self.__width_image_result
        ratio_y = self.image_height / height
        x = int(self.size_rubberband.x() * ratio_x)
        y = int(self.size_rubberband.y() * ratio_y)
        width = int(self.size_rubberband.width() * ratio_x)
        height = int(self.size_rubberband.height() * ratio_y)
        rect = QRect(x, y, width, height)
        croppedImage = image.copy(rect)
        point_1 = (round(x), round(y))
        point_2 = (round(x + width), round(y + height))
        ori_image = self.image_resize.copy() if self.__state_view == "FisheyeView" else image_ori.copy()
        image = self.draw_rectangle(ori_image, point_1, point_2)
        self.signal_image_original.emit(image)
        self.image_result.emit(self.convert_q_image_to_mat(croppedImage))

    @classmethod
    def draw_rectangle(cls, image, point_1, point_2, thickness=5):
        """
        Draw rectangle on the image.

        Args:
            image (): input image
            point_1 (): the first point
            point_2 (): the second point to create rectangle
            thickness (): the thickness of rectangle line

        Returns:
            image with rectangle object
        """
        image = cv2.rectangle(image, point_1, point_2, (0, 0, 225), thickness)
        return image

    @classmethod
    def convert_cv2_to_q_image(cls, image):
        """ Convert an image from OpenCV format to Qt format.
        The function takes an image in OpenCV format and returns the equivalent image in Qt format.
        The image can be grayscale, RGB or RGBA. The conversion is done by creating a `QImage` object and setting
        the image data and format accordingly.

        Args:
            image (ndarray): The image in OpenCV format (height x width x channels)

        Returns:
            QImage: The image in Qt format
        """
        qim = QImage()
        if image is None:
            return qim
        if image.dtype == np.uint8:
            if len(image.shape) == 2:
                qim = QImage(image.data, image.shape[1], image.shape[0], image.strides[0],
                             QImage.Format.Format_Indexed8)
                qim.setColorTable([qRgb(i, i, i) for i in range(256)])
            elif image.shape[2] == 3:
                image = np.ascontiguousarray(image)
                qim = QImage(image.data, image.shape[1], image.shape[0], image.strides[0],
                             QImage.Format.Format_RGB888)
            elif image.shape[2] == 4:
                qim = QImage(image.data, image.shape[1], image.shape[0], image.strides[0],
                             QImage.Format.Format_ARGB32)
        return qim

    @classmethod
    def convert_q_image_to_mat(cls, q_image):
        """Converts a QImage to a NumPy array.

        Args:
            q_image: A QImage instance to be converted.

        Returns:
            A NumPy array with the image data.

        Raises:
            TypeError: If `q_image` is not a QImage instance.
        """
        incomingImage = q_image.convertToFormat(QImage.Format.Format_ARGB32)
        width = incomingImage.width()
        height = incomingImage.height()
        ptr = incomingImage.constBits()

        # https://blog.csdn.net/weixin_42670810/article/details/120683036
        ptr.setsize(incomingImage.bytesPerLine() * incomingImage.height())
        arr = np.array(ptr).reshape(height, width, 4)  # Copies the data
        return cv2.cvtColor(arr, cv2.COLOR_BGR2RGB)

    def set_alpha_beta(self, alpha, beta):
        """Set the values of alpha and beta and update the configuration file.

        Args:
            alpha (float): the alpha value to set.
            beta (float): the beta value to set.

        Returns:
            None.
        """
        if self.recenter_image_state:
            self.alpha_beta_in_recenter_image.emit([alpha, beta])
        else:
            self.alpha_beta.emit([alpha, beta])

        if self.change_anypoint_mode == "mode_1":
            self.__configuration_view["Mode_1"]["alpha"] = alpha
            self.__configuration_view["Mode_1"]["beta"] = beta

            if alpha == 75 and beta == 0:
                self.__configuration_view["Mode_1"]["coord"][1] = self.__moildev.icy - round(
                    self.__moildev.get_rho_from_alpha(alpha))
                self.__configuration_view["Mode_1"]["coord"][0] = round(
                    self.__moildev.get_rho_from_alpha(beta)) + self.__moildev.icx
            elif alpha == 75 and beta == 180:
                if any([alpha > 110, beta > 110]):
                    alpha = alpha - 110
                    beta = beta - 110
                self.__configuration_view["Mode_1"]["coord"][1] = self.__moildev.icy + round(
                    self.__moildev.get_rho_from_alpha(beta))
                self.__configuration_view["Mode_1"]["coord"][0] = self.__moildev.icx

            elif alpha == 0 and beta == 0:
                self.__configuration_view["Mode_1"]["coord"][1] = self.__moildev.icy
                self.__configuration_view["Mode_1"]["coord"][0] = self.__moildev.icx

            elif alpha == 75 and beta == -90:
                self.__configuration_view["Mode_1"]["coord"][0] = self.__moildev.icx - round(
                    self.__moildev.get_rho_from_alpha(alpha))
                self.__configuration_view["Mode_1"]["coord"][1] = self.__moildev.icy

            elif alpha == 75 and beta == 90:
                self.__configuration_view["Mode_1"]["coord"][0] = self.__moildev.icx + round(
                    self.__moildev.get_rho_from_alpha(alpha))
                self.__configuration_view["Mode_1"]["coord"][1] = self.__moildev.icy

        else:
            self.__configuration_view["Mode_2"]["pitch"] = alpha
            self.__configuration_view["Mode_2"]["yaw"] = beta
            if alpha == 75 and beta == 0:
                self.__configuration_view["Mode_2"]["coord"][1] = self.__moildev.icy - round(
                    self.__moildev.get_rho_from_alpha(alpha))
                self.__configuration_view["Mode_2"]["coord"][0] = round(
                    self.__moildev.get_rho_from_alpha(beta)) + self.__moildev.icx

            elif alpha == -75 and beta == 0:
                self.__configuration_view["Mode_2"]["coord"][1] = self.__moildev.icy + round(
                    self.__moildev.get_rho_from_alpha(abs(alpha)))
                self.__configuration_view["Mode_2"]["coord"][0] = self.__moildev.icx

            elif alpha == 0 and beta == 0:
                self.__configuration_view["Mode_2"]["coord"][1] = self.__moildev.icy
                self.__configuration_view["Mode_2"]["coord"][0] = self.__moildev.icx

            elif alpha == 0 and beta == -75:
                self.__configuration_view["Mode_2"]["coord"][0] = self.__moildev.icx - round(
                    self.__moildev.get_rho_from_alpha(abs(beta)))
                self.__configuration_view["Mode_2"]["coord"][1] = self.__moildev.icy

            elif alpha == 0 and beta == 75:
                self.__configuration_view["Mode_2"]["coord"][0] = self.__moildev.icx + round(
                    self.__moildev.get_rho_from_alpha(beta))
                self.__configuration_view["Mode_2"]["coord"][1] = self.__moildev.icy

        with open(self.__config_file, "w") as outfile:
            yaml.dump(self.__configuration_view, outfile, default_flow_style=False)

    def create_image_original(self):
        """
       This function creates the original image based on the configuration view.
       The function will check the type of media source specified in the configuration view,
       and proceed accordingly. The function can handle different types of media sources including a camera stream,
       a video file, or an image file. The function sets the video and image variables based on the media source.
       If the media source is a camera stream, the function will start a timer to capture frames.
       If the media source is a video file, the function will capture frames for the duration of the video.
       If the media source is an image file, the function will read the image into memory.

       Returns:
           None
       """
        if self.__configuration_view is not None and self.__configuration_view["Media_path"] is not None:
            self.__media_source = self.__configuration_view["Media_path"]
            source_type = self.__configuration_view['Source_type']
            cam_type = self.__configuration_view['Cam_type']

            try:
                if source_type == "Streaming Camera":
                    if cam_type in ["opencv_usb_cam", "opencv_ip_cam", "camera_url"]:
                        if os.name == 'nt':
                            if isinstance(self.__media_source, int):
                                self.cap = cv2.VideoCapture(self.__media_source, cv2.CAP_DSHOW)
                            else:
                                self.cap = cv2.VideoCapture(self.__media_source)
                        else:
                            self.cap = cv2.VideoCapture(self.__media_source)

                        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.__moildev.image_width)
                        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.__moildev.image_height)
                        self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('M', 'J', 'P', 'G'))
                        success, self.image = self.cap.read()
                        if success:
                            self.video = False
                            self.__raspi = False
                            self.calculate_resolution()
                            self.resize_image()
                            self.next_frame_signal()
                            self.timer.start()
                            self.timer_status.emit(self.timer.isActive())
                            self.recent_media_source.emit("streaming")
                            print("Streaming Camera USB Camera")

                    else:
                        self.cap = self.__model.moil_camera(
                            cam_type=self.__configuration_view["Cam_type"],
                            cam_id=self.__media_source,
                            resolution=(self.__moildev.image_width, self.__moildev.image_height))
                        print(f"here us from model apps, cam type is {self.__configuration_view['Cam_type']}")
                        self.video = False
                        self.__raspi = False
                        self.next_frame_signal()
                        self.timer.start()
                        self.timer_status.emit(self.timer.isActive())
                        self.recent_media_source.emit("streaming")
                        print("streaming camera usb camera")

                if source_type == "Image/Video":
                    if self.__media_source.endswith(('.mp4', '.MOV', '.avi')):
                        self.cap = cv2.VideoCapture(self.__media_source)
                        success, self.image = self.cap.read()
                        self.calculate_resolution()
                        self.resize_image()
                        self.video = True
                        self.__raspi = False
                        self.next_frame_signal()
                        self.timer.stop()
                        self.timer_status.emit(self.timer.isActive())
                        self.recent_media_source.emit("video")
                        self.__configuration_view["Cam_type"] = "video source"
                        print("video source")

                    elif self.__media_source.endswith(('.jpeg', '.JPG', '.jpg', '.png', 'TIFF')):
                        print("image source")
                        self.cap = None
                        self.video = False
                        self.__raspi = False
                        self.timer.stop()
                        self.image = cv2.imread(self.__media_source)
                        self.calculate_resolution()
                        self.resize_image()
                        self.create_image_result()
                        self.timer_status.emit(self.timer.isActive())
                        self.__configuration_view["Cam_type"] = "image source"
                        self.recent_media_source.emit("image")

                    else:
                        print("another source")

                self.config_view_info.emit(self.__configuration_view)

            except:
                QMessageBox.warning(None, "Warning", "Cant load the history, have error in media source\n"
                                                     "Please check that your camera is on plug or \n"
                                                     "the file is exist!. you can select new media source.")
                print("some error in media_source")

    def calculate_resolution(self):
        self.resolution_option = []
        if self.image is not None:
            for ratio in self.ratio_resize:
                self.resolution_option.append((int(self.image.shape[1] * ratio), int(self.image.shape[0] * ratio)))

    def create_image_result(self):
        """Create the result image based on the current view and configuration settings.

        If the `load_saved_image` flag is True, the function crops the original image based on the state of the
        `state_rubberband` flag. If it is False, the function checks the state of the `state_recent_view` flag and
        performs the following actions:
        - If the state is "AnypointView", it rotates the image by the `__angle_rotate` angle, and remaps the image
          based on the `__map_x_anypoint` and `__map_y_anypoint` maps. If `set_draw_polygon` is True, it draws a
          polygon on the original image using the same maps. It then sets `image_result` to the resulting image
          and sets `__image_original` to the original image with the crosshair drawn on it.
        - If the state is "PanoramaView", it rotates the image by the `__angle_rotate` angle, and remaps the image
          based on the `__map_x_pano` and `__map_y_pano` maps. If `change_panorama_mode` is "car", it crops the
          resulting image using the `__crop_panorama_car` method. Otherwise, it crops it using the `__crop_panorama_tube`
          method. If `set_draw_polygon` is True, it draws a polygon on the original image using the same maps. It then
          sets `image_result` to the resulting image and sets `__image_original` to the original image with the crosshair
          drawn on it.
        - If the state is not "AnypointView" or "PanoramaView", it rotates the image by the `__angle_rotate` angle and
          sets `image_result` to the resulting image. It then sets `__image_original` to the original image with the
          crosshair drawn on it.

        After creating the result image, the function emits a signal with the resulting image, and sets the `image_height`
        and `image_width` properties of the class.

        If the `state_rubberband` flag is True, the function calls the `crop_image` method on the resulting image, which
        will emit a signal with the cropped image.

        If the `load_saved_image` flag is False and the `state_rubberband` flag is False, the function emits a signal with
        the resulting image.
        """
        if self.load_saved_image and self.state_rubberband:
            self.crop_image(self.image_resize)
            return

        if self.recenter_image_state:
            self.create_recenter_image()
            if self.state_recent_view == "AnypointView":
                image_result = self.__model.remap_image(self.rec_image.copy(), self.__map_x_anypoint,
                                                        self.__map_y_anypoint)
                image_result = self.__model.rotate_image(image_result, self.__angle_rotate)

                if self.set_draw_polygon:
                    self.__image_original = self.__model.draw_polygon(self.rec_image.copy(), self.__map_x_anypoint,
                                                                      self.__map_y_anypoint)
                else:
                    self.__image_original = self.rec_image.copy()

                self.draw_crosshair_on_the_original_image(self.image_resize.copy())
                self.draw_crosshair_on_the_recenter_image(self.__image_original)

            elif self.state_recent_view == "PanoramaView":
                image_result = self.__model.remap_image(self.rec_image.copy(), self.__map_x_pano, self.__map_y_pano)
                image_result = self.__model.rotate_image(image_result, self.__angle_rotate)

                if self.change_panorama_mode == "car":
                    image_result = self.__crop_panorama_car(image_result)
                else:
                    image_result = self.__crop_panorama_tube(image_result)

                if self.set_draw_polygon:
                    self.__image_original = self.__model.draw_polygon(self.rec_image.copy(),
                                                                      self.__map_x_pano,
                                                                      self.__map_y_pano)
                else:
                    self.__image_original = self.rec_image.copy()

                self.draw_crosshair_on_the_original_image(self.image_resize.copy())
                self.draw_crosshair_on_the_recenter_image(self.__image_original)

            else:
                image_result = self.__model.rotate_image(self.rec_image, self.__angle_rotate)
                self.draw_crosshair_on_the_original_image(self.image_resize.copy())
                self.recenter_image.emit(self.draw_crosshair_on_center_image(self.rec_image.copy()))

            self.image_height, self.image_width = image_result.shape[:2]
            if self.state_rubberband:
                self.crop_image(image_result)
            else:
                self.image_result.emit(image_result)

        else:
            try:
                if self.state_recent_view == "AnypointView":
                    # self.image_resize = self.__model.rotate_image(self.image_resize.copy(), 35)
                    image_result = self.__model.remap_image(self.image_resize, self.__map_x_anypoint,
                                                            self.__map_y_anypoint)
                    image_result = self.__model.rotate_image(image_result, self.__angle_rotate)
                    if self.set_draw_polygon:

                        self.__image_original = self.__model.draw_polygon(self.__image_resize.copy(),
                                                                          self.__map_x_anypoint,
                                                                          self.__map_y_anypoint)

                    else:
                        self.__image_original = self.image_resize.copy()

                    self.draw_crosshair_on_the_original_image(self.__image_original.copy())

                elif self.state_recent_view == "PanoramaView":
                    image_result = self.__model.remap_image(self.image_resize, self.__map_x_pano, self.__map_y_pano)
                    image_result = self.__model.rotate_image(image_result, self.__angle_rotate)

                    if self.change_panorama_mode == "car":
                        image_result = self.__crop_panorama_car(image_result)
                    else:
                        image_result = self.__crop_panorama_tube(image_result)

                    if self.set_draw_polygon:
                        self.__image_original = self.__model.draw_polygon(self.image_resize.copy(),
                                                                          self.__map_x_pano,
                                                                          self.__map_y_pano)
                    else:
                        self.__image_original = self.image_resize.copy()
                    self.draw_crosshair_on_the_original_image(self.__image_original.copy())

                else:
                    image_result = self.__model.rotate_image(self.image_resize, self.__angle_rotate)
                    self.draw_crosshair_on_the_original_image(self.image_resize.copy())

                self.image_height, self.image_width = image_result.shape[:2]
                if self.state_rubberband:
                    self.crop_image(image_result)
                else:
                    self.image_result.emit(image_result)

            except:
                print("Parameter selected is not compatible with the source!")

    def record_video_pressed(self):
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        filename = "../saved_image/recorded_video_" + time.strftime("%Y%m%d_%H%M") + ".avi"
        if self.image is not None:
            h, w = self.image_resize.shape[:2]
            self.video_writer = cv2.VideoWriter(filename, fourcc, round(self.fps), (w, h))

    def finish_recording_video(self):
        self.video_writer = None

    def get_cr_left_right_panorama_car(self, pano_car):
        width1 = pano_car.shape[1] // 2
        width2 = pano_car.shape[1]
        height1 = pano_car.shape[0] / 2
        height1_min = int(height1 - 1)
        height2_max = int(height1_min + 1)
        coordinate = []
        for y in range(height1_min, height2_max):
            for x in range(0, width1):
                color = pano_car[y, x]
                if list(color) == [0, 255, 0]:
                    coordinate.append(x)

        coordinate2 = []
        for y in range(height1_min, height2_max):
            for x in range(width1, width2):
                color = pano_car[y, x]
                if list(color) == [0, 255, 0]:
                    coordinate2.append(x)

        self.__cr_left_car_color = (max(list(coordinate))) * 2
        self.__cr_right_car_color = (min(list(coordinate2))) * 2

    def create_maps_fov(self, alpha=110):
        if alpha > 10:
            moildev = self.__model.connect_to_moildev(parameter_name=self.parameter_name)
            self.maps_x_fov, self.maps_y_fov = moildev.maps_panorama_tube(10, alpha)
            # if self.__map_x_pano is not None and self.__map_y_pano is not None:
            # self.image_car_with_color_polygon()

    def draw_fov_original_image(self, image):
        return self.draw_polygon_fov(image, self.maps_x_fov, self.maps_y_fov)

    @staticmethod
    def draw_polygon_fov(image, mapX, mapY):
        """
        Return image with a drawn polygon on it from mapX and mapY generated by maps anypoint or panorama.

        Args:
            image: Original image
            mapX: map image X from anypoint process
            mapY: map image Y from anypoint process

        return:
            image: map x, map y

        - Example:

        .. code-block:: python

            image = draw_polygon(image,mapX,mapY)
        """
        hi, wi = image.shape[:2]
        X1 = []
        Y1 = []
        X2 = []
        Y2 = []
        X3 = []
        Y3 = []
        X4 = []
        Y4 = []

        x = 0
        while x < wi:
            a = mapX[0,]
            b = mapY[0,]
            ee = mapX[-1,]
            f = mapY[-1,]

            if a[x] == 0. or b[x] == 0.:
                pass
            else:
                X1.append(a[x])
                Y1.append(b[x])

            if f[x] == 0. or ee[x] == 0.:
                pass
            else:
                Y3.append(f[x])
                X3.append(ee[x])
            x += 10

        y = 0
        while y < hi:
            c = mapX[:, 0]
            d = mapY[:, 0]
            g = mapX[:, -1]
            h = mapY[:, -1]

            # eliminate the value 0 for map X
            if d[y] == 0. or c[y] == 0.:  # or d[y] and c[y] == 0.0:
                pass
            else:
                Y2.append(d[y])
                X2.append(c[y])

            # eliminate the value 0 for map Y
            if h[y] == 0. or g[y] == 0.:
                pass
            else:
                Y4.append(h[y])
                X4.append(g[y])

            # render every 10 times, it will be like 1, 11, 21 and so on.
            y += 10

        r = np.array([X3, Y3])
        points3 = r.T.reshape((-1, 1, 2))

        # Draw polyline on original image
        cv2.polylines(image, np.int32([points3]), False, (0, 255, 0), 10)
        return image

    def re_run_after_load_saved_image(self):
        """
        Performs necessary actions after loading a saved image, including updating the configuration file, resetting
        certain attributes, and creating the original and result images.

        Returns:
            None.
        """
        self.update_file_config()
        self.load_saved_image = False
        self.state_recent_view = "FisheyeView"
        if isinstance(self.__configuration_view["Media_path"], int):
            self.timer.start(round(1000 / self.fps))

        else:
            self.create_image_original()
            self.create_image_result()

        self.timer_status.emit(self.timer.isActive())

    def draw_crosshair_on_center_image(self, image):
        """
        Draws a crosshair in the center of the currently stored image.

        Returns:
            None.
        """
        x = self.__moildev.icx
        y = self.__moildev.icy
        image = self.__marker.crosshair(image, (x, y))
        return image

    def draw_crosshair_on_the_recenter_image(self, image):
        config = self.__load_config()
        if self.__state_view == "FisheyeView":
            if self.recenter_image_state:
                x = config["Recenter_coord"][0]
                y = config["Recenter_coord"][1]

            else:
                x = self.__moildev.icx
                y = self.__moildev.icy

        elif self.__state_view == "AnypointView":
            if self.change_anypoint_mode == "mode_1":
                if any([config["Mode_1"]["coord"][0] is None,
                        config["Mode_1"]["coord"][0] == 0]):
                    x = self.__moildev.icx
                    y = self.__moildev.icy
                else:
                    x = config["Mode_1"]["coord"][0]
                    y = config["Mode_1"]["coord"][1]

            else:
                if any([config["Mode_2"]["coord"][0] is None,
                        config["Mode_2"]["coord"][0] == 0]):
                    x = self.__moildev.icx
                    y = self.__moildev.icy
                else:
                    x = config["Mode_2"]["coord"][0]
                    y = config["Mode_2"]["coord"][1]
        else:
            if self.change_panorama_mode == "car":
                if any([config["Pano_car"]["coord"][0] is None,
                        config["Pano_car"]["coord"][0] == 0]):
                    x = self.__moildev.icx
                    y = self.__moildev.icy
                else:
                    x = config["Pano_car"]["coord"][0]
                    y = config["Pano_car"]["coord"][1]
            else:
                x = self.__moildev.icx
                y = self.__moildev.icy

        image = self.__marker.crosshair(image, (x, y))
        self.recenter_image.emit(image)

    def draw_crosshair_on_the_original_image(self, image):
        """
        Draws a crosshair on the specified `image` at a location determined by the current state of the object.

        Args:
            image: The image on which to draw the crosshair.

        Returns:
            None.
        """
        config = self.__load_config()
        if self.__state_view == "FisheyeView":
            if self.recenter_image_state:
                x = self.__configuration_view["Recenter_coord"][0]
                y = self.__configuration_view["Recenter_coord"][1]

            else:
                x = self.__moildev.icx
                y = self.__moildev.icy

        elif self.__state_view == "AnypointView":
            if self.change_anypoint_mode == "mode_1":
                if self.recenter_image_state:
                    x = self.__configuration_view["Recenter_coord"][0]
                    y = self.__configuration_view["Recenter_coord"][1]

                else:
                    if any([config["Mode_1"]["coord"][0] is None,
                            config["Mode_1"]["coord"][0] == 0]):
                        x = self.__moildev.icx
                        y = self.__moildev.icy
                    else:
                        x = config["Mode_1"]["coord"][0]
                        y = config["Mode_1"]["coord"][1]

            else:
                if self.recenter_image_state:
                    x = self.__configuration_view["Recenter_coord"][0]
                    y = self.__configuration_view["Recenter_coord"][1]

                else:
                    if any([config["Mode_2"]["coord"][0] is None,
                            config["Mode_2"]["coord"][0] == 0]):
                        x = self.__moildev.icx
                        y = self.__moildev.icy
                    else:
                        x = config["Mode_2"]["coord"][0]
                        y = config["Mode_2"]["coord"][1]
        else:
            if self.recenter_image_state:
                x = self.__configuration_view["Recenter_coord"][0]
                y = self.__configuration_view["Recenter_coord"][1]

            else:
                if self.change_panorama_mode == "car":
                    if any([config["Pano_car"]["coord"][0] is None,
                            config["Pano_car"]["coord"][0] == 0]):
                        x = self.__moildev.icx
                        y = self.__moildev.icy
                    else:
                        x = config["Pano_car"]["coord"][0]
                        y = config["Pano_car"]["coord"][1]
                else:
                    x = self.__moildev.icx
                    y = self.__moildev.icy

        image = self.__marker.crosshair(image, (x, y))
        self.signal_image_original.emit(image)

    @property
    def parameter_name(self):
        """
        Gets the value of the `__parameter_name` attribute.

        Returns:
            The value of the `__parameter_name` attribute.
        """
        return self.__parameter_name

    @parameter_name.setter
    def parameter_name(self, parameter):
        """
        Sets the value of the `__parameter_name` attribute to the specified `parameter`.

        Args:
            parameter: The new value for the `__parameter_name` attribute.

        Returns:
            None.
        """
        self.__parameter_name = parameter

    # Moildev Area +++++++++++++++++++++++++++
    def create_moildev(self, virtual_parameter=False):
        """
        Creates a connection to Moildev based on the configuration view.

        If the `__configuration_view` attribute is not `None`, the function checks if the `Parameter_name` value is not
        `None`. If this is the case, the function sets the `parameter_name` attribute to the value of
        `self.__configuration_view["Parameter_name"]`, and creates a connection to Moildev using the
        `self.__model.connect_to_moildev()` method and the `parameter_name` attribute. The function also sets the
        `pos_x` and `pos_y` attributes to the values of `self.__moildev.icx` and `self.__moildev.icy`, respectively.

        Returns:
            None.
        """
        if self.__configuration_view is not None:
            if self.__configuration_view["Parameter_name"] is not None:
                self.parameter_name = self.__configuration_view["Parameter_name"]
                if virtual_parameter:
                    self.__moildev = self.__model.connect_to_moildev(parameter_name=self.parameter_name,
                                                                     parameters_database=None,
                                                                     virtual_param=self.virtual_parameter)
                    # moildev = self.__model.connect_to_moildev(parameter_name=self.parameter_name,
                    #                                                              parameters_database=None,
                    #                                                              virtual_param=self.virtual_parameter)
                    self.__moildev_recenter = self.__model.connect_to_moildev(parameter_name=self.parameter_name,
                                                                              parameters_database=None,
                                                                              virtual_param=self.virtual_parameter)
                    self.__moildev_recenter_a = self.__model.connect_to_moildev(parameter_name=self.parameter_name,
                                                                                parameters_database=None,
                                                                                virtual_param=self.virtual_parameter)
                else:
                    self.__moildev = self.__model.connect_to_moildev(parameter_name=self.parameter_name)
                    # moildev = self.__model.connect_to_moildev(parameter_name=self.parameter_name)
                    self.__moildev_recenter = self.__model.connect_to_moildev(parameter_name=self.parameter_name)
                    self.__moildev_recenter_a = self.__model.connect_to_moildev(parameter_name=self.parameter_name)

                x = self.__moildev.icx
                y = self.__moildev.icy
                self.value_coordinate.emit([x, y])

    def recenter_image_process(self):
        try:
            if self.__configuration_view["Recenter_coord"][0] is not None:
                self.value_coordinate.emit([self.__configuration_view["Recenter_coord"][0],
                                            self.__configuration_view["Recenter_coord"][1]])
                self.create_maps_recenter()

            else:
                self.__configuration_view["Recenter_coord"][0] = round(self.__moildev.icx)
                self.__configuration_view["Recenter_coord"][1] = round(self.__moildev.icy)
                self.create_maps_recenter()
        except:
            self.__configuration_view["Recenter_coord"][0] = round(self.__moildev.icx)
            self.__configuration_view["Recenter_coord"][1] = round(self.__moildev.icy)
            self.create_maps_recenter()

    def change_coordinate_by_spinbox(self, icx, icy):
        try:
            self.__configuration_view["Recenter_coord"][0] = icx
            self.__configuration_view["Recenter_coord"][1] = icy
            self.create_maps_recenter()
            self.create_image_result()

        except:
            pass

    def change_alpha_beta_by_spinbox(self, alpha, beta):
        self.create_maps_recenter(alpha=alpha, beta=beta)
        self.create_image_result()

    # Anypoint area ++++++++++++++++++++++++++
    def create_maps_anypoint_mode_1(self):
        """
        Creates maps for anypoint mode 1 based on the configuration file.

        If the configuration file exists, the function loads the alpha, beta, and zoom values for mode 1 from the
        configuration file. It then uses the loaded values to create the maps for anypoint mode 1 using the
        `moildev.maps_anypoint_mode1()` method. If the `moildev` attribute is not `None`, the function also creates an
        image result using the `create_image_result()` method.

        Returns:
            None.
        """
        if os.path.exists(self.__config_file):
            config = self.__load_config()
            alpha = config["Mode_1"]["alpha"]
            beta = config["Mode_1"]["beta"]
            zoom = config["Mode_1"]["zoom"]
            if self.__moildev is not None:
                self.__map_x_anypoint, self.__map_y_anypoint = self.__moildev.maps_anypoint_mode1(alpha, beta, zoom)
                self.create_image_result()

    def create_maps_anypoint_mode_2(self):
        """
        Creates maps for anypoint mode 2 based on the configuration file.

        If the configuration file exists, the function loads the pitch, yaw, roll, and zoom values for mode 2 from the
        configuration file. It then uses the loaded values to create the maps for anypoint mode 2 using the
        `moildev.maps_anypoint_mode2()` method. If the `moildev` attribute is not `None`, the function also creates an
        image result using the `create_image_result()` method.

        Returns:
            None.
        """
        if os.path.exists(self.__config_file):
            config = self.__load_config()
            pitch = config["Mode_2"]["pitch"]
            yaw = config["Mode_2"]["yaw"]
            roll = config["Mode_2"]["roll"]
            zoom = config["Mode_2"]["zoom"]
            if self.__moildev is not None:
                self.__map_x_anypoint, self.__map_y_anypoint = self.__moildev.maps_anypoint_mode2(pitch, yaw, roll,
                                                                                                  zoom)
                self.create_image_result()

    # panorama area ++++++++++++++++++++++++++
    def reset_panorama_car(self):
        self.__configuration_view["Pano_car"]["alpha"] = 0
        self.__configuration_view["Pano_car"]["beta"] = 0
        self.__configuration_view["Pano_car"]["coord"][0] = self.__moildev.icx
        self.__configuration_view["Pano_car"]["coord"][1] = self.__moildev.icy
        self.alpha_beta.emit([0, 0])
        with open(self.__config_file, "w") as outfile:
            yaml.dump(self.__configuration_view, outfile, default_flow_style=False)
        self.create_maps_panorama_car()

    def create_maps_panorama_car(self):
        """Create the map images for the panorama car feature.

        This method creates the map images for the panorama car feature using the MOIL SDK. If the configuration file exists,
        it retrieves the alpha and beta values for the car from the configuration file using the private method __load_config().
        If the MOIL device object is not None, this method creates the map images for the panorama car feature using the alpha
        and beta values and sets the image result.

        Returns:
            None.
        """
        if os.path.exists(self.__config_file):
            config = self.__load_config()
            alpha = config["Pano_car"]["alpha"]
            beta = config["Pano_car"]["beta"]
            if self.__moildev is not None:
                # alpha_max = self.__moildev.camera_fov / 2
                alpha_max = 110
                self.__map_x_pano, self.__map_y_pano = self.__moildev.maps_panorama_car(alpha_max,
                                                                                        alpha, beta, 0, 1)
                # self.image_car_with_color_polygon()
                self.create_image_result()

    def image_car_with_color_polygon(self):
        image = self.draw_polygon_fov(self.image_resize.copy(), self.maps_x_fov, self.maps_y_fov)
        image_result = self.__model.remap_image(image, self.__map_x_pano, self.__map_y_pano)
        self.get_cr_left_right_panorama_car(image_result)

    def create_maps_panorama_tube(self):
        """
        Create the map images for the panorama tube feature.

        This method creates the map images for the panorama tube feature using the MOIL SDK. If the configuration file exists,
        it retrieves the minimum and maximum alpha values for the tube from the configuration file using the private method
        __load_config(). If the MOIL device object is not None, this method creates the map images for the panorama tube
        feature using the alpha values and sets the image result.

        Returns:
            None.
        """
        if os.path.exists(self.__config_file):
            config = self.__load_config()
            alpha_min = config["Pano_tube"]["alpha_min"]
            alpha_max = config["Pano_tube"]["alpha_max"]
            if self.__moildev is not None:
                self.__map_x_anypoint, self.__map_y_anypoint = self.__moildev.maps_panorama_tube(alpha_min, alpha_max)
                self.create_image_result()

    def __crop_panorama_car(self, image):
        """
        Crop the input image for the panorama car feature.

        This method crops the input image for the panorama car feature using the cropping parameters defined in the configuration
        file loaded through the private method __load_config(). It resizes the image to twice its original width, then crops the
        image using the crop_left, crop_right, crop_top, and crop_bottom parameters. The resulting image is then returned.

        Args:
            image: The input image to be cropped.

        Returns:
            The cropped image.
        """
        config = self.__load_config()
        crop_left = config["Pano_car"]["crop_left"]
        crop_right = config["Pano_car"]["crop_right"]
        crop_top = config["Pano_car"]["crop_top"]
        crop_bottom = config["Pano_car"]["crop_bottom"]

        image = cv2.resize(image, (image.shape[1] * 2, image.shape[0]))
        if self.__cr_left_car_color is not None and self.__cr_right_car_color is not None:
            image = image[0:image.shape[0], self.__cr_left_car_color:self.__cr_right_car_color]
            image = self.__model.cropping_image(image, 0, 1, crop_top, crop_bottom)

        else:
            image = self.__model.cropping_image(image, crop_left, crop_right, crop_top, crop_bottom)

        return image

    def __load_config(self):
        """Load the configuration file for the Panorama object.

        This method loads the configuration file for the Panorama object using the private attribute __config_file.
        The configuration file is read using the PyYAML library and the resulting dictionary is returned.

        Returns:
            A dictionary containing the configuration settings.
        """
        with open(self.__config_file, "r") as file:
            configuration_view = yaml.safe_load(file)
        return configuration_view

    def __crop_panorama_tube(self, image):
        """
        Crop the top and bottom of the input image based on configuration values.

        This method crops the top and bottom of the input image based on configuration values for the panorama tube
        feature. The crop values are retrieved from the configuration file using the private method __load_config().
        The cropped image is then returned.

        Args:
            image: The input image to crop.

        Returns:
            The cropped image.
        """
        config = self.__load_config()
        crop_top = config["Pano_tube"]["crop_top"]
        crop_bottom = config["Pano_tube"]["crop_bottom"]
        image = self.__model.cropping_image(image, 0, 1, crop_top, crop_bottom)
        return image

    # video controller +++++++++++++++++++++++
    def next_frame_signal(self):
        """Read the next frame from the video or camera and update the display.

        If the video capture object is not None and the video is currently playing, this method will:

        1. Read the next frame from the video.
        2. Update the position of the video player slider.
        3. Calculate the duration of the video in minutes and seconds.
        4. Calculate the current position of the video player in minutes and seconds.
        5. Emit a signal with the total duration of the video and the current position of the video player.

        If the video capture object is None or the video is not playing, this method will:

        1. Read the next frame from the camera.
        2. Update the display.
        3. Emit a signal with zeros for the duration and current position of the video player.

        Args:
            self: The VideoPlayer object.

        Returns:
            None
        """
        if self.cap is not None:
            start = time.time()
            if self.video:
                success, self.image = self.cap.read()
                self.resize_image()
                if success:
                    self.pos_frame = self.cap.get(cv2.CAP_PROP_POS_FRAMES)
                    self.total_frame = float(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
                    self.create_image_result()
                    self.set_slider_video_time_position()
                    duration_sec = int(self.total_frame / self.fps)
                    total_minutes = duration_sec // 60
                    duration_sec %= 60
                    total_seconds = duration_sec
                    sec_pos = int(self.pos_frame / self.fps)
                    recent_minute = int(sec_pos // 60)
                    sec_pos %= 60
                    recent_sec = sec_pos
                    self.timer_video_info.emit([total_minutes, total_seconds, recent_minute, recent_sec])

                else:
                    self.timer.stop()
                    self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.total_frame - 1)
                    _, self.image = self.cap.read()
                    self.resize_image()

            else:
                cam_type = self.__configuration_view['Cam_type']
                if cam_type in ["opencv_usb_cam", "opencv_ip_cam", "camera_url"]:
                    success, self.image = self.cap.read()
                else:
                    self.image = self.cap.frame()

                self.resize_image()
                self.create_image_result()
                self.timer_video_info.emit([0, 0, 0, 0])
                self.i_camera += 1

            total_time = time.time() - start
            self.fps = 1 / total_time

            if self.video_writer is not None:
                self.video_writer.write(self.image)

    def play_pause_video(self):
        """
        Toggle between playing and pausing the video.

        If the video player timer is currently active, this method will pause the video. If the timer is not active,
        the method will resume playing the video. Additionally, if the video player was previously displaying a saved
        image, the method will reset the player to resume playing the video.
        """
        if self.timer.isActive():
            self.timer.stop()
        else:
            self.load_saved_image = False
            self.timer.start(round(1000 / self.fps))

        self.timer_status.emit(self.timer.isActive())

    def stop_video(self):
        """Stop playing the video.

        If the video capture object is not None and the video is currently playing, this method will:

        1. Reset the video to the first frame.
        2. Stop the video player timer.
        3. Emit a signal to display the next frame.
        4. Emit a signal to update the timer status.

        Args:
            self: The VideoPlayer object.

        Returns:
            None
        """
        if self.cap is not None:
            if self.video:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                self.timer.stop()
                self.next_frame_signal()
                self.timer_status.emit(self.timer.isActive())

    def rewind_video_5_second(self):
        """Rewinds a video by 5 seconds from the current position.

        If a video is loaded, this function calculates the position of the video 5 seconds before the current position,
        and updates the video to that position. If the calculated position is before the beginning of the video, the
        function sets the video to the first frame. If no video is loaded, the function does nothing.

        Args:
            self: The instance of the class that this method belongs to.

        Returns:
            None.
        """
        if self.cap is not None:
            if self.video:
                position = self.pos_frame - 5 * self.fps
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, position)
                self.next_frame_signal()

    def forward_video_5_second(self):
        """Updates the position of a video based on the value of a slider widget.

        If a video is loaded, this function calculates the frame number corresponding to the value of a slider widget
        as a percentage of the total duration, and updates the video to that frame. If no video is loaded, the function
        does nothing.

        Args:
            self: The instance of the class that this method belongs to.
            value: The current value of the slider widget as an integer between 0 and 100.

        Returns:
            None.
        """
        if self.cap is not None:
            if self.video:
                position = self.pos_frame + 5 * self.fps
                if position > self.total_frame:
                    self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.total_frame - 1)
                else:
                    self.cap.set(cv2.CAP_PROP_POS_FRAMES, position)

                self.next_frame_signal()

    def slider_controller(self, value):
        if self.cap is not None:
            if self.video:
                dst_frame = self.total_frame * value / 100
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, dst_frame)
                self.next_frame_signal()

    def set_slider_video_time_position(self):
        """Sets the value of a slider widget based on the current position of a video.

        If a video is loaded, this function calculates the current time position as a percentage of the total duration
        and emits a signal with the corresponding value to update a slider widget. If no video is loaded, the function
        does nothing.

        Args:
            self: The instance of the class that this method belongs to.

        Returns:
            None.
        """
        if self.cap is not None:
            if self.video:
                dst_value = self.pos_frame * 100 / self.total_frame
                self.slider_time_value.emit(dst_value)

    def clear_saved_image(self):
        """Clear the saved image data from the configuration view and save the updated configuration to a file.

        This method removes all saved image data from the configuration view and updates the configuration file with the
        modified view.

        Args:
            self: The object instance.

        Returns:
            None.

        Raises:
            IOError: An error occurred while writing the updated configuration to the file.

        """
        self.__configuration_view["Image_saved"] = {}
        with open(self.__config_file, "w") as outfile:
            yaml.dump(self.__configuration_view, outfile, default_flow_style=False)

    def resize_image(self):
        if self.resolution_option:
            if self.image is not None:
                image = cv2.resize(self.image, self.resolution_option[self.resolution_active_index], cv2.INTER_AREA)
                self.image_resize = image
                if self.image_resize.shape[0] != self.__moildev.image_height:
                    self.create_virtual_parameter()

    def create_virtual_parameter(self):
        self.create_moildev()
        if self.resolution_active_index != 0:
            ratio = self.ratio_resize[self.resolution_active_index]
            self.virtual_parameter = {
                "cameraName": self.__moildev.camera_name,
                "cameraFov": self.__moildev.camera_fov,
                "cameraSensorWidth": self.__moildev.sensor_width,
                "cameraSensorHeight": self.__moildev.sensor_height,
                "iCx": int(self.__moildev.icx * ratio),
                "iCy": int(self.__moildev.icy * ratio),
                "ratio": self.__moildev.ratio,
                "imageWidth": int(self.__moildev.image_width * ratio),
                "imageHeight": int(self.__moildev.image_height * ratio),
                "calibrationRatio": self.__moildev.calibration_ratio,
                "parameter0": self.__moildev.param_0 * ratio,
                "parameter1": self.__moildev.param_1 * ratio,
                "parameter2": self.__moildev.param_2 * ratio,
                "parameter3": self.__moildev.param_3 * ratio,
                "parameter4": self.__moildev.param_4 * ratio,
                "parameter5": self.__moildev.param_5 * ratio
            }
            self.create_moildev(True)

    # Reset config to the default value ++++++
    def reset_config(self):
        """Resets the configuration view to its default values.

        This function sets all the fields of the configuration view to their default values,
        and saves the new configuration to the config file.

        Args:
            None

        Returns:
            None

        Raises:
            None
        """
        self.__configuration_view = {
            "Media_path": None,
            "Cam_type": None,
            "Parameter_name": None,
            "Recenter_coord": [None, None],
            "Mode_1": {
                "coord": [None, None],
                "alpha": 0,
                "beta": 0,
                "zoom": 4
            },
            "Mode_2": {
                "coord": [None, None],
                "pitch": 0,
                "yaw": 0,
                "roll": 0,
                "zoom": 4
            },
            "Pano_tube": {
                "alpha_min": 8,
                "alpha_max": 110,
                "crop_top": 0,
                "crop_bottom": 1
            },
            "Pano_car": {
                "coord": [None, None],
                "alpha": 0,
                "beta": 0,
                "crop_left": 0,
                "crop_right": 1,
                "crop_top": 0,
                "crop_bottom": 1
            },
            "Image_saved": {}
        }

        with open(self.__config_file, "w") as outfile:
            yaml.dump(self.__configuration_view, outfile, default_flow_style=False)

    def github_information(self):
        """Fetches information about the GitHub repository.

        Returns:
            Tuple: A tuple containing the `git.Repo` object for the repository and a dictionary with the following keys:
                - 'origin_url': The URL of the repository's origin.
                - 'user_name': The username of the repository's owner.
                - 'active_branch': The name of the currently active branch.
                - 'list_branch': A list of the repository's branch names.
                - 'token': The personal access token (PAT) used to authenticate with the repository, or `None` if no PAT is specified.

        Raises:
            None.
        """
        path_file = os.path.normpath(os.getcwd() + os.sep + os.pardir).replace("\\", "/")
        __cached_file = path_file + "/src/models/cached/github_config.yaml"
        path_file = os.path.dirname(os.path.realpath(__file__ + "/../.."))
        self.repo_github = git.Repo(path_file)

        if not os.path.exists(__cached_file):
            list_branch = []
            for branch in self.repo_github.heads:
                list_branch.append(str(branch))
            user_name = re.search('.com/(.*)/moilapp', self.repo_github.remotes.origin.url)
            token = None
            if user_name is not None:
                user_name = user_name.group(1)
                token = re.search(f'https://{user_name}:(.*)@github.com/', self.repo_github.remotes.origin.url)
                if token is not None:
                    token = token.group(1)

            github_config = {"origin_url": self.repo_github.remotes.origin.url,
                             "user_name": user_name,
                             "active_branch": str(self.repo_github.active_branch),
                             "list_branch": list_branch,
                             "token": token}

            with open(__cached_file, "w") as outfile:
                yaml.dump(github_config, outfile, default_flow_style=False)

        with open(__cached_file, "r") as file:
            configuration_github = yaml.safe_load(file)
        self.git_repository_info.emit(configuration_github)
        return self.repo_github, configuration_github

    def refresh_github_information(self):
        """Refreshes the GitHub repository information and emits the updated configuration.

        Reads the cached GitHub configuration from the file system and updates it with the latest
        information from the remote repository. The list of branches is obtained from the repository,
        and the `list_branch` property in the cached configuration is updated. If a token is present
        in the configuration, the remote repository is fetched using the token. Finally, the updated
        configuration is emitted using the `git_repository_info` signal.

        Returns:
            None
        """
        path_file = os.path.normpath(os.getcwd() + os.sep + os.pardir)
        __cached_file = path_file + "/src/models/cached/github_config.yaml"
        with open(__cached_file, "r") as file:
            configuration_github = yaml.safe_load(file)

        list_branch = []
        for branch in self.repo_github.remote().refs:
            if str(branch) == "origin/HEAD":
                pass
            else:
                list_branch.append(str(branch).split("/")[1])

        configuration_github["list_branch"] = list_branch
        if configuration_github["token"] is not None:
            self.repo_github.remotes.origin.fetch()
            self.git_repository_info.emit(configuration_github)
            with open(__cached_file, "w") as outfile:
                yaml.dump(configuration_github, outfile, default_flow_style=False)

    def change_config_github(self, token=None, branch=None):
        """Change the configuration for the GitHub repository.

        Args:
            token (str, optional): The access token to use when connecting to the
                GitHub repository. If provided, the function will update the
                configuration file with the new token. Defaults to None.
            branch (str, optional): The name of the active branch to use. If
                provided, the function will update the configuration file with
                the new branch name. Defaults to None.

        Returns:
            None

        Raises:
            None

        The function loads the current configuration for the GitHub repository
        from a YAML file, updates it with the provided token and/or branch name,
        and writes it back to the file. If a token is provided and the current
        repository URL does not include the token, the function updates the
        repository URL with the new token. Finally, the function emits a signal
        with the updated configuration.
        """
        cached_file = os.path.normpath(os.path.join(os.getcwd(), os.pardir, "src/models/cached/github_config.yaml"))
        with open(cached_file, "r") as file:
            configuration = yaml.safe_load(file)

        if token:
            configuration["token"] = token

        if configuration["token"] is not None:
            check_token = re.search(configuration["token"], self.repo_github.remotes.origin.url)
            if check_token is None:
                remote_url = re.sub('https://', f"https://{configuration['user_name']}:{token}@",
                                    configuration['origin_url'])
                self.repo_github.remotes["origin"].set_url(remote_url)
                configuration["origin_url"] = self.repo_github.remotes.origin.url

        if branch:
            configuration["active_branch"] = branch

        with open(cached_file, "w") as outfile:
            yaml.dump(configuration, outfile, default_flow_style=False)

        self.git_repository_info.emit(configuration)
