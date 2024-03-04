# import necessary library you used here
import sys
from datetime import datetime
from subprocess import call, STDOUT
import os
import cv2
import webbrowser
import requests
import git
import yaml
from PyQt6 import QtCore, QtGui, QtWidgets

from .control_main_ui_apps import ControlApps
from .control_setup_icon import SetIconsUI
from .control_plugin_manager import PluginManager
from .control_result_image import ControlResultImage
from .control_anypoint import AnypointConfig
from .control_panorama import PanoramaConfig
from .control_config_file import ConfigFileApps
from src.models.model_apps import ModelApps


class Controller(QtWidgets.QMainWindow):
    def __init__(self, ui, model, *args, **kwargs):

        """
        Initialize the MoilApp GUI.

        Args:
            ui: The user interface for the MoilApp.
            model: The model representing the MoilApp.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            None
        """
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.ui = ui
        self.ui.setupUi(self)
        self.model = model
        self.model_apps = ModelApps()
        self.ctrl_apps = ControlApps(self.ui)
        self.ctrl_icon = SetIconsUI(self.ui)
        self.ctrl_icon.get_theme_main_apps(self.model.theme)
        self.ctrl_plugin = PluginManager(self)
        self.ctrl_config = ConfigFileApps(self.ui)
        self.model_apps.update_file_config()
        self.ctrl_result_image = ControlResultImage()
        self.anypoint_config = AnypointConfig(self.ui)
        self.panorama_config = PanoramaConfig(self.ui)

        self.__width_image_result = self.round_to_nearest_100(self.ui.scrollArea.width())
        self.__angle_image_result = 0
        self.__image_result = None
        self.__dir_save = None
        self.__base_dir_save = None
        self.__data_github = None

        self.__plugins_list = None
        self.repository_plugin_store_branch = "main"

        # add new widget #########################################
        self.add_full_screen_window_show_result()
        self.full_screen_mode = False
        # self.width_full_screen_mode = self.round_to_nearest_100(self.new_window.width())

        self.ui.label_logo.mousePressEvent = self.mouse_event_in_moil_logo
        self.ui.delete_plugins_button.hide()
        self.ui.close_plugin_button.hide()

        self.ui.widget_container_content.setCurrentIndex(0)
        self.ui.widget_mode_view.hide()
        self.ui.frame_recenter_image.hide()
        self.ui.frame_pointer_in_recenter_frame.hide()

        self.ui.frame_4.hide()
        self.ui.frame_7.hide()

        self.ui.spinBox_icx.setEnabled(False)
        self.ui.spinBox_icy.setEnabled(False)
        self.ui.doubleSpinBox_alpha_rec.setEnabled(False)
        self.ui.doubleSpinBox_beta_rec.setEnabled(False)

        self.onclick_change_theme_apps()

        # property anypoint mode 1
        self.ui.label_6.hide()
        self.ui.doubleSpinBox_roll.hide()

        self.ui.label_plugin_name.hide()
        self.ui.open_in_new_window_plugins.hide()

        # property panorama tube
        self.ui.frame_panorama_tube_config.hide()

        self.ui.add_plugins_button.show()

        self.setWindowTitle("Moilapps - v4.1.0")

        self.model_apps.recent_media_source.connect(self.control_video_controller)
        self.model_apps.signal_image_original.connect(self.show_image_original)
        self.model_apps.image_result.connect(self.get_image_result)
        self.model_apps.alpha_beta.connect(self.alpha_beta_from_coordinate)
        self.model_apps.alpha_beta_in_recenter_image.connect(self.alpha_beta_from_coordinate_recenter_image)
        self.model_apps.slider_time_value.connect(self.set_slider_position)
        self.model_apps.timer_video_info.connect(self.show_timer_video_info)
        self.model_apps.timer_status.connect(self.onclick_play_pause_video)
        self.model_apps.git_repository_info.connect(self.showing_git_repository_information)
        self.model_apps.config_view_info.connect(self.show_config_view_in_information)
        self.model_apps.recenter_image.connect(self.show_recenter_image)
        self.model_apps.value_coordinate.connect(self.set_value_coordinate)
        self.model_apps.value_coordinate_in_recenter_image.connect(self.set_value_coordinate_in_recenter_image)
        self.model_apps.create_moildev()
        self.model_apps.create_image_original()
        self.set_resolution_sources()

        if self.__image_result is not None:
            self.ui.btn_fisheye_view.setStyleSheet(self.set_style_selected_menu())
            self.load_saved_image_list(load=True)

        if not call(["git", "branch"], stderr=STDOUT, stdout=open(os.devnull, 'w')) != 0:
            self.model_apps.github_information()

        self.show_general_information()

        # pin plugin to open
        file_path = os.path.join(os.getcwd(), "models", "cached", "plugin_cached.yaml")
        with open(file_path, "r") as file:
            config = yaml.safe_load(file)
        if config["plugin_run"] is not None:
            self.ctrl_plugin.open_pinned_plugin(config["plugin_run"])
            self.ui.add_plugins_button.hide()

        # connect event to button
        self.connect_event()

    def connect_event(self):
        """
        Connects all the events and signals to their respective functions.

        Args:
        self: An instance of the class.

        Returns:
            None
        """
        # control full screen
        self.spinBox_fov_full_screen.valueChanged.connect(self.control_fov_full_screen)
        self.new_window.resizeEvent = self.resize_event_new_window
        self.label_full_screen.mouseDoubleClickEvent = self.label_full_screen_double_click_event

        # control maoil app main
        self.rubberband = QtWidgets.QRubberBand(QtWidgets.QRubberBand.Shape.Rectangle, self.ui.label_result)
        self.setMouseTracking(True)

        shortcut = QtGui.QShortcut(QtCore.Qt.Key.Key_Escape, self)
        shortcut.activated.connect(self.escape_event)

        self.ui.label_image_original.mouseReleaseEvent = self.label_original_mouse_release_event
        self.ui.label_image_original.mouseMoveEvent = self.label_original_mouse_move_event
        self.ui.label_image_original.mousePressEvent = self.label_original_mouse_press_event
        self.ui.label_image_original.leaveEvent = self.label_original_mouse_leave_event
        self.ui.label_image_original.mouseDoubleClickEvent = self.label_original_mouse_double_click_event

        self.ui.label_image_recenter.mousePressEvent = self.label_recenter_mouse_press_event
        self.ui.label_image_recenter.mouseMoveEvent = self.label_recenter_mouse_move_event
        self.ui.label_image_recenter.leaveEvent = self.label_recenter_mouse_leave_event
        self.ui.label_image_recenter.mouseDoubleClickEvent = self.label_original_mouse_double_click_event

        self.ui.label_result.mouseDoubleClickEvent = self.label_result_mouse_double_click
        self.ui.label_result.mousePressEvent = self.label_result_mouse_press_event
        self.ui.label_result.mouseMoveEvent = self.label_result_mouse_move_event
        self.ui.label_result.mouseReleaseEvent = self.label_result_mouse_release_event

        self.ui.listWidget_saved_image.itemPressed.connect(self.list_widget_saved_image_activated)
        self.ui.pushButton.clicked.connect(self.onclick_clear_button_list_saved_image)

        self.ui.btn_record_screen.clicked.connect(self.onclick_record_screen)

        self.ui.extra_left_close_button.clicked.connect(self.close_setting_window)
        self.ui.comboBox.activated.connect(self.combo_box_change_branch)
        self.ui.btn_refresh_github.clicked.connect(self.onclick_refresh_github_repository)
        self.ui.btn_change_branch.clicked.connect(self.onclick_btn_change_branch)
        self.ui.pushButton_update.clicked.connect(self.check_for_update)
        self.ui.pushButton_commit_now.clicked.connect(self.onclick_commit_now)

        self.ui.btn_change_theme.clicked.connect(self.onclick_change_theme_apps)
        self.ui.btn_togle_menu.clicked.connect(self.onclick_button_menu)
        self.ui.btn_setting.clicked.connect(self.onclick_button_setting_menu)
        self.ui.btn_about_us.clicked.connect(self.onclick_button_about_us)
        self.ui.btn_open_media.clicked.connect(self.onclick_btn_open_media)
        self.ui.btn_form_params.clicked.connect(self.model.form_camera_parameter)
        self.ui.btn_fisheye_view.clicked.connect(self.onclick_btn_fisheye)
        self.ui.btn_anypoint_view.clicked.connect(self.onclick_btn_anypoint)
        self.ui.btn_panorama_view.clicked.connect(self.onclick_btn_panorama)
        self.ui.btn_clear_ui.clicked.connect(self.onclick_clear_user_interface)
        self.ui.github_button.clicked.connect(self.onclick_btn_github)
        self.ui.btn_read_the_docs.clicked.connect(self.read_the_documentation)
        self.ui.btn_check_update.clicked.connect(self.check_for_update)
        self.ui.check_draw_poligon.stateChanged.connect(self.change_polygon_state)

        self.ui.check_draw_poligon_pano.stateChanged.connect(self.change_polygon_state)

        self.ui.screenshoot_button.clicked.connect(lambda: self.save_image(True))
        self.ui.record_button.clicked.connect(self.onclick_record_video_button)

        self.ui.zoom_in_button.clicked.connect(lambda: self.zoom_image("zoom_in"))
        self.ui.zoom_out_button.clicked.connect(lambda: self.zoom_image("zoom_out"))
        self.ui.spinBox_zooming.valueChanged.connect(self.control_change_zooming)

        self.ui.rotate_left_button.clicked.connect(lambda: self.rotate_image("left"))
        self.ui.rotate_right_button.clicked.connect(lambda: self.rotate_image("right"))
        self.ui.doubleSpinBox_rotate.valueChanged.connect(self.rotation_change_value)
        self.ui.reset_view_button.clicked.connect(self.reset_view_back_to_original)

        self.ui.radio_mode_1.toggled.connect(self.change_mode_anypoint)
        self.ui.radio_mode_2.toggled.connect(self.change_mode_anypoint)

        self.ui.checkBox_reverse_view.toggled.connect(self.activate_change_optical_point)

        self.ui.doubleSpinBox_alpha.valueChanged.connect(self.change_properties_anypoint)
        self.ui.doubleSpinBox_beta.valueChanged.connect(self.change_properties_anypoint)
        self.ui.doubleSpinBox_roll.valueChanged.connect(self.change_properties_anypoint)
        self.ui.doubleSpinBox_zoom.valueChanged.connect(self.change_properties_anypoint)

        self.ui.radioButton_car.toggled.connect(self.change_mode_panorama)
        self.ui.radioButton_tube.toggled.connect(self.change_mode_panorama)

        self.ui.doubleSpinBox_pano_car_alpha.valueChanged.connect(self.change_properties_panorama)
        self.ui.doubleSpinBox_pano_car_beta.valueChanged.connect(self.change_properties_panorama)

        self.ui.doubleSpinBox_pano_car_crop_left.valueChanged.connect(self.change_properties_crop_panorama)
        self.ui.doubleSpinBox_pano_car_crop_right.valueChanged.connect(self.change_properties_crop_panorama)
        self.ui.doubleSpinBox_pano_car_crop_top.valueChanged.connect(self.change_properties_crop_panorama)
        self.ui.doubleSpinBox_pano_car_crop_bottom.valueChanged.connect(self.change_properties_crop_panorama)

        self.ui.doubleSpinBox_pano_tube_alpha_min.valueChanged.connect(self.change_properties_panorama)
        self.ui.doubleSpinBox_pano_tube_alpha_max.valueChanged.connect(self.change_properties_panorama)

        self.ui.doubleSpinBox_pano_tube_crop_top.valueChanged.connect(self.change_properties_crop_panorama)
        self.ui.doubleSpinBox_pano_tube_crop_buttom.valueChanged.connect(self.change_properties_crop_panorama)

        self.ui.pushButton_any_up.clicked.connect(self.onclick_anypoint)
        self.ui.pushButton_any_left.clicked.connect(self.onclick_anypoint)
        self.ui.pushButton_any_center.clicked.connect(self.onclick_anypoint)
        self.ui.pushButton_any_bottom.clicked.connect(self.onclick_anypoint)
        self.ui.pushButton_any_right.clicked.connect(self.onclick_anypoint)

        self.ui.spinBox_icx.valueChanged.connect(self.change_coordinate_optical_point)
        self.ui.spinBox_icy.valueChanged.connect(self.change_coordinate_optical_point)

        self.ui.doubleSpinBox_alpha_rec.valueChanged.connect(self.change_alpha_beta_optical_point)
        self.ui.doubleSpinBox_beta_rec.valueChanged.connect(self.change_alpha_beta_optical_point)

        self.ui.play_pause_button.clicked.connect(self.onclick_play_pause_video_button)
        self.ui.stop_button.clicked.connect(self.model_apps.stop_video)
        self.ui.rewind_button.clicked.connect(self.model_apps.rewind_video_5_second)
        self.ui.forward_button.clicked.connect(self.model_apps.forward_video_5_second)
        self.ui.slider_video_time.valueChanged.connect(self.model_apps.slider_controller)

        self.ui.add_plugins_button.clicked.connect(self.onclick_show_moilapp_plugin_store)
        self.ui.pushButton_close_plugin_store.clicked.connect(self.onclick_close_plugin_store)

        self.ui.btn_help.clicked.connect(self.onclick_help_button)

        self.ui.comboBox_resolution_sources.currentIndexChanged.connect(self.change_resolution_sources)

    def change_resolution_sources(self):
        self.model_apps.resolution_active_index = self.ui.comboBox_resolution_sources.currentIndex()
        self.model_apps.resize_image()
        if self.ui.checkBox_reverse_view.isChecked():
            self.model_apps.create_maps_recenter(reset=True)
        if self.model_apps.state_recent_view == "PanoramaView":
            self.change_properties_panorama()
        elif self.model_apps.state_recent_view == "AnypointView":
            self.change_properties_anypoint()

    def add_full_screen_window_show_result(self):
        self.new_window = QtWidgets.QWidget()
        self.new_window.setWindowTitle("Full Screen Window")

        self.new_window.setMinimumSize(QtCore.QSize(800, 600))
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.new_window)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.scrollArea = QtWidgets.QScrollArea(self.new_window)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 962, 598))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.scrollAreaWidgetContents)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_full_screen = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding,
                                           QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_full_screen.sizePolicy().hasHeightForWidth())
        self.label_full_screen.setSizePolicy(sizePolicy)
        self.label_full_screen.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.label_full_screen.setText("")
        self.label_full_screen.setObjectName("label_full_screen")

        self.label_full_screen_origin_image = QtWidgets.QLabel(self.scrollArea)
        self.label_full_screen_origin_image.setGeometry(5, 5, 320, 240)
        self.label_full_screen_origin_image.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.label_full_screen_origin_image.setText("")
        self.label_full_screen_origin_image.setObjectName("label_full_screen_origin_image")

        self.label_fff = QtWidgets.QLabel(self.scrollArea)
        self.label_fff.setGeometry(QtCore.QRect(10, 11, 60, 30))
        self.label_fff.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_fff.setStyleSheet("background-color: rgb(255,255,255);"
                                     "color: rgb(30 31 34);"
                                     "font-family: 'Segoe UI';"
                                     "font-size: 12px;")
        self.label_fff.setText("FoV Line: ")

        self.spinBox_fov_full_screen = QtWidgets.QSpinBox(self.scrollArea)
        self.spinBox_fov_full_screen.setGeometry(QtCore.QRect(10, 39, 60, 30))
        self.spinBox_fov_full_screen.setMinimumSize(QtCore.QSize(50, 30))
        self.spinBox_fov_full_screen.setMaximum(110)
        self.spinBox_fov_full_screen.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.spinBox_fov_full_screen.setSuffix("°")
        self.spinBox_fov_full_screen.setProperty("value", 110)

        self.horizontalLayout_3.addWidget(self.label_full_screen)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.horizontalLayout.addWidget(self.scrollArea)
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.new_window.setLayout(self.horizontalLayout)
        self.showMaximized()

    def label_full_screen_double_click_event(self, event):
        self.show()
        self.new_window.hide()
        self.full_screen_mode = False
        self.show_image_result()

    def control_fov_full_screen(self):
        self.model_apps.create_maps_fov(self.spinBox_fov_full_screen.value())

    def back_to_moil_apps(self):
        self.show()
        self.new_window.hide()
        self.full_screen_mode = False
        self.show_image_result()

    def showing_new_window_full_screen(self):
        self.hide()
        self.new_window.showMaximized()
        self.new_window.show()
        self.full_screen_mode = True
        self.show_image_result()

    def resize_event_new_window(self, a0: QtGui.QResizeEvent) -> None:
        self.show_image_result()

    def show_general_information(self):
        """
        Show general information on the user interface

        Returns:
            None
        """
        _time = datetime.now()
        _time = _time.strftime("%H:%M:%S")
        self.ui.label_info_time_running_apps.setText(_time)
        self.ui.label_info_who_the_user.setText(os.environ.get('USERNAME'))

    def onclick_show_moilapp_plugin_store(self):
        self.get_list_plugins()

    def get_list_plugins(self):
        if self.__data_github["token"] is None:
            if self.show_update_dialog(
                    "No token found, input your token?") == QtWidgets.QMessageBox.StandardButton.Yes:
                if self.open_dialog_for_input_token():
                    access_token = self.__data_github["token"]

                else:
                    return

        else:
            access_token = self.__data_github["token"]

        try:
            url = f'https://api.github.com/repos/perseverance-tech-tw/moilapp-plugins-store/contents?ref=' \
                  f'{self.repository_plugin_store_branch}'

            headers = {'Authorization': f'token {access_token}'}
            response = requests.get(url, headers=headers)
            file_names = [file['name'] for file in response.json() if file['size'] == 0]
            self.__plugins_list = file_names
            self.ui.stackedWidget_2.setCurrentIndex(1)

        except:
            QtWidgets.QMessageBox.information(None, "Information", "Connection Error or repository not found!!!")
            return

        self.clear_item_layout()

        sys.path.append(os.path.dirname(__file__))
        installed_apps = os.listdir("plugins")
        for i in range(len(self.__plugins_list)):
            item_widget = QtWidgets.QWidget()
            tupleName = os.path.splitext(self.__plugins_list[i])
            name = tupleName[0].replace('moilapp-plugin-', '')
            name = name.replace('_', ' ')
            name = (name.replace('-', ' ')).title()
            line_text = QtWidgets.QLabel(name)
            if tupleName[0] in installed_apps:
                line_push_button = QtWidgets.QPushButton("Remove")
                style = self.stylesheet_button_install_plugin("remove")
                line_push_button.clicked.connect(self.clicked_plugin_remove)
            else:
                line_push_button = QtWidgets.QPushButton("Install")
                style = self.stylesheet_button_install_plugin("install")
                line_push_button.clicked.connect(self.clicked_install_plugins)
            line_push_button.setAccessibleName(tupleName[0])
            line_push_button.setStyleSheet(style)
            line_push_button.setObjectName(str(i))
            line_push_button.setMaximumWidth(70)
            line_push_button.setMinimumWidth(70)
            line_push_button.setMinimumHeight(30)

            item_layout = QtWidgets.QHBoxLayout()
            item_layout.setSpacing(5)
            item_layout.addWidget(line_text)
            item_layout.addWidget(line_push_button)
            item_widget.setLayout(item_layout)
            self.ui.verticalLayout_plugin_store.addWidget(item_widget)

    def stylesheet_button_install_plugin(self, state="install"):
        if state == "install":
            stylesheet = """
                    QPushButton {
                        color: rgb(25,25,25);
                        border-radius: 3px;
                        padding-left:8px;
                        padding-right:8px;
                        background-color: #57965c;
                    }
                    
                    QPushButton:hover {
                        background-color: rgb(255, 255, 255);
                        border: 2px solid rgb(52, 59, 72);
                    }
                    
                    QPushButton:pressed {
                        background-color: rgb(35, 40, 49);
                        border: 2px solid rgb(43, 50, 61);
                        color: rgb(255,255,255);
                    }"""

        else:
            stylesheet = """
                    QPushButton {
                        color: rgb(25,25,25);
                        border-radius: 3px;
                        padding-left:8px;
                        padding-right:8px;
                        background-color: rgb(236, 30, 68);
                    }

                    QPushButton:hover {
                        background-color: rgb(255, 255, 255);
                        border: 2px solid rgb(52, 59, 72);
                    }

                    QPushButton:pressed {
                        background-color: rgb(35, 40, 49);
                        border: 2px solid rgb(43, 50, 61);
                        color: rgb(255,255,255);
                    }"""
        return stylesheet

    def clear_item_layout(self):
        while self.ui.verticalLayout_plugin_store.count():
            item = self.ui.verticalLayout_plugin_store.takeAt(0)
            widget = item.widget()
            widget.deleteLater()

    def clicked_plugin_remove(self):
        """Delete a plugin application from the system.

        Args:
            index (int): The index of the application to be deleted in the list of available plugins.

        Returns:
            None

        Raises:
            None

        The function prompts the user with a confirmation message, and if the user confirms, deletes the plugin
        application from the system. The function then reloads the list of available plugins, initializes the available
        plugin UI, and displays a success message.

        """
        sender = self.sender()
        name = sender.accessibleName()
        path_file = os.path.abspath(".")
        path = path_file + '/plugins/' + name

        reply = QtWidgets.QMessageBox.question(None, 'Message',
                                               "Are you sure want to delete \n" +
                                               name + " application ?\n",
                                               QtWidgets.QMessageBox.StandardButton.Yes |
                                               QtWidgets.QMessageBox.StandardButton.No,
                                               QtWidgets.QMessageBox.StandardButton.No)

        if reply == QtWidgets.QMessageBox.StandardButton.Yes:
            self.ctrl_plugin.remove_plugin_folder(path)
            self.ctrl_plugin.plugin.reload_plugins()
            self.ctrl_plugin.init_available_plugin()
            self.ctrl_plugin.pop_up_message_box("Plugins was successfully deleted !!")
            self.ui.add_plugins_button.show()
            self.get_list_plugins()
        else:
            print('clicked_plugin_remove no')

    def clicked_install_plugins(self):
        sender = self.sender()
        push_button = self.findChild(QtWidgets.QPushButton, sender.objectName())
        name = self.__plugins_list[int(push_button.objectName())]
        self.download_plugins_from_github(name)
        self.get_list_plugins()

    def download_plugins_from_github(self, plugin):
        access_token = self.__data_github["token"]
        path_file = os.path.abspath(".")
        try:
            repo_url = f'https://{access_token}@github.com/perseverance-tech-tw/{plugin}'
            destination_path = os.path.join(path_file, 'plugins', plugin)

            git.Repo.clone_from(repo_url, destination_path, branch='main')

            try:
                self.ctrl_plugin.refresh_the_plugin_available()
            except:
                self.pop_up_message_box("Have error in installation apps")
        except:
            self.pop_up_message_box("Have error in installation apps")
            return None

    @classmethod
    def pop_up_message_box(cls, message=""):
        """Displays a message box with the given message.

        Args:
            message: The message to display in the message box.

        Returns:
            None

        Raises:
            None
        """
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
        msg.setStyleSheet("font-family: Segoe UI; font-size:14px;")
        msg.setWindowTitle("Information")
        # setting message for Message Box
        msg.setText("Information !! \n\n" + message)
        msg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        msg.show()

        def close_msg():
            msg.done(0)

        QtCore.QTimer.singleShot(6000, close_msg)

    def onclick_close_plugin_store(self):
        self.ui.stackedWidget_2.setCurrentIndex(0)

    @QtCore.pyqtSlot(dict)
    def show_config_view_in_information(self, config):
        """
        Updates the information labels in the UI with the given configuration data.

        Args:
            config (dict): A dictionary containing the configuration data to be displayed.
                It should have the following keys:

                - "Media_path": A string representing the path to the media being used.
                - "Cam_type": A string representing the type of camera being used.
                - "Parameter_name": A string representing the name of the parameter being used.

        Returns:
            None

        Side effects:
            - Updates the "Media path" label in the UI with the value of "Media_path" in config.
            - Updates the "Media type" label in the UI with the value of "Cam_type" in config.
            - Updates the "Parameter used" label in the UI with the value of "Parameter_name" in config.
        """
        if config is not None:
            media_path = str(config["Media_path"])
            camera_type = str(config["Cam_type"])
            parameter = str(config["Parameter_name"])
            self.ui.label_info_media_path.setText(media_path)
            self.ui.label_info_media_type.setText(camera_type)
            self.ui.label_info_parameter_used.setText(parameter)

    def reset_view_back_to_original(self):
        """Resets the UI to its original state.

        Unlocks the menu state view, enables the mode view widget, and hides it. If
        the image result is not None, resets its width and angle to default values,
        sets the state of the rubberband tool to False, and re-runs the image
        processing pipeline after loading a saved image. Finally, updates the UI to
        display the new rotation value.

        Args:
            None

        Returns:
            None
        """
        self.unlock_menu_state_view()
        self.ui.widget_mode_view.setEnabled(True)
        self.ui.widget_mode_view.hide()

        if self.__image_result is not None:
            self.resetStyle(self.ui.btn_fisheye_view.objectName())
            self.ui.btn_fisheye_view.setStyleSheet(self.set_style_selected_menu())

            if self.model_apps.state_rubberband:
                self.model_apps.state_rubberband = False
            self.__width_image_result = self.round_to_nearest_100(self.ui.scrollArea.width())
            self.model_apps.set_angle_rotate = 0
            self.__angle_image_result = 0
            self.model_apps.re_run_after_load_saved_image()
            self.show_rotation_value()

            self.ui.widget_mode_view.hide()
            self.ui.frame_recenter_image.hide()

            self.ui.spinBox_icx.setEnabled(False)
            self.ui.spinBox_icy.setEnabled(False)

            self.ui.doubleSpinBox_alpha_rec.setEnabled(False)
            self.ui.doubleSpinBox_beta_rec.setEnabled(False)

            self.model_apps.recenter_image_state = False
            self.model_apps.reset_coordinate_recenter_to_default()
            self.ui.checkBox_reverse_view.setChecked(False)

            self.model_apps.create_image_result()

    def change_polygon_state(self):
        """Sets the drawing state of the polygon based on the checked state of the UI element.

        If the 'check_draw_polygon' UI element is checked, the drawing state of the polygon will be set to True.
        Otherwise, it will be set to False.

        Args:
            None

        Returns:
            None
        """
        if self.ui.check_draw_poligon.isChecked() or self.ui.check_draw_poligon_pano.isChecked():
            self.model_apps.set_draw_polygon = True

        else:
            self.model_apps.set_draw_polygon = False

    def label_recenter_mouse_leave_event(self, event):
        self.model_apps.label_recenter_mouse_leave_event()

    def label_original_mouse_leave_event(self, event):
        """Handle the mouse leave event on the original image label.

        This method is called when the mouse leaves the original image label in the
        UI. It delegates the handling of the event to the model_apps instance of the
        Model class.

        Args:
            event (QEvent): The event object representing the mouse leave event.

        Returns:
            None
        """
        self.model_apps.label_original_mouse_leave_event()

    def label_original_mouse_double_click_event(self, event):
        """
        Handles the mouse double-click event for the `label_original` widget, which displays the original fisheye image.

        If the current view mode is `AnypointView`, calls the corresponding `model_apps` method and displays the
        corresponding `anypoint_config` UI widget.

        Args:
            event: A `QMouseEvent` object representing the mouse double-click event.

        Returns:
            None.
        """
        if self.model_apps.state_recent_view == "AnypointView":
            if self.ui.radio_mode_1.isChecked():
                self.model_apps.label_original_mouse_double_click_anypoint_mode_1()
                self.anypoint_config.showing_config_mode_1()
            else:
                self.model_apps.label_original_mouse_double_click_anypoint_mode_2()
                self.anypoint_config.showing_config_mode_2()

    def label_recenter_mouse_press_event(self, event):
        if event.buttons() == QtCore.Qt.MouseButton.LeftButton:
            if self.model_apps.state_rubberband:
                print("under developing")
            else:
                if self.model_apps.state_recent_view == "AnypointView":
                    if self.ui.radio_mode_1.isChecked():
                        self.model_apps.label_recenter_mouse_press_event_anypoint_mode_1(event)
                        self.model_apps.create_maps_anypoint_mode_1()
                        self.anypoint_config.showing_config_mode_1()
                    else:
                        self.model_apps.label_recenter_mouse_press_event_anypoint_mode_2(event)
                        self.model_apps.create_maps_anypoint_mode_2()
                        self.anypoint_config.showing_config_mode_2()

                elif self.model_apps.state_recent_view == "PanoramaView":
                    if self.ui.radioButton_car.isChecked():
                        self.model_apps.label_original_mouse_press_event_panorama_car(event)
                        self.panorama_config.showing_config_panorama_car()
                        self.model_apps.create_maps_panorama_car()

    def label_original_mouse_press_event(self, event):
        """
        Handles mouse press events on the original label.

        Args:
            event (QtGui.QMouseEvent): The mouse press event.

        Returns:
            None
        """
        if event.buttons() == QtCore.Qt.MouseButton.LeftButton:
            if self.model_apps.state_rubberband:
                print("under developing")
            else:
                if self.model_apps.state_recent_view == "AnypointView":
                    if self.ui.radio_mode_1.isChecked():
                        if self.model_apps.recenter_image_state:
                            self.model_apps.label_original_recenter_mode(event)
                            self.model_apps.label_original_mouse_double_click_anypoint_mode_1()

                        else:
                            self.model_apps.label_original_mouse_press_event_anypoint_mode_1(event)
                            self.model_apps.create_maps_anypoint_mode_1()
                        self.anypoint_config.showing_config_mode_1()

                    else:
                        if self.model_apps.recenter_image_state:
                            self.model_apps.label_original_recenter_mode(event)
                            self.model_apps.label_original_mouse_double_click_anypoint_mode_2()

                        else:
                            self.model_apps.label_original_mouse_press_event_anypoint_mode_2(event)
                            self.model_apps.create_maps_anypoint_mode_2()
                        self.anypoint_config.showing_config_mode_2()

                elif self.model_apps.state_recent_view == "PanoramaView":
                    if self.ui.radioButton_car.isChecked():
                        if self.model_apps.recenter_image_state:
                            self.model_apps.label_original_recenter_mode(event)
                            self.model_apps.reset_panorama_car()
                            # self.panorama_config.showing_config_panorama_car()

                        else:
                            self.model_apps.label_original_mouse_press_event_panorama_car(event)
                            self.panorama_config.showing_config_panorama_car()
                        self.model_apps.create_maps_panorama_car()
                    else:
                        if self.model_apps.recenter_image_state:
                            self.model_apps.label_original_recenter_mode(event)

                else:
                    if self.ui.checkBox_reverse_view.isChecked():
                        self.model_apps.mouse_press_event_handler_recenter(event)

    def label_recenter_mouse_move_event(self, event):
        self.model_apps.label_recenter_mouse_move_event(self.ui.label_image_recenter, event)

    def label_original_mouse_move_event(self, event):
        """
        Handles mouse move events on the original label.

        Args:
            event:

        Returns:
            None
        """
        self.model_apps.label_original_mouse_move_event(self.ui.label_image_original, event)

    def label_result_mouse_double_click(self, event):
        """
        Handles mouse double-click events on the original label.

        Args:
            event (QtGui.QMouseEvent): The mouse press event.

        Returns:
            None
        """
        if self.model_apps.state_rubberband:
            self.model_apps.create_image_result()
            self.model_apps.state_rubberband = False
            self.model_apps.create_image_result()
        else:
            self.ui.check_draw_poligon.setChecked(False)
            self.change_polygon_state()
            self.model_apps.create_maps_fov()
            self.showing_new_window_full_screen()

    def label_result_mouse_press_event(self, event):
        """Handles the mouse press event on the result image label.

        Args:
            event: A `QMouseEvent` object representing the mouse press event.

        Returns:
            None.

        Note:
            This function is responsible for creating and showing a rubberband when the left mouse button is pressed on
            the result image label. The rubberband is used to select a specific region of interest (ROI) in the image.
        """
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            if self.__image_result is not None:
                self.rubberband.hide()
                self.origin = event.pos()
                self.rubberband.setGeometry(QtCore.QRect(self.origin, QtCore.QSize()))
                self.rubberband.show()

    def label_result_mouse_move_event(self, event):
        """
        Handle mouse move events on the result label.

        Args:
            event: A `QMouseEvent` instance representing the mouse move event.

        Returns:
            None.
        """
        if event.buttons() == QtCore.Qt.MouseButton.LeftButton:
            if self.__image_result is not None:
                if self.rubberband.isVisible():
                    self.rubberband.setGeometry(QtCore.QRect(self.origin, event.pos()))

    def label_result_mouse_release_event(self, event):
        """
        Handles the mouse release event on the label_result widget.

        Args:
            event: A QMouseEvent object representing the mouse event.

        Returns:
            None.

        Behavior:
            If the left mouse button was released and an image is loaded, the size of the rubberband is checked.
            If it has a width and height greater than 20 pixels and the state of the rubberband is False, the size of
            the rubberband is stored in the model's size_rubberband attribute, the state of the rubberband is set to
            True, and a new image result is created. The rubberband is then hidden. If the right mouse button is
            released, the menu_mouse_event method is called with the event object and the string "label_result" as
            arguments.
        """
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            if self.__image_result is not None:
                size_rubberband = self.rubberband.geometry()
                if size_rubberband.width() > 20 and size_rubberband.height() > 20:
                    if self.model_apps.state_rubberband is False:
                        self.model_apps.size_rubberband = size_rubberband
                        self.model_apps.state_rubberband = True
                        self.model_apps.create_image_result()

                self.rubberband.hide()

        elif event.button() == QtCore.Qt.MouseButton.RightButton:
            self.menu_mouse_event(event, "label_result")

    def label_original_mouse_release_event(self, event):
        """Handle the mouse release event on the original image label.

        Args:
            event (QMouseEvent): The mouse release event that triggered the function.

        Returns:
            None.
        """
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            pass
        else:
            self.menu_mouse_event(event, "label_original")

    def menu_mouse_event(self, event, label):
        """
        Show a context menu on the mouse event with options for the specified label.

        Args:
            event: A `QMouseEvent` object containing information about the mouse event.
            label: A string indicating the label type, either "label_result" or "label_original".

        Returns:
            None
        """
        menu = QtWidgets.QMenu()
        if self.model_apps.state_rubberband:
            close = menu.addAction("Close Preview")

            def close_preview():
                self.model_apps.state_rubberband = False
                self.model_apps.create_image_result()

            close.triggered.connect(close_preview)

        save = menu.addAction("Save Image")
        info = menu.addAction("Show Info")

        if label == "label_result":
            save.triggered.connect(lambda: self.save_image(True))
            info.triggered.connect(lambda: self.show_information_of_image(label))
        else:
            save.triggered.connect(lambda: self.save_image(False))
            info.triggered.connect(lambda: self.show_information_of_image(label))

        menu.exec(event.globalPosition().toPoint())

    def show_information_of_image(self, label):
        """Displays information about the current image view.

        Displays a message box with information about the current image view, including whether it is a fisheye,
        anypoint, or panorama view. If the current view has a polygon drawn on it, the message box will indicate
        that the polygon is being shown and the user can change the ROI by clicking on the image.

        If the application is in zooming mode to view a specific ROI, a message box will be displayed indicating
        that the user should close the preview or press 'Esc' on the keyboard to return.

        Args:
            label (str): The label of the current image view.

        Returns:
            None

        """
        if self.model_apps.state_rubberband:
            QtWidgets.QMessageBox.information(self, "Info!", "You're in zooming mode to see the specific ROI, \n"
                                                             "close preview or press 'Esc' on the keyboard\n"
                                                             "for return")
            return

        info = ""
        if label == "label_result":
            if self.model_apps.state_recent_view == "FisheyeView":
                info = "original fisheye image"
            elif self.model_apps.state_recent_view == "AnypointView":
                info = "Anypoint mode {} image".format(1 if self.ui.radio_mode_1.isChecked() else 2)
            elif self.model_apps.state_recent_view == "PanoramaView":
                info = "Panorama {} image".format("car" if self.ui.radioButton_car.isChecked() else "Tube")
        else:
            if self.model_apps.set_draw_polygon:
                if self.model_apps.state_recent_view == "FisheyeView":
                    info = "original fisheye image"
                elif self.model_apps.state_recent_view == "AnypointView":
                    info = "Showing original fisheye image with polygon\n" \
                           "for showing anypoint mode {}. You can change\n" \
                           "the ROI by clicking this image!!".format(1 if self.ui.radio_mode_1.isChecked() else 2)
                elif self.model_apps.state_recent_view == "PanoramaView":
                    info = "Showing original fisheye image with polygon\n" \
                           "for showing panorama {}. You can change\n" \
                           "the ROI by clicking this image!!".format(
                        "car" if self.ui.radioButton_car.isChecked() else "tube")

        QtWidgets.QMessageBox.information(self, "Info!", info)

    def save_image(self, image_result=True):
        """Saves the current or resulting image to a selected folder.

        Args:
            image_result (bool, optional): Determines whether to save the resulting image
                (`True`) or the original image (`False`). Defaults to `True`.

        :Raises:
            FileNotFoundError: If the base directory for saving images is not found.

        """
        if self.__image_result is not None:
            if self.__base_dir_save is None or self.__base_dir_save == "":
                self.__base_dir_save = self.model.select_directory(parent_dir="../saved_image",
                                                                   title="Select Folder")

            if self.__base_dir_save:
                if self.model_apps.state_recent_view == "FisheyeView":
                    self.__dir_save = self.__base_dir_save + "/original/"
                elif self.model_apps.state_recent_view == "AnypointView":
                    self.__dir_save = self.__base_dir_save + "/anypoint/"
                elif self.model_apps.state_recent_view == "PanoramaView":
                    self.__dir_save = self.__base_dir_save + "/panorama/"
                else:
                    self.__dir_save = None

                if image_result:
                    image = self.__image_result
                else:
                    self.__dir_save = self.__base_dir_save + "/original/"
                    image = self.model_apps.image

                self.model_apps.save_image_file(image, self.__dir_save,
                                                self.model_apps.parameter_name)

                self.load_saved_image_list(load=True)
                QtWidgets.QMessageBox.information(
                    None, "Information", "Image saved !!\n\nLoc @: " + self.__dir_save)
        else:
            print('save_image failed')

    def onclick_record_video_button(self):
        """Handle the click event on the Record Video button.

        This function displays an information message indicating that video recording is currently under development,
        and unchecks the Record Video button.

        Args:
            None.

        Returns:
            None.
        """
        # self.show_message("Information", "Record video under developing!!")
        if self.model_apps.image is not None:
            if self.ui.record_button.isChecked():
                self.show_message("Information", "Recording started!!")
                self.model_apps.record_video_pressed()
            else:
                self.show_message("Information", "Recording finish!!")
                self.model_apps.finish_recording_video()

    def load_saved_image_list(self, load=False):
        """Loads saved images into the GUI's list widget.

        Args:
            load (bool, optional): Whether to load the images into the list widget. Defaults to False.

        Returns:
            None
        """
        self.ui.listWidget_saved_image.clear()
        for i in range(len(self.model_apps.saved_image_list)):
            name_file = os.path.basename(self.model_apps.saved_image_list[i])
            image = cv2.imread(self.model_apps.saved_image_list[i])
            self.add_widget_save_image(image, name_file, load)

    def add_widget_save_image(self, image, name_file, load=False):
        """
        Adds a new widget to the saved image list with the given image and file name.

        Args:
            image (numpy.ndarray): The image to be displayed in the widget.
            name_file (str): The name of the image file.
            load (bool, optional): Whether the widget is being added during load or not. Defaults to False.

        Returns:
            None
        """
        self.ui.listWidget_saved_image.setIconSize(QtCore.QSize(140, 120))
        new_widget = QtWidgets.QListWidgetItem()

        image_ = self.model.resize_image(image, 140)
        imagePixmap = QtGui.QImage(
            image_.data,
            image_.shape[1],
            image_.shape[0],
            QtGui.QImage.Format.Format_RGB888).rgbSwapped()
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(imagePixmap))
        new_widget.setIcon(icon)
        if load:
            new_widget.setText(str(name_file))
        else:
            new_widget.setText(str(name_file) + ".png")
        self.ui.listWidget_saved_image.addItem(new_widget)
        self.model_apps.add_position_video_on_saved_image()

    def list_widget_saved_image_activated(self):
        """Handle the activation of a saved image in the list widget.

        The function sets the appropriate image view mode and opens the saved image.

        Args:
            None.

        Returns:
            None.
        """
        self.model_apps.load_saved_image = False
        self.model_apps.state_rubberband = False
        file_name = self.model_apps.saved_image_list[self.ui.listWidget_saved_image.currentRow()]
        view = file_name.split('/')[-2]
        if view == "original":
            self.ui.widget_mode_view.setEnabled(True)
            self.ui.widget_mode_view.hide()
            if self.model_apps.video:
                self.unlock_menu_state_view()
                self.model_apps.set_position_frame_save_image(file_name, True)
            else:
                self.unlock_menu_state_view()
                self.model_apps.reopen_saved_image(file_name)
            self.ui.btn_fisheye_view.setStyleSheet(self.set_style_selected_menu())

        elif view == "anypoint":
            self.lock_menu_state_view()
            self.ui.btn_anypoint_view.setStyleSheet(self.set_style_selected_menu())
            self.ui.widget_mode_view.show()
            self.ui.frame_22.hide()
            # self.ui.frame_pointer_anypoint.hide()
            self.ui.widget_mode_view.setEnabled(False)
            self.ui.widget_mode_view.setCurrentIndex(0)
            self.model_apps.reopen_saved_image(file_name)

        elif view == "panorama":
            self.lock_menu_state_view()
            self.ui.frame_22.hide()
            # self.ui.frame_pointer_anypoint.hide()
            self.ui.btn_panorama_view.setStyleSheet(self.set_style_selected_menu())
            self.ui.widget_mode_view.show()
            self.ui.widget_mode_view.setEnabled(False)
            self.ui.widget_mode_view.setCurrentIndex(1)
            self.model_apps.reopen_saved_image(file_name)

        else:
            return

    def lock_menu_state_view(self):
        """
        Locks the state of the view menu by disabling all view mode buttons and resetting their style to default.

        Args:
            None

        Returns:
            None
        """
        self.reset_style_button_menu()
        self.ui.btn_fisheye_view.setEnabled(False)
        self.ui.btn_anypoint_view.setEnabled(False)
        self.ui.btn_panorama_view.setEnabled(False)

    def unlock_menu_state_view(self):
        """
        Unlocks the state of the menu for viewing modes, enabling the FishEye, AnyPoint, and Panorama buttons.

        Args:
            None

        Returns:
            None
        """
        self.reset_style_button_menu()
        self.ui.btn_fisheye_view.setEnabled(True)
        self.ui.btn_anypoint_view.setEnabled(True)
        self.ui.btn_panorama_view.setEnabled(True)

    def reset_style_button_menu(self):
        """
        Resets the style of the fish-eye, anypoint, and panorama buttons to their default state.

        Args:
            None

        Returns:
            None
        """
        self.resetStyle(self.ui.btn_fisheye_view)
        self.resetStyle(self.ui.btn_anypoint_view)
        self.resetStyle(self.ui.btn_panorama_view)

    def change_properties_panorama(self):
        """Change the properties of the panorama configuration according to the selected options.

        If there is a result image, this function updates the panorama configuration and maps based on the
        selected radio button, which can be "Car" or "Tube". It then updates the file configuration. If
        there is no result image, this function does nothing.

        Args:
            None

        Returns:
            None
            """
        if self.__image_result is not None:
            self.model_apps.state_rubberband = False
            if self.ui.radioButton_car.isChecked():
                self.panorama_config.change_properties_panorama_car()
                self.model_apps.create_maps_panorama_car()

            else:
                self.panorama_config.change_properties_panorama_tube()
                self.model_apps.create_maps_panorama_tube()
            self.model_apps.update_file_config()

    def change_properties_crop_panorama(self):
        """Changes the properties of the current panorama crop.

        If there is a panorama image loaded, this function updates the properties of the crop using the settings
        selected in the UI. If the "car" option is selected, the panorama is cropped to a horizontal field of view
        of 360 degrees and a vertical field of view of 90 degrees. If the "tube" option is selected, the panorama is
        cropped to a horizontal field of view of 180 degrees and a vertical field of view of 360 degrees.

        After updating the properties of the crop, this function updates the app's configuration file and creates
        a new image result.

        Args:
            None

        Returns:
            None
        """
        if self.__image_result is not None:
            self.model_apps.state_rubberband = False
            if self.ui.radioButton_car.isChecked():
                self.panorama_config.change_properties_panorama_car()
            else:
                self.panorama_config.change_properties_panorama_tube()

            self.model_apps.update_file_config()
            self.model_apps.create_image_result()

    def change_mode_panorama(self):
        """Changes the panorama mode to either 'car' or 'tube'.

        This method sets the panorama mode to either 'car' or 'tube' based on the selected radio button.
        If the 'car' radio button is selected, the car configuration frame is shown and the tube configuration frame
        is hidden. The opposite is true if the 'tube' radio button is selected. The panorama configuration object is
        then updated and the maps for the selected mode are created.

        Raises:
            None

        Returns:
            None
        """
        self.model_apps.state_rubberband = False
        self.model_apps.create_maps_fov()
        if self.ui.radioButton_car.isChecked():
            self.ui.frame_panorama_tube_config.hide()
            self.ui.frame_panorama_car_config.show()
            self.panorama_config.showing_config_panorama_car()
            self.model_apps.change_panorama_mode = "car"
            self.model_apps.create_maps_panorama_car()

        else:
            self.ui.frame_panorama_car_config.hide()
            self.ui.frame_panorama_tube_config.show()
            self.panorama_config.showing_config_panorama_tube()
            self.model_apps.change_panorama_mode = "tube"
            self.model_apps.create_maps_panorama_tube()
        self.model_apps.update_properties_config_when_change_view_mode()

    def activate_change_optical_point(self):
        if self.ui.checkBox_reverse_view.isChecked():
            if self.__image_result is not None:
                self.ui.frame_recenter_image.show()
                self.ui.spinBox_icx.setEnabled(True)
                self.ui.spinBox_icy.setEnabled(True)
                self.ui.doubleSpinBox_alpha_rec.setEnabled(True)
                self.ui.doubleSpinBox_beta_rec.setEnabled(True)
                self.model_apps.recenter_image_state = True
                self.model_apps.recenter_image_process()
                self.model_apps.create_image_result()

        else:
            if self.__image_result is not None:
                self.ui.spinBox_icx.setEnabled(False)
                self.ui.spinBox_icy.setEnabled(False)
                self.ui.doubleSpinBox_alpha_rec.setEnabled(False)
                self.ui.doubleSpinBox_beta_rec.setEnabled(False)
                self.ui.frame_recenter_image.hide()
                self.model_apps.recenter_image_state = False
                self.model_apps.create_image_result()

        self.model_apps.update_properties_config_when_change_view_mode()

    @QtCore.pyqtSlot(list)
    def set_value_coordinate(self, coordinate):
        self.ui.spinBox_icx.blockSignals(True)
        self.ui.spinBox_icy.blockSignals(True)
        self.ui.spinBox_icx.setValue(coordinate[0])
        self.ui.spinBox_icy.setValue(coordinate[1])
        self.ui.spinBox_icx.blockSignals(False)
        self.ui.spinBox_icy.blockSignals(False)

    @QtCore.pyqtSlot(list)
    def set_value_coordinate_in_recenter_image(self, coordinate):
        self.ui.label_pos_x.setText(str(coordinate[0]))
        self.ui.label_pos_y.setText(str(coordinate[1]))

    def change_coordinate_optical_point(self):
        icx = self.ui.spinBox_icx.value()
        icy = self.ui.spinBox_icy.value()
        self.model_apps.change_coordinate_by_spinbox(icx, icy)

    def change_alpha_beta_optical_point(self):
        alpha = self.ui.doubleSpinBox_alpha_rec.value()
        beta = self.ui.doubleSpinBox_beta_rec.value()
        self.model_apps.change_alpha_beta_by_spinbox(alpha, beta)

    @QtCore.pyqtSlot(object)
    def show_recenter_image(self, image):
        self.model.show_image_to_label(self.ui.label_image_recenter, image, 320)

    def change_mode_anypoint(self):
        """Change the current anypoint mode.

        Changes the anypoint mode based on the selected radio button in the user interface.
        Shows or hides certain configuration options depending on the selected mode.
        Updates the anypoint maps and the anypoint mode in the model.

        Returns:
            None
        """
        self.model_apps.state_rubberband = False
        if self.ui.radio_mode_1.isChecked():
            self.ui.label_6.hide()
            self.ui.doubleSpinBox_roll.hide()
            self.ui.label.setText("Alpha:")
            self.ui.label_28.setText("Beta:")
            self.anypoint_config.showing_config_mode_1()
            self.model_apps.change_anypoint_mode = "mode_1"
            self.model_apps.create_maps_anypoint_mode_1()

        else:
            self.ui.label_6.show()
            self.ui.doubleSpinBox_roll.show()
            self.ui.label.setText("Pitch:")
            self.ui.label_28.setText("Yaw:")
            self.anypoint_config.showing_config_mode_2()
            self.model_apps.change_anypoint_mode = "mode_2"
            self.model_apps.create_maps_anypoint_mode_2()

        self.model_apps.update_properties_config_when_change_view_mode()

    def change_properties_anypoint(self):
        """Changes the properties of the AnyPoint view mode.

        If an image result is available, this method changes the properties of the AnyPoint view mode according to
        the values set in the GUI. The changes are applied to the configuration object, and new maps are created.
        The configuration file is updated accordingly.

        Raises:
            None.

        Returns:
            None.
        """
        self.model_apps.state_rubberband = False
        if self.__image_result is not None:
            if self.ui.radio_mode_1.isChecked():
                self.anypoint_config.change_properties_mode_1()
                self.model_apps.create_maps_anypoint_mode_1()
            else:
                self.anypoint_config.change_properties_mode_2()
                self.model_apps.create_maps_anypoint_mode_2()
            self.model_apps.update_file_config()

    def onclick_anypoint(self):
        """Handle anypoint buttons click event.

        If radio_mode_1 is checked, the method sets the alpha and beta values of the model_apps object based on which
        button was clicked and then calls the showing_config_mode_1 and create_maps_anypoint_mode_1 methods.
        If radio_mode_1 is not checked, the method sets the alpha and beta values of the model_apps object based on
        which button was clicked and then calls the showing_config_mode_2 and create_maps_anypoint_mode_2 methods.
        It also sets the state_rubberband attribute of the model_apps object to False and updates the file config.

        Raises:
            None

        Returns:
            None
        """
        if self.ui.radio_mode_1.isChecked():
            if self.sender().objectName() == "pushButton_any_up":
                self.model_apps.set_alpha_beta(75, 0)
            elif self.sender().objectName() == "pushButton_any_bottom":
                self.model_apps.set_alpha_beta(75, 180)
            elif self.sender().objectName() == "pushButton_any_center":
                self.model_apps.set_alpha_beta(0, 0)
            elif self.sender().objectName() == "pushButton_any_left":
                self.model_apps.set_alpha_beta(75, -90)
            elif self.sender().objectName() == "pushButton_any_right":
                self.model_apps.set_alpha_beta(75, 90)
            self.anypoint_config.showing_config_mode_1()
            self.model_apps.create_maps_anypoint_mode_1()

        else:
            if self.sender().objectName() == "pushButton_any_up":
                self.model_apps.set_alpha_beta(75, 0)
            elif self.sender().objectName() == "pushButton_any_bottom":
                self.model_apps.set_alpha_beta(-75, 0)
            elif self.sender().objectName() == "pushButton_any_center":
                self.model_apps.set_alpha_beta(0, 0)
            elif self.sender().objectName() == "pushButton_any_left":
                self.model_apps.set_alpha_beta(0, -75)
            elif self.sender().objectName() == "pushButton_any_right":
                self.model_apps.set_alpha_beta(0, 75)
            self.anypoint_config.showing_config_mode_2()
            self.model_apps.create_maps_anypoint_mode_2()
        self.model_apps.state_rubberband = False
        self.model_apps.update_file_config()

    @classmethod
    def read_the_documentation(cls):
        """Opens the HTML documentation for this project in a new browser tab.

        If the `../docs/build/html` directory doesn't exist, this method runs the command `make -C ../docs html`
        to generate the documentation. Then, it opens the `index.html` file in the `../docs/build/html`
        directory in a new browser tab.

        Args:
            cls: The class object itself.

        Returns:
            None
        """
        if os.name == 'nt':
            if not os.path.isdir("../docs/build/html"):
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
                msg.setWindowTitle("Information")
                # setting message for Message Box
                msg.setText("Document building in progress. Please be patient!, \n"
                            "Once completed, a new tab will open in your browser.")
                msg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                msg.show()

                def close_msg():
                    msg.done(0)
                    os.system(r"..\docs\make.bat html")
                    QtWidgets.QApplication.processEvents()
                    webbrowser.open(r'..\docs\build\html\index.html', new=2)

                QtCore.QTimer.singleShot(3000, close_msg)

            else:
                webbrowser.open(r'..\docs\build\html\index.html', new=2)

        elif os.name == 'posix':
            if not os.path.isdir("../docs/build/html"):
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
                msg.setWindowTitle("Information")
                # setting message for Message Box
                msg.setText("Document building in progress. Please be patient!, \n"
                            "Once completed, a new tab will open in your browser.")
                msg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                msg.show()

                def close_msg():
                    msg.done(0)
                    os.system("make -C ../docs html")
                    QtWidgets.QApplication.processEvents()
                    webbrowser.open('../docs/build/html/index.html', new=2)

                QtCore.QTimer.singleShot(3000, close_msg)

            else:
                webbrowser.open('../docs/build/html/index.html', new=2)

        else:
            print("This os is not support yet!")

    @classmethod
    def show_message(cls, title, message, timer=5000):
        """Show an information message box with a title and a message for 5 seconds.

        Args:
            title: A string with the title of the message box.
            message: A string with the message to be displayed.
            timer:

        Returns:
            None
        """
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        msg.show()
        QtCore.QTimer.singleShot(timer, lambda: msg.done(0))

    @classmethod
    def onclick_btn_github(cls):
        """
        Open the link to the project's GitHub page in a new browser window.

        Args:
            None

        Returns:
            None
        """
        webbrowser.open('https://github.com/McutOIL', new=2)

    def onclick_button_menu(self):
        """
        Handles the click event for the menu button.

        This method calls the button_menu method of the ctrl_apps object to show the menu with a width of 220 pixels
        and sets the flag to True to indicate that the menu is open.

        Args:
            self: The instance of the current object.

        Returns:
            None.
        """
        self.ctrl_apps.button_menu(220, True)

    def onclick_button_about_us(self):
        """
        Handles the click event for the "About Us" button.

        This method calls the button_about_us method of the ctrl_apps object to show the "About Us" page and sets
        the flag to True to indicate that the page is open. The current theme of the app is also passed as a
        parameter to the button_about_us method.

        Args:
            self: The instance of the current object.

        Returns:
            None.
        """
        self.ctrl_apps.button_about_us(True, self.model.theme)

    def onclick_button_setting_menu(self):
        """
        Handles the click event for the "Settings" button.

        This method calls the setting_menu method of the ctrl_apps object to show the "Settings" menu and sets the
        flag to True to indicate that the menu is open. The current theme of the app is also passed as a parameter
        to the setting_menu method.

        Args:
            self: The instance of the current object.

        Returns:
            None.
        """
        self.ctrl_apps.setting_menu(True, self.model.theme)

    def onclick_record_screen(self):
        """
        Handles the click event of the record screen button.

        If the button is checked, the screen recording is started and the button icon is changed to the "record" icon.
        If the button is unchecked, the screen recording is stopped and the button icon is changed to the "stop" icon.

        Args:
            None

        Returns:
            None

        Raises:
            None
        """
        if self.ui.btn_record_screen.isChecked():
            print("record ")
            if not self.model.update_scree_image.worker.timer.isActive():
                if not self.model.update_scree_image.thread.isRunning():
                    self.model.update_scree_image.worker.timer.start()
                self.model.update_scree_image.worker.initialize_record_screen()
                self.model.update_scree_image.worker.record_state = True
                self.model.update_scree_image.worker.timer.start()
                self.ui.btn_record_screen.setIcon(QtGui.QIcon("icons:Record-screen.png"))
        else:
            print("not record ")
            self.model.update_scree_image.worker.record_state = False
            self.model.update_scree_image.worker.timer.stop()
            self.ui.btn_record_screen.setIcon(QtGui.QIcon("icons:record-screen_black.png"))

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        width = self.ui.scrollArea.width() - 20
        self.__width_image_result = self.round_to_nearest_100(width)

        if self.__image_result is not None:
            self.show_image_result()

    @classmethod
    def round_to_nearest_100(cls, num):
        return round(num / 20) * 20

    def closeEvent(self, event):
        if self.model_apps.cap is not None:
            self.model_apps.timer.stop()
        sys.exit()

    def moveEvent(self, event):
        """
        Moves the screen image worker to the position specified by the given event.

        Args:
            event: A PyQt event containing information about the new position of the screen image worker.

        Returns:
            The return value of the super() method for the same event.

        Raises:
            N/A
        """
        self.model.update_scree_image.worker.get_event(event.pos())
        return super().moveEvent(event)

    def onclick_btn_open_media(self):
        """
        Handles the click event for the "Open Media" button.

        This method prompts the user to select a media source and loads the selected media into the app. If the
        user selects a file, it sets the media source and parameter name in the model_apps object and calls the
        load_saved_image_list and show_rotation_value methods to update the UI. It also updates the view mode and
        hides some UI elements. If there is a result image, it sets the recent view state in the model_apps object
        to "FisheyeView" and loads the saved image list.

        If the user does not select a file, this method displays an information message box.

        Args:
            self: The instance of the current object.

        Returns:
            None.
        """
        if os.name == "nt":
            self.model_apps.timer.stop()
            source_type, cam_type, source_media, parameter_name = self.model.select_media_source()
            if source_media is None:
                self.model_apps.create_image_original()
                self.show_message("Information", "No media selected, Load the previous media!", 3000)

            else:
                self._handle_successful_media_selection(source_type, cam_type, source_media, parameter_name)

        else:
            source_type, cam_type, source_media, parameter_name = self.model.select_media_source()
            if source_media is not None:
                self._handle_successful_media_selection(source_type, cam_type, source_media, parameter_name)
            else:
                QtWidgets.QMessageBox.information(None, "Information!", "You not select any file !!")

    def _handle_successful_media_selection(self, source_type, cam_type, source_media, parameter_name):
        self.model_apps.set_media_source(source_type, cam_type, source_media, parameter_name)
        self.model_apps.create_maps_fov()
        if type(source_media) == int or source_media.endswith(('.mp4', '.MOV', '.avi', '.mjpg')):
            if self.model_apps.recenter_image_state:
                self.ui.widget_mode_view.hide()
                self.ui.frame_recenter_image.hide()
                self.ui.checkBox_reverse_view.setChecked(False)
                self.model_apps.recenter_image_state = False
                self.model_apps.create_image_result()

        self.load_saved_image_list(load=True)
        self.show_rotation_value()
        self.ui.widget_mode_view.hide()
        # self.ui.frame_pointer_anypoint.hide()
        self.resetStyle(self.ui.btn_anypoint_view)
        self.resetStyle(self.ui.btn_panorama_view)
        self.ui.btn_fisheye_view.setStyleSheet(self.set_style_selected_menu())
        self.set_resolution_sources()
        if self.__image_result is not None:
            self.model_apps.state_recent_view = "FisheyeView"
            self.load_saved_image_list(load=True)

    def set_resolution_sources(self):
        self.ui.comboBox_resolution_sources.blockSignals(True)
        self.ui.comboBox_resolution_sources.clear()
        self.ui.comboBox_resolution_sources.blockSignals(False)
        if self.model_apps.resolution_option:
            for item in self.model_apps.resolution_option:
                self.ui.comboBox_resolution_sources.addItem(f"{str(item[0])} x {str(item[1])}")

    @QtCore.pyqtSlot(str)
    def control_video_controller(self, source_media_type):
        """
        Controls the visibility of the video controller frame based on the type of media source.

        This method takes a string parameter, source_media_type, that specifies the type of media source. If the
        source is an image, the video controller frame is hidden. Otherwise, it is shown.

        Args:
            self: The instance of the current object.
            source_media_type: A string that specifies the type of media source.

        Returns:
            None.
        """
        if source_media_type == "image":
            self.ui.frame_video_controller.hide()
        else:
            self.ui.frame_video_controller.show()

    @QtCore.pyqtSlot(bool)
    def onclick_play_pause_video(self, status):
        """
        Handles the play/pause button click event for the video player.

        This method takes a boolean parameter, status, that indicates whether the video should be played or paused. If the
        status is True, the play/pause button is updated to show the pause icon. Otherwise, it is updated to show the play
        icon.

        Args:
            self: The instance of the current object.
            status: A boolean that indicates whether the video should be played (True) or paused (False).

        Returns:
            None.
        """
        if status:
            self.ui.play_pause_button.setIcon(QtGui.QIcon("icons:pause.svg"))
        else:
            self.ui.play_pause_button.setIcon(QtGui.QIcon("icons:play.svg"))

    @QtCore.pyqtSlot(float)
    def set_slider_position(self, value):
        """
        Sets the position of the video slider.

        This method takes a float parameter, value, that represents the position of the video slider. The slider is updated to
        the given value, and the blockSignals method is used to prevent signals from being emitted during the update.

        Args:
            self: The instance of the current object.
            value: A float that represents the new position of the video slider.

        Returns:
            None.
        """
        self.ui.slider_video_time.blockSignals(True)
        self.ui.slider_video_time.setValue(int(value))
        self.ui.slider_video_time.blockSignals(False)

    @QtCore.pyqtSlot(list)
    def show_timer_video_info(self, list_timer):
        """
        Updates the video timer labels with the given time values.

        This method takes a list parameter, list_timer, that contains four values representing the current and total times
        of the video in minutes and seconds. The current time is displayed in the label_current_time label, and the total time
        is displayed in the label_total_time label.

        Args:
            self: The instance of the current object.
            list_timer: A list of four integers representing the current and total times of the video in minutes and seconds.

        Returns:
            None.
        """
        self.ui.label_current_time.setText("%02d:%02d" % (list_timer[2], list_timer[3]))
        self.ui.label_total_time.setText("%02d:%02d" % (list_timer[0], list_timer[1]))

    @QtCore.pyqtSlot(list)
    def alpha_beta_from_coordinate(self, alpha_beta):
        """
        Sets the alpha and beta values based on the given coordinate.

        This method takes a list parameter, alpha_beta, that contains two values representing the alpha and beta angles of a
        spherical coordinate. If either value is None, then the alpha and beta labels are set to 0.0. Otherwise, the alpha and
        beta labels are set to the rounded values of alpha_beta[0] and alpha_beta[1], respectively.

        Args:
            self: The instance of the current object.
            alpha_beta: A list of two floating-point numbers representing the alpha and beta angles of a spherical coordinate.

        Returns:
            None.
        """
        self.ui.doubleSpinBox_alpha_rec.blockSignals(True)
        self.ui.doubleSpinBox_beta_rec.blockSignals(True)
        if any(elem is None for elem in alpha_beta):
            self.ui.doubleSpinBox_alpha_rec.setValue(0)
            self.ui.doubleSpinBox_beta_rec.setValue(0)
        else:
            self.ui.doubleSpinBox_alpha_rec.setValue(round(alpha_beta[0], 2))
            self.ui.doubleSpinBox_beta_rec.setValue(round(alpha_beta[1], 2))
        self.ui.doubleSpinBox_alpha_rec.blockSignals(False)
        self.ui.doubleSpinBox_beta_rec.blockSignals(False)

    @QtCore.pyqtSlot(list)
    def alpha_beta_from_coordinate_recenter_image(self, alpha_beta):
        if any(elem is None for elem in alpha_beta):
            self.ui.label_alpha.setText(str(0))
            self.ui.label_beta.setText(str(0))

        else:
            self.ui.label_alpha.setText(str(round(alpha_beta[0], 2)))
            self.ui.label_beta.setText(str(round(alpha_beta[1], 2)))

    @QtCore.pyqtSlot(object)
    def show_image_original(self, image):
        """
        Displays the original image in the designated label.

        This method takes an image object and displays it in the label_image_original widget. The image is scaled to fit within
        the dimensions of the label while maintaining its aspect ratio.

        Args:
            self: The instance of the current object.
            image: An image object to display in the label.

        Returns:
            None.
        """
        if self.full_screen_mode:
            image = self.model_apps.draw_fov_original_image(image)
            self.model.show_image_to_label(self.label_full_screen_origin_image, image, 400)
        else:
            self.ui.frame_image_original.setMinimumSize(QtCore.QSize(0, 0))
            self.model.show_image_to_label(self.ui.label_image_original, image, 320)

    @QtCore.pyqtSlot(object)
    def get_image_result(self, image):
        """
        Sets the image result and displays it.

        This method takes an image object and sets it as the current image result. It then calls the show_image_result method to
        display the image in the label. If no image is provided, the method does nothing.

        Args:
            self: The instance of the current object.
            image: An image object to set as the current image result.

        Returns:
            None.
        """
        self.__image_result = image
        self.show_image_result()

    def control_change_zooming(self):
        """
        Controls the change of zooming in the displayed image. Updates the displayed image's width according to
        the zoom level set by the user through the spinBox_zooming input. The updated width is chosen from a
        predefined list of possible values to ensure the closest match to the desired width.

        Args:
            None.

        Returns:
            None.

        Raises:
            None.
        """
        list_zoom = [520, 560, 596, 696, 796, 896, 996, 1096, 1196, 1296, 1396, 1496, 1596, 1696, 1796, 1896, 1996,
                     2096, 2196, 2296, 2396, 2496, 2596, 2596, 2696, 2796, 2896, 3096, 3196, 3296, 3396, 3496, 3596]

        if self.__image_result is not None:
            width = self.model_apps.image.shape[1]
            value = width * (self.ui.spinBox_zooming.value() / 100)
            active = min(list_zoom, key=lambda x: abs(x - value))
            self.__width_image_result = active
            self.show_image_result()

    def zoom_image(self, operation):
        """Zooms in or out on the result image.

        Args:
            operation (str): The zoom operation to perform. Must be one of "zoom_in" or "zoom_out".
        """
        if operation == "zoom_in":
            self.__width_image_result = self.ctrl_result_image.zoom_in(self.__width_image_result)
        elif operation == "zoom_out":
            self.__width_image_result = self.ctrl_result_image.zoom_out(self.__width_image_result)
        self.show_image_result()

    def show_percentage_zoom(self):
        """Displays the percentage of the current zoom level in the zoom spin box.

        Calculates the percentage of the current width of the image result with respect to the original width of
        the input image, and sets the value of the zoom spin box to this percentage.

        Args:
            None

        Returns:
            None
        """
        value = round((self.__width_image_result / self.model_apps.image.shape[1]) * 100)
        self.ui.spinBox_zooming.blockSignals(True)
        self.ui.spinBox_zooming.setValue(value)
        self.ui.spinBox_zooming.blockSignals(False)

    def show_image_result(self):
        """Displays the image result with the specified width and angle to the result label.

        Args:
            image: The image result to be displayed on the label.

        Returns:
            None
        """
        if self.__image_result is not None:
            if self.full_screen_mode:
                width_full_screen_mode = self.round_to_nearest_100(self.new_window.width())
                self.__image_result = cv2.flip(self.__image_result, 1)
                self.model.show_image_to_label(self.label_full_screen,
                                               self.__image_result,
                                               width_full_screen_mode,
                                               plusIcon=True)

            else:
                self.model_apps.set_width_image_on_label_result(self.__width_image_result)
                if self.model_apps.state_rubberband:
                    self.model.show_image_to_label(self.ui.label_result,
                                                   self.__image_result,
                                                   self.__width_image_result,
                                                   angle=self.model_apps.set_angle_rotate,
                                                   plusIcon=True)
                else:
                    self.model.show_image_to_label(self.ui.label_result,
                                                   self.__image_result,
                                                   self.__width_image_result,
                                                   plusIcon=True)
                self.show_percentage_zoom()

    def rotate_image(self, direction):
        """Rotates the result image in the specified direction.

        Args:
            direction (str): The direction to rotate the image. Must be either "left" or "right".

        Returns:
            None.

        """
        if self.__image_result is not None:
            if direction == "left":
                self.__angle_image_result = self.ctrl_result_image.rotate_right(self.__angle_image_result)
            else:
                self.__angle_image_result = self.ctrl_result_image.rotate_left(self.__angle_image_result)
            self.model_apps.set_angle_rotate = self.__angle_image_result * -1
            if self.model_apps.state_rubberband:
                self.show_image_result()
            else:
                self.model_apps.create_image_result()
            self.show_rotation_value()

    def show_rotation_value(self):
        """Sets the value of the rotation angle in the GUI.

        Disables the signals of the GUI double spin box widget, sets its value to
        the current rotation angle and enables the signals back again.

        Args:
            None

        Returns:
            None
        """
        self.ui.doubleSpinBox_rotate.blockSignals(True)
        self.ui.doubleSpinBox_rotate.setValue(self.__angle_image_result)
        self.ui.doubleSpinBox_rotate.blockSignals(False)

    def rotation_change_value(self):
        """Updates the rotation angle when the user changes its value.

        Sets the new value of the rotation angle to the private attribute and also
        to the model of the application. If the rubber band tool is active, it
        updates the result image and the percentage of zoom. Otherwise, it creates
        a new result image.

        Args:
            None

        Returns:
            None
        """
        if self.__image_result is not None:
            self.__angle_image_result = self.ui.doubleSpinBox_rotate.value()
            self.model_apps.set_angle_rotate = self.__angle_image_result * -1
            if self.model_apps.state_rubberband:
                self.show_image_result()
            else:
                self.model_apps.create_image_result()

    def onclick_btn_fisheye(self):
        """
        Changes the current view mode to fisheye.

        The function changes the current view mode to "FisheyeView" and hides the anypoint pointer frame and
        mode view widget.

        Args:
            None

        Returns:
            None
        """
        self.change_stylesheet_selected_menu()
        if self.__image_result is not None:
            self.model_apps.state_recent_view = "FisheyeView"
            self.model_apps.state_rubberband = False
            self.ui.widget_mode_view.hide()
            self.ui.frame_pointer_in_recenter_frame.hide()
            self.model_apps.create_image_result()
            self.model_apps.update_properties_config_when_change_view_mode()
        else:
            print('onclick_btn_fisheye (image result was None)')

    def onclick_btn_anypoint(self):
        """Handles the button click event for the Anypoint mode.

        Changes the application state to the Anypoint mode, shows the Anypoint widget, and sets the
        current index of the widget to 0.

        Returns:
            None
        """
        self.change_stylesheet_selected_menu()
        if self.__image_result is not None:
            self.change_mode_anypoint()
            self.model_apps.state_recent_view = "AnypointView"
            self.model_apps.state_rubberband = False
            self.ui.widget_mode_view.show()
            self.ui.check_draw_poligon_pano.setChecked(False)
            self.ui.check_draw_poligon.setChecked(True)
            self.ui.frame_pointer_in_recenter_frame.show()
            self.ui.widget_mode_view.setCurrentIndex(0)
            self.model_apps.update_properties_config_when_change_view_mode()
        else:
            print('onclick_btn_anypoint (image result was None)')

    def onclick_btn_panorama(self):
        """Handles click event for the 'panorama' button.

        Changes the app's recent view state to 'PanoramaView', shows the widget mode view and frame pointer anypoint,
        sets the current index of the widget mode view to 1, and sets the state rubberband to False if an image has been loaded.

        Returns:
            None
        """
        self.change_stylesheet_selected_menu()
        if self.__image_result is not None:
            self.change_mode_panorama()
            self.model_apps.state_recent_view = "PanoramaView"
            self.model_apps.state_rubberband = False
            self.ui.widget_mode_view.show()
            self.ui.check_draw_poligon.setChecked(False)
            self.ui.check_draw_poligon_pano.setChecked(True)
            self.ui.widget_mode_view.setCurrentIndex(1)
            self.ui.frame_pointer_in_recenter_frame.show()
            self.model_apps.update_properties_config_when_change_view_mode()
        else:
            print('onclick_btn_panorama (image result was None)')

    # controller standard application user interface
    def onclick_clear_user_interface(self):
        """Clears the user interface and resets the app state to its default state.

        This function resets the app's state to its default state, clears the displayed images, and resets the style
        of the mode buttons.

        Args:
            None.

        Returns:
            None.
        """
        self.onclick_btn_fisheye()
        self.model_apps.timer.stop()
        self.__image_result = None
        self.model_apps.image = None
        self.model_apps.image_resize = None
        self.ui.label_result.setMinimumSize(QtCore.QSize(0, 0))
        self.ui.label_result.setMaximumSize(QtCore.QSize(700, 170))
        self.ui.label_result.setPixmap(QtGui.QPixmap("icons:moilapp.png"))
        self.ui.label_result.setScaledContents(True)
        self.ui.frame_image_original.setMinimumSize(QtCore.QSize(0, 200))
        self.ui.label_image_original.setMinimumSize(QtCore.QSize(0, 0))
        self.ui.label_image_original.setMaximumSize(QtCore.QSize(200, 50))
        self.ui.label_image_original.setPixmap(QtGui.QPixmap("icons:moilapp.png"))
        self.ui.label_image_original.setScaledContents(True)
        self.resetStyle(self.ui.btn_fisheye_view)
        self.resetStyle(self.ui.btn_anypoint_view)
        self.resetStyle(self.ui.btn_panorama_view)
        self.ui.listWidget_saved_image.clear()

        self.ui.widget_mode_view.hide()
        self.ui.frame_recenter_image.hide()
        self.ui.stackedWidget_2.setCurrentIndex(0)
        # self.ui.frame_pointer_anypoint.hide()

        self.ui.spinBox_icx.blockSignals(True)
        self.ui.spinBox_icy.blockSignals(True)
        self.ui.spinBox_icx.setValue(0)
        self.ui.spinBox_icy.setValue(0)
        self.ui.spinBox_icx.blockSignals(False)
        self.ui.spinBox_icy.blockSignals(False)

        self.ui.doubleSpinBox_alpha_rec.setEnabled(False)
        self.ui.doubleSpinBox_beta_rec.setEnabled(False)

        self.model_apps.recenter_image_state = False

        self.model_apps.reset_config()
        self.model_apps.saved_image_list = []
        if self.model_apps.cap is not None:
            try:
                self.model_apps.cap.close()
            except:
                pass
        self.model_apps.cap = None

    def onclick_clear_button_list_saved_image(self):
        """
        Clear the saved image list and the UI list widget.

        Returns:
            None.
        """
        self.model_apps.saved_image_list = []
        self.model_apps.clear_saved_image()
        self.ui.listWidget_saved_image.clear()

    def close_setting_window(self):
        """
        Closes the settings window if it is open.

        Returns:
            None
        """
        width = self.ui.frame_additional_left.width()
        if width != 0:
            self.ctrl_apps.setting_menu(True, self.model.theme)

    def escape_event(self):
        """
        Escape button keyboard event. Will return to the default state of application.

        Returns:

        """
        self.ctrl_apps.button_menu(70, True)
        width = self.ui.frame_additional_right.width()
        if width != 0:
            self.ctrl_apps.button_about_us(True, self.model.theme)
        width = self.ui.frame_additional_left.width()
        if width != 0:
            self.ctrl_apps.setting_menu(True, self.model.theme)

        if self.model_apps.state_rubberband:
            self.model_apps.state_rubberband = False
            self.model_apps.create_image_result()

        self.unlock_menu_state_view()
        self.reset_view_back_to_original()

    def onclick_play_pause_video_button(self):
        if self.model_apps.load_saved_image:
            self.reset_view_back_to_original()
        self.model_apps.play_pause_video()

    def mouse_event_in_moil_logo(self, event):
        """Handle mouse events in the MOIL logo.

        Args:
            event: The mouse event to handle.

        Returns:
            None
        """
        if event.type() == QtCore.QEvent.Type.MouseButtonPress:
            if event.button() == QtCore.Qt.MouseButton.LeftButton:
                self.back_to_home()

    def onclick_help_button(self):
        message_box = QtWidgets.QMessageBox()
        message_box.setIcon(QtWidgets.QMessageBox.Icon.Information)
        message_box.setWindowTitle('Help!')
        message_box.setText('This is a help menu application, The content still under developing!!')
        message_box.setInformativeText('Version 1.0')
        message_box.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        message_box.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
        message_box.exec()

    def back_to_home(self):
        """
        Switches the content view to home screen and hides plugin buttons and sets the plugin index to None.

        Returns:
            None
        """
        file_path = os.path.join(os.getcwd(), "models", "cached", "plugin_cached.yaml")
        with open(file_path, "r") as file:
            config = yaml.safe_load(file)

        if config["plugin_run"] is not None:
            plugin = self.ctrl_plugin.plugin.plugins[config["plugin_run"]]

            try:
                plugin.widget.timer.stop()
                plugin.widget.model_plugin.cap.close()

            except:
                print("no cap opened")

        self.ui.stackedWidget_2.setCurrentIndex(0)
        self.ui.widget_container_content.setCurrentIndex(0)
        self.ui.frame_btn_moilapp.show()
        self.ui.frame_button_view.show()
        self.ui.add_plugins_button.show()
        self.ui.delete_plugins_button.hide()
        self.ui.label_plugin_name.hide()
        self.ui.close_plugin_button.hide()
        self.ui.open_in_new_window_plugins.hide()
        self.ctrl_plugin.index = None
        file_path = os.path.join(os.getcwd(), "models", "cached", "plugin_cached.yaml")
        with open(file_path, "r") as file:
            config = yaml.safe_load(file)
        config["plugin_run"] = self.ctrl_plugin.index
        with open(file_path, "w") as outfile:
            yaml.dump(config, outfile, default_flow_style=False)

    @QtCore.pyqtSlot(dict)
    def showing_git_repository_information(self, data=None):
        """
        Updates the UI with information about a Git repository.

        Args:
            data (dict): A dictionary containing information about the Git repository.

        Returns:
            None
        """
        self.ui.textBrowser_3.setText(data["origin_url"])
        self.__data_github = data
        self.ui.label_active_branch.setText(data["active_branch"])
        self.ui.textBrowser_token.setText(data["token"])
        self.ui.comboBox.clear()
        self.ui.comboBox.addItems(data["list_branch"])
        index = self.ui.comboBox.findText(data["active_branch"])
        self.ui.comboBox.setCurrentIndex(index)
        if self.__data_github["token"] is not None:
            self.show_info_of_github_repository()
        else:
            new = "Software cant find your token for this repository"
            self.ui.textBrowser.setText(new)

    def onclick_refresh_github_repository(self):
        """Updates the Github repository information by refreshing the repository and showing the updated information if there
            are any changes.

        Returns:
            None
        """
        if self.__data_github["token"] is None:
            if self.show_update_dialog("No token found, input your token?") != QtWidgets.QMessageBox.StandardButton.Yes:
                return
            if not self.open_dialog_for_input_token():
                return

        self.model_apps.refresh_github_information()
        current_hash = self.model_apps.repo_github.head.object.hexsha
        branch = str(self.model_apps.repo_github.active_branch)
        latest_hash = self.model_apps.repo_github.remotes.origin.refs[branch].object.hexsha
        if latest_hash != current_hash:
            self.show_info_of_github_repository()
        else:
            self.show_message("information", "the software already up to date")

    def check_for_update(self):
        """Checks for updates in the Git repository.

        If Git is not installed, does nothing. If a token is not set, asks the user to input one.
        Otherwise, calls `show_info_of_github_repository` and `check_for_new_update`.

        Returns:
            None
        """
        if not call(["git", "branch"], stderr=STDOUT, stdout=open(os.devnull, 'w')) != 0:
            if self.__data_github["token"] is None:
                if self.show_update_dialog(
                        "No token found, input your token?") == QtWidgets.QMessageBox.StandardButton.Yes:
                    if self.open_dialog_for_input_token():
                        self.check_for_new_update()
            else:
                self.show_info_of_github_repository()
                self.check_for_new_update()

    def check_for_new_update(self):
        """Check if a new software update is available and install it if user approves.

        Returns:
            None
        """
        current_hash = self.model_apps.repo_github.head.object.hexsha
        self.model_apps.repo_github.remotes.origin.fetch()
        branch = str(self.model_apps.repo_github.active_branch)
        latest_hash = self.model_apps.repo_github.remotes.origin.refs[branch].object.hexsha
        if latest_hash != current_hash:
            if self.show_update_dialog(
                    "Software update available, install now?") == QtWidgets.QMessageBox.StandardButton.Yes:
                release_message = self.model_apps.repo_github.remotes.origin.refs[branch].object.message
                self.model_apps.repo_github.remotes.origin.pull()
                self.show_update_successful_message(release_message)
        else:
            self.show_message("Information", "The software is already up to date")

    def show_update_dialog(self, message):
        """Displays a message box with options for the user to choose.

        Args:
            message: A string containing the message to be displayed in the message box.

        Returns:
            An integer representing the user's response to the message box. The value will be one of the
            following constants from the QMessageBox.StandardButton enum: QMessageBox.Yes, QMessageBox.No.
        """
        reply = QtWidgets.QMessageBox()
        reply.setWindowTitle("Update")
        reply.setText(message)
        reply.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
        return reply.exec()

    def show_update_successful_message(self, message):
        """
        Shows a message box to indicate that the software has been updated successfully.

        Args:
            message: A string containing the release note for the software update.

        Returns:
            None

        Raises:
            None
        """
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
        msg.setWindowTitle("Information!!")
        msg.setText("Software has successfully updated\n"
                    "Release note:\n" + message +
                    "\nPlease re-run the application for successful update!")
        msg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        msg.show()

        QtCore.QTimer.singleShot(3000, sys.exit)

    def show_info_of_github_repository(self):
        """
        Fetches and displays information about the GitHub repository associated with the application's model.
        Specifically, it retrieves a list of commits behind the currently active branch, and displays their
        commit message and hex SHA in the application's text browser.

        Returns:
            None
        """
        commits_behind = self.model_apps.repo_github.iter_commits(
            f'{self.__data_github["active_branch"]}..origin/{self.__data_github["active_branch"]}')

        text = [f"{commit.hexsha}\n\n{commit.message}\n" for commit in commits_behind]

        new = ''
        if new.join(text) == "":
            message = "The repository no have commits behind\n"
        else:
            message = f'The repository have commits behind\n' \
                      f'here is the record commits for you \n\n' \
                      f'{new.join(text)}'

        self.ui.textBrowser.setText(message)

    def open_dialog_for_input_token(self):
        """
        Displays a dialog box to prompt the user for a GitHub token, and then validates and stores the token in the
        application's model.

        Returns:
            bool: True if the token was successfully validated and stored in the model, False otherwise.
        """
        token, ok = QtWidgets.QInputDialog.getText(None, "Github Token!", "Write your correct token!")
        if not ok:
            return False

        if len(token) < 30:
            self.show_message("Warning!", "You didn't write the password or wrote a wrong token.")
            return False

        self.model_apps.change_config_github(token=token)
        return True

    def onclick_btn_change_branch(self):
        """Handles the click event of the "Change branch" button.

        If the button is checked, shows a frame containing a list of available branches
        for the user to choose from. If the button is unchecked, hides the frame.

        Args:
            self: An instance of the class.

        Returns:
            None.
        """
        if self.ui.btn_change_branch.isChecked():
            self.ui.frame_4.show()
        else:
            self.ui.frame_4.hide()

    def combo_box_change_branch(self):
        """
        Event handler for when the value of the combo box changes. It checks if the selected branch name is different
        from the currently active branch of the GitHub repository. If it is different and a valid GitHub token exists,
        it attempts to change the active branch to the selected branch, and then updates the configuration and GitHub
        information in the application's model. It also checks if the 'docs/build/html' directory exists and removes it
        if it does. Finally, it displays an information message to the user, and then closes the application after a
        delay of 3 seconds.

        If the selected branch cannot be checked out, or if no valid GitHub token exists, it shows an error message to
        the user, and resets the combo box to the currently active branch.

        Returns:
            None
        """
        branch_name = str(self.ui.comboBox.currentText())
        active_branch = self.model_apps.repo_github.active_branch
        if str(active_branch) != branch_name:
            if self.__data_github["token"] is not None:
                try:
                    g = git.Git()
                    g.checkout(branch_name)
                    self.model_apps.change_config_github(branch=branch_name)
                    self.model_apps.github_information()
                    if os.path.isdir("../docs/build/html"):
                        os.system("make -C ../docs clean")

                    msg = QtWidgets.QMessageBox()
                    msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
                    msg.setWindowTitle("Information!!")
                    msg.setText("Branches changed, Application will be closed automatically in 3 seconds!")
                    msg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                    msg.show()

                    def close_msg():
                        msg.done(0)
                        sys.exit()

                    QtCore.QTimer.singleShot(3000, lambda: close_msg())

                except:
                    self.show_message("Information", "Can't change branch, you modify the code. \n"
                                                     "please commit it before you change the branch!!!")
                    self.ui.comboBox.setCurrentText(str(self.model_apps.repo_github.active_branch))
                    self.ui.frame_7.show()

            else:
                self.show_message("Information", "Token cannot finding. Please add !!")

    def onclick_commit_now(self):
        """Commit changes to the Git repository.

        This method commits changes to the Git repository and displays a success or error message
        depending on the result.

        Args:
            self: An instance of the class that this method belongs to.

        Returns:
            None.

        Raises:
            None.
        """
        text = self.ui.plainTextEdit.toPlainText()
        if text == "":
            self.show_message("Information", "Please write the commit message!!")
        else:
            try:
                self.model_apps.repo_github.git.add(all=True)
                self.model_apps.repo_github.index.commit(str(text))
                self.show_message("Information", "Successfully committed, now you can change branch!!")
                self.ui.frame_7.hide()

            except:
                self.show_message("Error", "failed to commit !!")

    def onclick_change_theme_apps(self):
        """
        Change the theme between light and dark modes.

        Returns:
            None
        """
        icon = QtGui.QIcon()

        if self.model.theme == "dark":
            color = "background-color: rgb(255, 255, 255); color: rgb(0, 0, 0);"
            self.ui.statusBar.setStyleSheet(color)
            self.setStyleSheet(self.model.theme_light_mode())
            icon.addPixmap(QtGui.QPixmap("icons:sun.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        else:
            color = "background-color: rgb(44, 49, 58); color: rgb(255, 255, 255);"
            self.ui.statusBar.setStyleSheet(color)
            self.setStyleSheet(self.model.theme_dark_mode())
            icon.addPixmap(QtGui.QPixmap("icons:light/moon.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)

        self.ui.btn_change_theme.setIcon(icon)
        self.ctrl_icon.get_theme_main_apps(self.model.theme)
        self.ctrl_plugin.refresh_theme_widget()

        if self.__image_result is not None:
            view_map = {
                "FisheyeView": self.ui.btn_fisheye_view,
                "AnypointView": self.ui.btn_anypoint_view,
                "PanoramaView": self.ui.btn_panorama_view,
            }

            view = view_map.get(self.model_apps.state_recent_view)
            if view is not None:
                self.resetStyle(view)
                view.setStyleSheet(self.set_style_selected_menu())
            else:
                self.resetStyle(self.ui.btn_setting)
                self.ui.btn_setting.setStyleSheet(self.set_style_selected_menu())

        width_left = self.ui.frame_additional_left.width()
        style = self.ui.btn_setting.styleSheet()
        color = "background-color: rgb(238, 238, 236);"
        color_dark = "background-color: rgb(33, 37, 43);"
        color_show = "background-color: rgb(255, 255, 255);"
        color_dark_show = "background-color: rgb(44, 49, 58);"

        if width_left == 0:
            self.ui.btn_setting.setStyleSheet(style + (color_dark if self.model.theme == "dark" else color))
        else:
            self.ui.btn_setting.setStyleSheet(style + (color_dark_show if self.model.theme == "dark" else color_show))

    def change_stylesheet_selected_menu(self):
        """Change the stylesheet of a selected menu button.

        If an image is available, this function updates the style of a selected menu button by applying a new stylesheet that
        highlights it. The old stylesheet is reset for all other buttons.

        Args:
            self: An instance of the class that this method belongs to.

        Returns:
            None
        """
        if self.__image_result is not None:
            btn = self.sender()
            self.resetStyle(btn.objectName())
            btn.setStyleSheet(self.set_style_selected_menu())

    # selected menu button
    def set_style_selected_menu(self):
        """Returns the CSS stylesheet for the currently selected menu item.

        The returned stylesheet is based on the current theme set in the `model` attribute.

        Returns:
            str: The CSS stylesheet for the selected menu item.
        """
        select = self.stylesheet_selected_menu_light_theme()
        if self.model.theme == "dark":
            select = self.stylesheet_selected_menu_dark_theme()
        return select

    # deselected menu button
    def set_style_deselect_menu(self, getStyle):
        """
        Replaces the selected menu style with an unselected style in the current theme.

        Args:
            getStyle (str): The current style of the menu to be deselected.

        Returns:
            str: The updated style of the menu with the selected style replaced with the unselected style.
        """
        deselect = getStyle.replace(self.stylesheet_selected_menu_light_theme(), "")
        if self.model.theme == "dark":
            deselect = getStyle.replace(self.stylesheet_selected_menu_dark_theme(), "")
        return deselect

    # reset selection button
    def resetStyle(self, widget):
        """Resets the stylesheet of all push buttons in the frame_button_view except for the one with the given
        object name.

        Args:
            widget (str): The object name of the push button to exclude.

        Returns:
            None
        """
        for w in self.ui.frame_button_view.findChildren(QtWidgets.QPushButton):
            if w.objectName() != widget:
                w.setStyleSheet(self.set_style_deselect_menu(w.styleSheet()))

    @classmethod
    def stylesheet_selected_menu_dark_theme(cls):
        """Return the CSS stylesheet for a selected menu button in dark theme.

        Returns:
            str: The CSS stylesheet for a selected menu button in dark theme.

        """
        stylesheet = """
            border-left: 22px solid 
            qlineargradient(spread:pad, x1:0.034, y1:0, x2:0.216, y2:0, stop:0.499 rgba(255, 121, 198, 255), 
            stop:0.5 rgba(85, 170, 255, 0));
            background-color: rgb(45, 49, 55);
        """
        return stylesheet

    @classmethod
    def stylesheet_selected_menu_light_theme(cls):
        """
        Returns the light theme stylesheet for the selected menu.

        Returns:
            str: The stylesheet for the selected menu in the light theme.
        """
        stylesheet = """
            border-left: 22px solid 
            qlineargradient(spread:pad, x1:0.034, y1:0, x2:0.216, y2:0, stop:0.499 rgba(47, 55, 58, 255), 
            stop:0.5 rgba(85, 170, 255, 0));
            background-color: rgb(248, 248, 248);
        """
        return stylesheet
