import json

try:
    from PyQt6 import QtWidgets, QtGui, QtCore
    pyqt_version = "pyqt6"
except:
    from PyQt5 import QtWidgets, QtGui, QtCore
    pyqt_version = "pyqt5"

type_camera = None


def set_icon_select_camera_type(comboBox_cam_type):
    comboBox_cam_type.setStyleSheet("QComboBox::drop-down {"
                                    "background-image: url(icons:chevron-down.svg);}")


def select_parameter(camera_parameter):
    """
    This function allows a user to choose what parameter will be used. this function will open a dialog,
    and you can select the parameter available from Combobox.

    Theme will change the color of base widget.

    return:
        cls.__type_camera : load camera type

    - Example:

    .. code-block:: python

        type_camera = MoilUtils.selectCameraType()
    """
    new_list = []

    with open(camera_parameter) as f:
        data_parameter = json.load(f)
    for key in data_parameter.keys():
        new_list.append(key)

    Dialog = QtWidgets.QDialog()
    Dialog.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
    Dialog.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
    Dialog.setObjectName("Dialog")
    Dialog.resize(316, 172)
    Dialog.setStyleSheet("")
    verticalLayout = QtWidgets.QVBoxLayout(Dialog)
    verticalLayout.setObjectName("verticalLayout")
    widget = QtWidgets.QWidget(Dialog)
    widget.setStyleSheet("QWidget {\n"
                              "    color: rgb(221, 221, 221);\n"
                              "    font: 10pt \"Segoe UI\";\n"
                              "}\n"
                              "\n"
                              "#frame_main{\n"
                              "    background-color: rgb(37, 41, 48);\n"
                              "    border: 2px solid rgb(155, 125, 175);\n"
                              "    border-radius: 10px;\n"
                              "}\n"
                              "\n"
                              "#label{\n"
                              "color: rgb(238,238,238);\n"
                              "font: 14pt \"Segoe UI\";\n"
                              "}\n"
                              "\n"
                              "QComboBox{\n"
                              "    color: rgb(221, 221, 221);\n"
                              "    background-color: rgb(27, 29, 35);\n"
                              "    border-radius: 5px;\n"
                              "    border: 1px solid rgb(145, 125, 175);\n"
                              "    padding: 1px;\n"
                              "    padding-left: 15px;\n"
                              "}\n"
                              "\n"
                              "QComboBox:hover{\n"
                              "    border: 2px solid rgb(64, 71, 88);\n"
                              "}\n"
                              "QComboBox::drop-down {\n"
                              "    subcontrol-origin: padding;\n"
                              "    subcontrol-position: top right;\n"
                              "    width: 25px; \n"
                              "    border-left-width: 3px;\n"
                              "    border-left-color: rgba(39, 44, 54, 150);\n"
                              "    border-left-style: solid;\n"
                              "    border-top-right-radius: 3px;\n"
                              "    border-bottom-right-radius: 3px;    \n"
                              "    background-position: center;\n"
                              "    background-image: url(icons:light/cil-arrow-bottom.png);\n"
                              "    background-repeat: no-reperat;\n"
                              " }\n"
                              "QComboBox QAbstractItemView {\n"
                              "    color: rgb(255, 121, 198);    \n"
                              "    background-color: rgb(33, 37, 43);\n"
                              "    padding: 10px;\n"
                              "    selection-background-color: rgb(39, 44, 54);\n"
                              "}\n"
                              "\n"
                              "QPushButton {\n"
                              "    border: 2px solid rgb(52, 59, 72);\n"
                              "    border-radius: 5px;    \n"
                              "    background-color: rgb(52, 59, 72);\n"
                              "}\n"
                              "QPushButton:hover {\n"
                              "    background-color: rgb(57, 65, 80);\n"
                              "    border: 2px solid rgb(61, 70, 86);\n"
                              "}\n"
                              "QPushButton:pressed {    \n"
                              "    background-color: rgb(35, 40, 49);\n"
                              "    border: 2px solid rgb(43, 50, 61);\n"
                              "}")
    widget.setObjectName("widget")
    verticalLayout_4 = QtWidgets.QVBoxLayout(widget)
    verticalLayout_4.setObjectName("verticalLayout_4")
    frame_main = QtWidgets.QFrame(widget)
    frame_main.setMinimumSize(QtCore.QSize(280, 0))
    frame_main.setStyleSheet("")

    frame_main.setObjectName("frame_main")
    verticalLayout_2 = QtWidgets.QVBoxLayout(frame_main)
    verticalLayout_2.setContentsMargins(12, 5, 12, 10)
    verticalLayout_2.setSpacing(10)
    verticalLayout_2.setObjectName("verticalLayout_2")
    verticalLayout_3 = QtWidgets.QVBoxLayout()
    verticalLayout_3.setContentsMargins(-1, -1, -1, 0)
    verticalLayout_3.setSpacing(5)
    verticalLayout_3.setObjectName("verticalLayout_3")
    label = QtWidgets.QLabel(frame_main)
    label.setMinimumSize(QtCore.QSize(0, 30))
    font = QtGui.QFont()
    font.setFamily("Segoe UI")
    font.setPointSize(13)
    font.setBold(False)
    font.setItalic(False)
    font.setWeight(50)
    label.setFont(font)
    label.setStatusTip("")
    label.setStyleSheet("color: rgb(221, 221, 221);\n"
                             "font: 13pt \"Segoe UI\";\n"
                             "border: none;")
    if pyqt_version == "pyqt6":
        label.setAlignment(QtCore.Qt.AlignmentFlag.AlignBottom | QtCore.Qt.AlignmentFlag.AlignHCenter)
    else:
        label.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignHCenter)
    label.setObjectName("label")
    verticalLayout_3.addWidget(label)
    line = QtWidgets.QFrame(frame_main)
    if pyqt_version == "pyqt6":
        line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
    else:
        line.setFrameShape(QtWidgets.QFrame.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Sunken)
    line.setObjectName("line")
    verticalLayout_3.addWidget(line)
    verticalLayout_2.addLayout(verticalLayout_3)
    comboBox_cam_type = QtWidgets.QComboBox(frame_main)
    comboBox_cam_type.setMinimumSize(QtCore.QSize(0, 30))
    comboBox_cam_type.setStyleSheet("")
    comboBox_cam_type.setObjectName("comboBox_cam_type")
    comboBox_cam_type.addItems(new_list)
    verticalLayout_2.addWidget(comboBox_cam_type)
    horizontalLayout_6 = QtWidgets.QHBoxLayout()
    horizontalLayout_6.setObjectName("horizontalLayout_6")
    if pyqt_version == "pyqt6":
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
    else:
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
    horizontalLayout_6.addItem(spacerItem)
    btn_cancel = QtWidgets.QPushButton(frame_main)
    btn_cancel.setMinimumSize(QtCore.QSize(60, 25))
    btn_cancel.setMaximumSize(QtCore.QSize(16777215, 25))
    btn_cancel.setObjectName("btn_cancel")
    horizontalLayout_6.addWidget(btn_cancel)
    btn_ok = QtWidgets.QPushButton(frame_main)
    btn_ok.setMinimumSize(QtCore.QSize(40, 25))
    btn_ok.setMaximumSize(QtCore.QSize(40, 25))
    btn_ok.setObjectName("btn_ok")
    horizontalLayout_6.addWidget(btn_ok)
    verticalLayout_2.addLayout(horizontalLayout_6)
    verticalLayout_4.addWidget(frame_main)
    verticalLayout.addWidget(widget)

    label.setText("Select Camera Type")
    btn_cancel.setText("Cancel")
    btn_ok.setText("Ok")

    btn_ok.clicked.connect(lambda: accept_btn(Dialog, comboBox_cam_type))
    btn_cancel.clicked.connect(lambda: reject_btn(Dialog))
    Dialog.exec()
    return type_camera


def accept_btn(dialog, msg):
    """
    This function is to accept dialog, msg for camera type from the button which user clicked
    in the user interface

    Args:
        dialog: show dialog always in front of the user interface
        msg: accept msg current text from the camera used

    Returns:
        This function is None
    """
    global type_camera
    dialog.accept()
    type_camera = msg.currentText()


def reject_btn(dialog):
    """
    This function is to given reject on dialog if the camera type it's not in accordance
    Args:
        dialog: the rejection to show dialog in front of the user interface
    Returns:
        This function is None
    """
    global type_camera
    dialog.reject()
    type_camera = None
