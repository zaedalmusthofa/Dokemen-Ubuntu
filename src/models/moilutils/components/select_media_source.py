import json
import os
from .form_crud_parameters import CameraParametersForm
from moil_camera import MoilCam
from typing import Dict
import pyexiv2

try:
    from PyQt6 import QtWidgets, QtCore, QtGui
    from .ui_select_media_source import Ui_Dialog

    pyqt_version = "pyqt6"

except:
    from PyQt5 import QtWidgets, QtCore, QtGui
    from .ui_select_media_source_pyqt5 import Ui_Dialog

    pyqt_version = "pyqt5"


class CameraSource(Ui_Dialog):
    def __init__(self, RecentWindow):
        """
        Create class controllers open camera with inheritance from Ui Dialog Class.

        Args:
            RecentWindow ():
        """
        super(CameraSource, self).__init__()
        self.recent_win = RecentWindow
        self.setupUi(self.recent_win)

        self.recent_win.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
        self.recent_win.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)

        self.frame.mousePressEvent = self.mousePressEvent
        self.frame.mouseMoveEvent = self.moveWindow

        type_camera = MoilCam.supported_cam_type()
        self.comboBox_type_cam.addItems(type_camera)

        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.database_camera_parameters = dir_path + "/camera_parameters.json"
        self.list_camera_ip = dir_path + "/list_camera_ip.json"
        with open(self.database_camera_parameters) as f:
            self.data = json.load(f)

        self.camera_source = None
        self.parameter_selected = None
        self.cam_type = None
        self.__file_path = None
        self.index = None
        self.dragPos = None
        self.list_camera = None
        self.comboBox_id_url_camera.addItem('http://<ip-address-cam>:8000/stream.mjpg')

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons:text.svg"), QtGui.QIcon.Mode.Normal,
                       QtGui.QIcon.State.Off)
        self.btn_form_camera_params.setIconSize(QtCore.QSize(40, 40))
        self.btn_form_camera_params.setIcon(icon)

        self.handle_activated_comboBox_camera_source()
        self.handle_activate_type_camera()
        self.add_list_camera_to_combobox()
        self.comboBox_camera_sources.activated.connect(self.handle_activated_comboBox_camera_source)
        self.comboBox_type_cam.activated.connect(self.handle_activate_type_camera)
        self.comboBox_parameters.activated.connect(self.handle_activate_parameters_camera)
        self.btn_form_camera_params.clicked.connect(self.open_camera_parameters_form)
        self.btn_load_media.clicked.connect(self.open_media_path)
        self.btn_refresh.clicked.connect(self.onclick_btn_refresh)
        self.btn_cancel.clicked.connect(self.onclick_comboBox_cancel)
        self.btn_ok.clicked.connect(self.onclick_comboBox_oke)

    def add_list_camera_to_combobox(self):
        self.comboBox_parameters.blockSignals(True)
        self.comboBox_parameters.clear()
        parameter_list = []

        for key in self.data.keys():
            parameter_list.append(key)
        self.comboBox_parameters.addItems(sorted(parameter_list))
        self.comboBox_parameters.blockSignals(False)

    def moveWindow(self, event):
        if pyqt_version == "pyqt6":
            if event.buttons() == QtCore.Qt.MouseButton.LeftButton:
                if self.dragPos is not None:
                    self.recent_win.move(self.recent_win.pos() + event.globalPosition().toPoint() - self.dragPos)
                    self.dragPos = event.globalPosition().toPoint()
                    event.accept()

        else:
            if event.buttons() == QtCore.Qt.LeftButton:
                delta = QtCore.QPoint(event.globalPos() - self.dragPos)
                self.recent_win.move(self.recent_win.x() + delta.x(), self.recent_win.y() + delta.y())
                self.dragPos = event.globalPos()
                event.accept()

    def mousePressEvent(self, event):
        if pyqt_version == "pyqt6":
            self.dragPos = event.globalPosition().toPoint()
        else:
            self.dragPos = event.globalPos()

    def refresh_camera_parameter_list(self):
        """
        When editing the camera parameter, this will show the list of the camera parameter in uptodate
        Returns:
            None
        """
        self.comboBox_parameters.clear()
        new_list = []
        with open(self.database_camera_parameters) as f:
            data_parameter = json.load(f)
        for key in data_parameter.keys():
            new_list.append(key)
        self.comboBox_parameters.addItems(new_list)
        if self.index is not None:
            self.comboBox_parameters.setCurrentIndex(self.index)

    def open_camera_parameters_form(self):
        open_cam_params = QtWidgets.QDialog()
        CameraParametersForm(open_cam_params, self.database_camera_parameters, self.index)
        open_cam_params.exec()
        self.refresh_camera_parameter_list()

    def handle_activate_type_camera(self):
        # self.comboBox_type_cam.setMaximumSize(QtCore.QSize(16777215, 16777215))
        if self.comboBox_type_cam.currentText() == "opencv_usb_cam":
            self.comboBox_type_cam.setMaximumWidth(160)
            self.label_5.setText("ID :")
            self.label_status.setText("")
            self.btn_refresh.hide()
            self.comboBox_id_url_camera.clear()
            camera = [str(x) for x in MoilCam.scan("opencv_usb_cam")]
            self.comboBox_id_url_camera.addItems(camera)

        elif self.comboBox_type_cam.currentText() == "opencv_ip_cam":
            self.comboBox_type_cam.setMaximumWidth(150)
            self.label_5.setText("Cam :")
            self.btn_refresh.show()
            self.comboBox_id_url_camera.clear()
            if os.path.isfile(self.list_camera_ip) and os.access(self.list_camera_ip, os.R_OK):
                with open(self.list_camera_ip) as file_list_cam:
                    self.list_camera = json.load(file_list_cam)

                if len(self.list_camera) == 0:
                    self.comboBox_id_url_camera.clear()
                    self.list_camera = MoilCam.scan("opencv_ip_cam", "admin")

                    json_object = json.dumps(self.list_camera)
                    with open(self.list_camera_ip, "w") as outfile:
                        outfile.write(json_object)

                    camera = [str(x) for x in self.list_camera]
                    self.comboBox_id_url_camera.addItems(camera)
                else:

                    camera = [str(x) for x in self.list_camera]
                    if len(camera) == 0:
                        self.comboBox_id_url_camera.addItems(["No Camera Detected!"])
                    else:
                        self.comboBox_id_url_camera.addItems(camera)

            else:
                # QtWidgets.QMessageBox.information(None, "Information",
                #                                   "No camera found. system will auto scan the camera available."
                #                                   "This action will take several time, \n Please wait till finish!!")
                self.onclick_btn_refresh()
                # self.comboBox_id_url_camera.clear()
                # self.list_camera = MoilCam.scan("opencv_ip_cam", "admin")
                #
                # json_object = json.dumps(self.list_camera)
                # with open(self.list_camera_ip, "w") as outfile:
                #     outfile.write(json_object)
                #
                # camera = [str(x) for x in self.list_camera]
                # self.comboBox_id_url_camera.addItems(camera)

            # with open("sample_file.json", "w") as file:
            #     json.dump(self.list_camera_ip, file)
            # camera = MoilCam.scan_id("opencv_ip_cam", "admin")
            # print(type(camera))
            # if isinstance(camera, Dict):
            #     self.comboBox_id_url_camera.addItems(["Error"])
            #     QtWidgets.QMessageBox.warning(None, "Warning", f"Error obtained: \n{camera['Error']}")
            # else:
                # camera = [str(x) for x in camera]
            # print(camera)
                # self.comboBox_id_url_camera.addItems(camera)

        elif self.comboBox_type_cam.currentText() == "intel_t265":
            self.comboBox_type_cam.setMaximumWidth(180)
            self.label_5.setText("ID :")
            self.btn_refresh.hide()
            # self.comboBox_id_url_camera.clear()
            # camera = MoilCam.scan_id("ids_peak")
            # if isinstance(camera, Dict):
            #     self.comboBox_id_url_camera.addItems(["Error"])
            #     QtWidgets.QMessageBox.warning(None, "Warning", f"Error obtained: \n{camera['Error']}")
            # else:
            #     camera = [str(x) for x in camera]
            self.comboBox_id_url_camera.clear()
            self.comboBox_id_url_camera.addItems(["Under Developing!!!"])

        elif self.comboBox_type_cam.currentText() == "ids_peak":
            self.comboBox_type_cam.setMaximumWidth(180)
            self.label_5.setText("ID :")
            self.btn_refresh.hide()
            # self.comboBox_id_url_camera.clear()
            # camera = MoilCam.scan_id("ids_peak")
            # if isinstance(camera, Dict):
            #     self.comboBox_id_url_camera.addItems(["Error"])
            #     QtWidgets.QMessageBox.warning(None, "Warning", f"Error obtained: \n{camera['Error']}")
            # else:
            #     camera = [str(x) for x in camera]
            self.comboBox_id_url_camera.clear()
            self.comboBox_id_url_camera.addItems(["Under Developing!!!"])

        elif self.comboBox_type_cam.currentText() == "camera_url":
            self.label_5.setText("URL :")
            self.btn_refresh.hide()
            self.comboBox_id_url_camera.clear()

            edit = QtWidgets.QLineEdit()
            edit.setPlaceholderText("Type here.")
            edit.setStyleSheet("color: rgb(255,255,255)")
            self.comboBox_id_url_camera.setLineEdit(edit)

        else:
            pass

    def onclick_btn_refresh(self):
        self.label_status.setText("Scan available cameras, Please wait!!")
        QtWidgets.QApplication.processEvents()
        self.comboBox_id_url_camera.clear()
        self.list_camera = MoilCam.scan("opencv_ip_cam", "admin")

        json_object = json.dumps(self.list_camera)
        with open(self.list_camera_ip, "w") as outfile:
            outfile.write(json_object)

        camera = [str(x) for x in self.list_camera]
        self.comboBox_id_url_camera.addItems(camera)
        self.label_status.setText("Scanning camera finish!")

    def handle_activated_comboBox_camera_source(self):
        """
        Handle the selection from comboBox of source camera.

        Returns:

        """
        if self.comboBox_camera_sources.currentText() == "Streaming Camera":
            self.media_path.hide()
            self.btn_load_media.hide()
            self.comboBox_type_cam.show()
            self.comboBox_id_url_camera.show()
            self.label_5.show()
            self.label_3.show()
            self.btn_refresh.hide()
            # self.label_3.setText("Type cam :")
            self.label_status.setText("Streaming cam, please select type cam!")
            self.label_5.setText("ID :")
            self.comboBox_parameters.setEnabled(True)

        else:
            # self.label_3.setText("Media Path :")
            self.label_3.hide()
            self.comboBox_type_cam.hide()
            self.comboBox_id_url_camera.hide()
            self.media_path.show()
            self.btn_load_media.show()
            # self.label_5.hide()
            self.btn_refresh.hide()
            self.label_5.setText("Media Path :")
            self.label_status.setText("Load media, please select the media path!")
            self.label_5.setMaximumWidth(100)

    def open_media_path(self):
        if pyqt_version == "pyqt6":
            option = QtWidgets.QFileDialog.Option.DontUseNativeDialog
            self.__file_path, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Load Media", "../",
                                                                        "Files format (*.jpeg *.jpg *.png *.gif *.bmg *.avi *.mp4)",
                                                                        options=option)
        else:
            options = QtWidgets.QFileDialog.DontUseNativeDialog
            self.__file_path, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Load Media", "../",
                                                                        "Files format (*.jpeg *.jpg *.png *.gif *.bmg *.avi *.mp4)",
                                                                        options=options)
        if self.__file_path.endswith(('.png', '.jpg', '.jpeg')):
            parameter = self.read_camera_type(self.__file_path)
            self.index = self.comboBox_parameters.findText(parameter)
            if self.index != -1:
                self.comboBox_parameters.setCurrentIndex(self.index)
                self.comboBox_parameters.setStyleSheet("color:rgb(100,100,100);")
                self.comboBox_parameters.setEnabled(False)


            else:
                QtWidgets.QMessageBox.information(None, "Information", 'Camera Parameter Not Available on the list \n'
                                                                       'You can open the parameter form and \n'
                                                                       'synchronize or select the available list!!')
        else:
            self.comboBox_parameters.setStyleSheet("color:rgb(255,255,255);")
            self.comboBox_parameters.setEnabled(True)

        self.media_path.setText(self.__file_path)

    def handle_activate_parameters_camera(self):
        if self.__file_path is not None:
            if self.__file_path.endswith(('.png', '.jpg', '.jpeg')):
                self.write_camera_type(self.__file_path, self.comboBox_parameters.currentText())

    @staticmethod
    def write_camera_type(image_file, type_camera):
        """
        Write the camera type into the image's metadata.

        Args:
            image_file: image file path
            type_camera: name of camera

        Returns:
            None

        .. code-block::

            mutils.write_camera_type('sample_image.jpg', 'Camera_name')

        """
        img = pyexiv2.Image(image_file)
        pyexiv2.registerNs('a namespace for image', 'Image')
        img.modify_xmp({'Xmp.Image.cameraName': type_camera})
        img.close()

    @staticmethod
    def read_camera_type(image_file):
        """
        Read the camera type from image's metadata.

        Args:
            image_file: image file path

        Returns:
            camera type

        .. code-block::

            c_type = mutils.read_camera_type('sample_image.jpg')

        """
        img = pyexiv2.Image(image_file)
        try:
            camera_type = img.read_xmp()['Xmp.Image.cameraName']

        except:
            camera_type = None
        img.close()
        return camera_type

    def camera_source_used(self):
        """
        This function will return the source of camera used depend on what the camera use.

        Returns:
            camera source
        """
        if self.comboBox_camera_sources.currentText() == "Streaming Camera":
            if self.comboBox_type_cam.currentText() == "opencv_usb_cam":
                if self.comboBox_id_url_camera.currentText().startswith('Error'):
                    self.camera_source = None
                else:
                    self.camera_source = int(self.comboBox_id_url_camera.currentText())

            elif self.comboBox_type_cam.currentText() == "opencv_ip_cam":
                key_value = self.comboBox_id_url_camera.currentText()
                self.camera_source = self.list_camera[key_value]

            elif self.comboBox_type_cam.currentText() == "camera_url":
                self.camera_source = self.comboBox_id_url_camera.currentText()

            # if self.comboBox_id_url_camera.currentText() != "":
            #     if self.comboBox_id_url_camera.currentText().startswith('Error'):
            #         self.camera_source = None
            #
            #     else:
            #         if self.comboBox_id_url_camera.currentText().endswith('.mjpg'):
            #             self.camera_source = self.comboBox_id_url_camera.currentText()
            #         else:
            #             try:
            #                 self.camera_source = int(self.comboBox_id_url_camera.currentText())
            #
            #             except:
            #
            #                     key_value = self.comboBox_id_url_camera.currentText()
            #                     self.camera_source = self.list_camera[key_value]
            #
            #                 else:
            #                     self.camera_source = self.comboBox_id_url_camera.currentText()

        else:
            if self.media_path.text() != "":
                self.camera_source = self.media_path.text()

            else:
                self.camera_source = None

        self.cam_type = self.comboBox_type_cam.currentText()
        self.parameter_selected = self.comboBox_parameters.currentText()

    def onclick_comboBox_oke(self):
        """
        Open the camera following the parent function and close the dialog window.

        Returns:

        """
        self.camera_source_used()
        print(self.camera_source)
        self.recent_win.close()

    def onclick_comboBox_cancel(self):
        """
        close the window when you click the buttonBox cancel.

        Returns:

        """
        self.recent_win.close()


style_appearance = """
    QWidget {
        color: rgb(221, 221, 221);
        font: 10pt "Segoe UI";
    }
    
    #frame{
        background-color: rgb(37, 41, 48);
        border: 2px solid rgb(155, 125, 175);
        border-radius: 10px;
    }
    
    #label_title{
    color: rgb(238,238,238);
    font: 14pt "Segoe UI";
    }
    
    QLineEdit {
        font: 9pt "Segoe UI";
        background-color: rgb(33, 37, 43);
        border-radius: 5px;
        border: 1px solid rgb(145, 125, 175);
        padding-left: 10px;
        selection-color: rgb(255, 255, 255);
        selection-background-color: rgb(255, 121, 198);
    }
    QLineEdit:hover {
        border: 2px solid rgb(64, 71, 88);
    }
    QLineEdit:focus {
        border: 2px solid rgb(91, 101, 124);
    }
    
    QComboBox{
        background-color: rgb(27, 29, 35);
        border-radius: 5px;
        border: 1px solid rgb(145, 125, 175);
        padding: 5px;
        padding-left: 10px;
    }

    QComboBox:hover{
        border: 2px solid rgb(64, 71, 88);
    }
    QComboBox::drop-down {
        subcontrol-origin: padding;
        subcontrol-position: top right;
        width: 25px; 
        border-left-width: 3px;
        border-left-color: rgba(39, 44, 54, 150);
        border-left-style: solid;
        border-top-right-radius: 3px;
        border-bottom-right-radius: 3px;	
        background-position: center;
        background-image: url(icons:light/cil-arrow-bottom.png);
        background-repeat: no-reperat;
     }
    QComboBox QAbstractItemView {
        color: rgb(255, 121, 198);	
        background-color: rgb(33, 37, 43);
        padding: 10px;
        selection-background-color: rgb(39, 44, 54);
    }
    
    QPushButton {
        border: 2px solid rgb(52, 59, 72);
        border-radius: 5px;	
        background-color: rgb(52, 59, 72);
    }
    QPushButton:hover {
        background-color: rgb(57, 65, 80);
        border: 2px solid rgb(61, 70, 86);
    }
    QPushButton:pressed {	
        background-color: rgb(35, 40, 49);
        border: 2px solid rgb(43, 50, 61);
    }
"""
