from .moilutils import MoilUtils
from .thread_screen_capture import UpdaterImage
from .theme import *
import logging

try:
    from PyQt6 import QtCore, QtGui

except:
    from PyQt5 import QtCore, QtGui


class Model(MoilUtils):
    def __init__(self):
        """
        The backend that contains all the data logic.
        The model's job is to simply manage the data. Whether the data is from a database,
        API, or a JSON object, the model is responsible for managing it.

        """
        super(Model, self).__init__()
        self.theme = "dark"
        self.update_scree_image = UpdaterImage()
        self.update_scree_image.worker.main()
        self.update_scree_image.thread.start()

        CURRENT_DIRECTORY = os.path.abspath(".")
        QtCore.QDir.addSearchPath("icons", CURRENT_DIRECTORY + "/models/plugins_model/icons")

    # change style user interface
    def theme_light_mode(self):
        """Sets the user interface theme to light mode.

        Changes the `theme` attribute of the object to "light",
        and returns the value of the `STYLE_LIGHT_MODE` constant.

        Returns:
            int: The value of the `STYLE_LIGHT_MODE` constant.
        """
        self.theme = "light"
        return STYLE_LIGHT_MODE

    def theme_dark_mode(self):
        """Sets the user interface theme to dark mode.

        Changes the `theme` attribute of the object to "dark", and returns the value of the `STYLE_DARK_MODE` constant.

        Returns:
            int: The value of the `STYLE_DARK_MODE` constant.
        """
        self.theme = "dark"
        return STYLE_DARK_MODE

    # stylesheets components begin from here
    def style_pushbutton(self):
        """Generates a Qt stylesheet for QPushButton widgets based on the current theme.

        Returns a string representing the stylesheet to use for QPushButton widgets in the current theme. The style is
        different for "light" and "dark" themes. The returned string can be set as the style sheet of a QPushButton
        widget to apply the theme.

        Returns:
            str: A string representing the Qt stylesheet to use for QPushButton widgets in the current theme.
        """
        if self.theme == "light":
            stylesheet = """
                            QPushButton {
                                color: rgb(0,0,0);
                                border-radius: 3px;
                                padding-left:8px;
                                padding-right:8px;
                                background-color: rgb(235,243,255);
                            }
                            QPushButton:hover {
                                background-color: rgb(255, 255, 255);
                                border: 2px solid rgb(52, 59, 72);
                            }
                            QPushButton:pressed {
                                background-color: rgb(35, 40, 49);
                                border: 2px solid rgb(43, 50, 61);
                                color: rgb(255,255,255);
                            }
                            QPushButton:checked {
                                background-color: rgb(35, 40, 49);
                                border: 2px solid rgb(43, 50, 61);
                                color: rgb(255,255,255);
                            }
                        """
        else:
            stylesheet = """
                            QPushButton {
                                color: rgb(221,221,221);
                                border-radius: 3px;
                                padding-left:8px;
                                padding-right:8px;
                                background-color: #5F676E;
                                border: 2px solid rgb(52, 59, 72);
                            }
                            QPushButton:hover {
                                color: rgb(0,0,0);
                                background-color: rgb(200, 200, 200);
                                border: 1px solid rgb(255, 255, 255);
                            }
                            QPushButton:pressed {
                                background-color: rgb(35, 40, 49);
                                border: 2px solid rgb(43, 50, 61);
                                color: rgb(255,255,255);
                            }
                            QPushButton:checked {
                                background-color: rgb(35, 40, 49);
                                border: 2px solid rgb(43, 50, 61);
                                color: rgb(255,255,255);
                            }
                        """
        return stylesheet

    def style_pushbutton_play_pause_video(self):
        """Generates a Qt stylesheet for QPushButton widgets based on the current theme.

        Returns a string representing the stylesheet to use for QPushButton widgets in the current theme. The style is
        different for "light" and "dark" themes. The returned string can be set as the style sheet of a QPushButton
        widget to apply the theme.

        Returns:
            str: A string representing the Qt stylesheet to use for QPushButton widgets in the current theme.
        """
        if self.theme == "light":
            stylesheet = """
                            QPushButton {
                                color: rgb(0,0,0);
                                border-radius: 3px;
                                padding-left:8px;
                                padding-right:8px;
                                background-color: rgb(235,243,255);
                            }
                            QPushButton:hover {
                                background-color: rgb(255, 255, 255);
                                border: 2px solid rgb(52, 59, 72);
                            }
                            QPushButton:pressed {
                                background-color: rgb(35, 40, 49);
                                border: 2px solid rgb(43, 50, 61);
                                color: rgb(255,255,255);
                            }
                        """
        else:
            stylesheet = """
                            QPushButton {
                                color: rgb(221,221,221);
                                border-radius: 3px;
                                padding-left:8px;
                                padding-right:8px;
                                background-color: #5F676E;
                                border: 2px solid rgb(52, 59, 72);
                            }
                            QPushButton:hover {
                                color: rgb(0,0,0);
                                background-color: rgb(200, 200, 200);
                                border: 1px solid rgb(255, 255, 255);
                            }
                            QPushButton:pressed {
                                background-color: rgb(35, 40, 49);
                                border: 2px solid rgb(43, 50, 61);
                                color: rgb(255,255,255);
                            }
                        """
        return stylesheet

    def style_label(self):
        """Generates a Qt stylesheet for QLabel widgets based on the current theme.

        Returns a string representing the stylesheet to use for QLabel widgets in the current theme. The style is
        different for "light" and "dark" themes. The returned string can be set as the style sheet of a QLabel widget
        to apply the theme.

        Returns:
            str: A string representing the Qt stylesheet to use for QLabel widgets in the current theme.
        """
        if self.theme == "light":
            stylesheet = """
                            QLabel { 
                                background-color: rgb(200,205,205);
                                border-radius:3px;
                            }
                            """
        else:
            stylesheet = """
                            QLabel { 
                                background-color: #17202b;
                                border-radius:3px;
                            }
                        """
        return stylesheet

    def style_label_title(self):
        """Generates a Qt stylesheet for QLabel widgets based on the current theme.

        Returns a string representing the stylesheet to use for QLabel widgets in the current theme. The style is
        different for "light" and "dark" themes. The returned string can be set as the style sheet of a QLabel widget
        to apply the theme.

        Returns:
            str: A string representing the Qt stylesheet to use for QLabel widgets in the current theme.
        """
        if self.theme == "light":
            stylesheet = """
                            QLabel {
                                font-size: 16pt;
                                background-color: rgb(200,205,205);
                                border-radius:3px;
                                font-family: Courier;
                            }
                            """
        else:
            stylesheet = """
                            QLabel {
                                font-size: 16pt;
                                background-color: #17202b;
                                border-radius:3px;
                                font-family: Courier;
                            }
                        """
        return stylesheet

    def style_transparent_label(self):
        """Generates a Qt stylesheet for QLabel widgets based on the current theme.

        Returns a string representing the stylesheet to use for QLabel widgets in the current theme. The style is
        different for "light" and "dark" themes. The returned string can be set as the style sheet of a QLabel widget
        to apply the theme.

        Returns:
            str: A string representing the Qt stylesheet to use for QLabel widgets in the current theme.
        """
        if self.theme == "light":
            stylesheet = """
                            QLabel {
                                background-color: transparent;
                            }
                            """
        else:
            stylesheet = """
                            QLabel {
                                background-color: transparent;
                            }
                        """
        return stylesheet

    def style_frame_main(self):
        """Generates a Qt stylesheet for QLabel widgets based on the current theme.

        Returns a string representing the stylesheet to use for QLabel widgets in the current theme. The style is
        different for "light" and "dark" themes. The returned string can be set as the style sheet of a QLabel widget
        to apply the theme.

        Returns:
            str: A string representing the Qt stylesheet to use for QLabel widgets in the current theme.
        """
        if self.theme == "light":
            stylesheet = """
                            QFrame {
                                    color: rgb(0, 0, 0);
                                    font: 10pt "Segoe UI";
                                    background-color: rgb(255, 255, 255);
                                    border:none;}
                            """
        else:
            stylesheet = """
                            QFrame {
                                    color: rgb(255, 255, 255);
                                    font: 10pt "Segoe UI";
                                    background-color: rgb(44, 49, 58);
                                    border:none;}
                        """
        return stylesheet

    def style_font_12(self):
        if self.theme == "light":
            stylesheet = """
                color: rgb(0, 0, 0);
                font: 12pt "Segoe UI";
            """
        else:
            stylesheet = """
                color: rgb(221, 221, 221);
                font: 12pt "Segoe UI";
            """
        return stylesheet

    def style_font_14(self):
        if self.theme == "light":
            stylesheet = """
                color: rgb(0, 0, 0);
                font: 14pt "Segoe UI";
            """
        else:
            stylesheet = """
                color: rgb(221, 221, 221);
                font: 14pt "Segoe UI";
            """
        return stylesheet

    def style_frame_object(self):
        """Generates a Qt stylesheet for QLabel widgets based on the current theme.

        Returns a string representing the stylesheet to use for QLabel widgets in the current theme. The style is
        different for "light" and "dark" themes. The returned string can be set as the style sheet of a QLabel widget
        to apply the theme.

        Returns:
            str: A string representing the Qt stylesheet to use for QLabel widgets in the current theme.
        """
        if self.theme == "light":
            stylesheet = """
                            QFrame {
                                    color: rgb(0, 0, 0);
                                    background-color: rgb(220, 221, 225);
                                    border:none;}
                            """
        else:
            stylesheet = """
                        QFrame{
                            background-color: rgb(57, 65, 80);
                            border:none;
                        }
                        """
        return stylesheet

    def frame_transparent(self):
        if self.theme == "light":
            stylesheet = """
                            QFrame {
                                    background-color: rgb(220, 221, 225);
                                    color: rgb(0, 0, 0);
                                    border:none;}
                            """
        else:
            stylesheet = """
                            QFrame {
                                    background-color: rgb(57, 65, 80);
                                    border:none;}
                        """
        return stylesheet

    def style_line(self):
        if self.theme == "light":
            stylesheet = """
                            QFrame {
                                    border: 2px solid rgb(255, 255, 255);
                                    width: 1px;}
                            """
        else:
            stylesheet = """
                            QFrame {
                                    border: 2px solid rgb(44, 49, 58);
                                    width: 1px;}
                        """
        return stylesheet

    def style_combobox(self):
        """Returns the Qt stylesheet for a QComboBox widget, based on the current theme.

        Args:
            self: The object that this method belongs to.

        Returns:
            A string containing the Qt stylesheet for the QComboBox widget, based on the current theme.
        """
        if self.theme == "light":
            stylesheet = """
                QComboBox{
                        color: rgb(0, 0, 0);
                        background-color: rgb(238, 238, 236);
                        border-radius: 3px;
                        border: 2px solid rgb(200, 200, 200);
                        padding: 5px;
                        padding-left: 10px;
                    }

                    QComboBox:hover{
                        border: 2px solid rgb(52, 59, 72);
                    }

                    QComboBox::drop-down {
                        subcontrol-origin: padding;
                        subcontrol-position: top right;
                        width: 25px;
                        border-left-width: 3px;
                        border-left-color: rgb(200, 200, 200);
                        border-left-style: solid;
                        border-top-right-radius: 3px;
                        border-bottom-right-radius: 3px;
                        background-image: url(icons:chevron-down.svg);
                        background-position: center;
                        background-repeat: no-repeat;
                     }

                    QComboBox QAbstractItemView {
                        color: rgb(0, 0, 0);
                        background-color: rgb(255, 255, 255);
                        padding:5px;
                        selection-background-color: rgb(39, 44, 54);
                    }
                """

        else:
            stylesheet = """
                QComboBox{
                        background-color: rgb(27, 29, 35);
                        border-radius: 5px;
                        border: 2px solid rgb(52, 59, 72);
                        padding: 5px;
                        padding-left: 10px;
                    }
                QComboBox:hover{
                        border: 2px solid rgb(82, 94, 88);
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
                        background-image: url(icons:light/cil-arrow-bottom.png);
                        background-position: center;
                        background-repeat: no-repeat;
                     }
                QComboBox QAbstractItemView {
                        color: rgb(255, 121, 198);
                        background-color: rgb(33, 37, 43);
                        padding: 10px;
                        selection-background-color: rgb(39, 44, 54);
                    }
                    """
        return stylesheet

    def style_scroll_area(self):
        if self.theme == "light":
            stylesheet = """
            QScrollArea {
                background-color: rgb(220, 221, 225);
                } 

            QScrollBar:horizontal {
                border: 1px solid rgb(180, 180, 180);
                background: rgb(180, 180, 180);
                height: 12px;
                margin: 0px 12px 0 12px;
                border-radius: 0px;
            }
            QScrollBar::handle:horizontal {
                background: rgb(220, 221, 225);
                min-width: 25px;
                border-radius: 0px
            }

            QScrollBar::add-line:horizontal {
                border: none;
                background: rgb(130, 135, 140);
                width: 13px;
                background-image: url(icons:chevron-right-12.svg);
                border-top-right-radius: 0px;
                border-bottom-right-radius: 0px;
                subcontrol-position: right;
                subcontrol-origin: margin;
            }

            QScrollBar::sub-line:horizontal {
                border: none;
                background: rgb(130, 135, 140);
                width: 13px;
                background-image: url(icons:chevron-left-12.svg);
                border-top-left-radius: 0px;
                border-bottom-left-radius: 0px;
                subcontrol-position: left;
                subcontrol-origin: margin;
            }

            QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal{
                 background: none;
            }

            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal{
                 background: none;
            }

            QScrollBar:vertical {
                border: 1px solid rgb(180, 180, 180);
                background: rgb(180, 180, 180);
                width: 12px;
                margin: 12px 0px 12px 0px;
                border-radius: 0px;
            }
            QScrollBar::handle:vertical {
                background: rgb(220, 221, 225);
                min-height: 25px;
                border-radius: 0px
            }

            QScrollBar::add-line:vertical {
                border: none;
                background: rgb(130, 135, 140);
                height: 12px;
                background-image: url(icons:chevron-down-12.svg);
                border-bottom-left-radius: 0px;
                border-bottom-right-radius: 0px;
                subcontrol-position: bottom;
                subcontrol-origin: margin;
            }

            QScrollBar::sub-line:vertical {
                border: none;
                background: rgb(130, 135, 140);
                height: 12px;
                background-image: url(icons:chevron-up-12.svg);
                border-top-left-radius: 0px;
                border-top-right-radius: 0px;
                subcontrol-position: top;
                subcontrol-origin: margin;
            }

            QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
                background: none;
            }

            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }

                """
        else:
            stylesheet = """
            QScrollArea {
                background-color: rgb(57, 65, 80);
                } 

            QScrollBar:horizontal {
                border: 1px solid rgb(80, 80, 80);
                background: rgb(80, 80, 80);
                height: 12px;
                margin: 0px 12px 0px 12px;
                border-radius: 0px;
                }
            QScrollBar::handle:horizontal {
                background: #17202b;;
                min-width: 25px;
                border-radius: 0px
                }

            QScrollBar::add-line:horizontal {
                border: none;
                background: rgb(55, 63, 77);
                width: 12px;
                background-image: url(icons:light/chevron-right-12.png);
                border-top-right-radius: 0px;
                border-bottom-right-radius: 0px;
                subcontrol-position: right;
                subcontrol-origin: margin;
                }

            QScrollBar::sub-line:horizontal {
                border: none;
                background: rgb(55, 63, 77);
                width: 12px;
                background-image: url(icons:light/chevron-left-12.png);
                border-top-left-radius: 0px;
                border-bottom-left-radius: 0px;
                subcontrol-position: left;
                subcontrol-origin: margin;
                }

            QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal
                {
                background: none;
                }

            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal
                {
                background: none;
                }
            QScrollBar:vertical {
                border: 1px solid rgb(80, 80, 80);
                background: rgb(80, 80, 80);
                width: 12px;
                margin: 12px 0px 12px 0;
                border-radius: 0px;}
            QScrollBar::handle:vertical {
                background: #17202b;
                min-height: 25px;
                border-radius: 0px}
            QScrollBar::add-line:vertical {
                border: none;
                background: rgb(55, 63, 77);
                height: 12px;
                background-image: url(icons:light/cil-arrow-bottom-12.png);
                border-bottom-left-radius: 0px;
                border-bottom-right-radius: 0px;
                subcontrol-position: bottom;
                subcontrol-origin: margin;}

            QScrollBar::sub-line:vertical {
                border: none;
                background: rgb(55, 63, 77);
                height: 12px;
                background-image: url(icons:light/cil-arrow-top-12.png);
                border-top-left-radius: 0px;
                border-top-right-radius: 0px;
                subcontrol-position: top;
                subcontrol-origin: margin;}

            QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
                background: none;}

            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;}"""
        return stylesheet

    def style_radio_button(self):
        if self.theme == "light":
            stylesheet = """
            QRadioButton {
                color: rgb(0, 0, 0);}

            QRadioButton::indicator {
                color: rgb(0, 0, 0);
                border: 2px solid rgb(52, 59, 72);
                width: 12px;
                height: 12px;
                border-radius: 8px;
                background: rgb(44, 49, 60);}

            QRadioButton::indicator:hover {
                border: 2px solid rgb(58, 66, 81);}

            QRadioButton::indicator:checked {
                background: 2px solid rgb(52, 59, 72);
                border: 2px solid rgb(52, 59, 72);
                background-image: url(icons:light/cil-check-alt-12.png);} """
        else:
            stylesheet = """
            QRadioButton {
                color: rgb(255, 255, 255);}

            QRadioButton::indicator {
                border: 2px solid rgb(52, 59, 72);
                width: 12px;
                height: 12px;
                border-radius: 8px;
                background: rgb(44, 49, 60);}

            QRadioButton::indicator:hover {
                border: 2px solid rgb(58, 66, 81);}

            QRadioButton::indicator:checked {
                background: 2px solid rgb(52, 59, 72);
                border: 2px solid rgb(52, 59, 72);
                background-image: url(icons:light/cil-check-alt-12.png);} """
        return stylesheet

    def style_slider(self):
        if self.theme == "light":
            stylesheet = """
            QSlider::groove:horizontal {
                    height: 10px;
                    margin: 0px;
                    background-color: rgb(52, 59, 72);}

            QSlider::groove:horizontal:hover {
                background-color: rgb(55, 62, 76);}

            QSlider::handle:horizontal {
                background-color: rgb(189, 147, 249);
                border: none;
                height: 10px;
                width: 15px;
                margin: 0px;}

            QSlider::handle:horizontal:hover {
                background-color: rgb(195, 155, 255);}

            QSlider::handle:horizontal:pressed {
                background-color: rgb(255, 121, 198);}"""

        else:
            stylesheet = """
            QSlider::groove:horizontal {
                border-radius: 0px;
                height: 10px;
                margin: 0px;
                background-color: rgb(52, 59, 72);}

            QSlider::groove:horizontal:hover {
                background-color: rgb(55, 62, 76);}

            QSlider::handle:horizontal {
                background-color: rgb(189, 147, 249);
                border: none;
                height: 10px;
                width: 15px;
                margin: 0px;
                border-radius: 0px;}

            QSlider::handle:horizontal:hover {
                background-color: rgb(195, 155, 255);}

            QSlider::handle:horizontal:pressed {
                background-color: rgb(255, 121, 198);} """
        return stylesheet

    def style_checkbox(self):
        if self.theme == "light":
            stylesheet = """
            QCheckBox {
                color: rgb(0, 0, 0);
                font: 10pt "Segoe UI";
                }

            QCheckBox::indicator {
                border: 2px solid rgb(52, 59, 72);
                width: 10px;
                height: 10px;
                border-radius: 5px;
                background: rgb(44, 49, 60);}

            QCheckBox::indicator:hover {
                border: 2px solid rgb(58, 66, 81);}

            QCheckBox::indicator:checked {
                background: 2px solid rgb(52, 59, 72);
                border: 2px solid rgb(52, 59, 72);
                background-image: url(icons:light/cil-check-alt-12.png) contain;} """

        else:
            stylesheet = """
            QCheckBox {
                color: rgb(255, 255, 255);
                font: 10pt "Segoe UI";
                }

            QCheckBox::indicator {
                border: 2px solid rgb(255, 255, 255);
                width: 10px;
                height: 10px;
                border-radius: 5px;
                background: rgb(180, 180, 180);}

            QCheckBox::indicator:hover {
                border: 2px solid rgb(180, 180, 180);
                background: rgb(255, 255, 255);}

            QCheckBox::indicator:checked {
                background: 2px solid rgb(180, 180, 180);
                border: 2px solid rgb(255, 255, 255);
                background-image: url(icons:check-12.svg);} """
        return stylesheet

    def style_spinbox(self):
        if self.theme == "light":
            stylesheet = """
            QSpinBox{
                color: rgb(0, 0, 0);
                border-radius: 3px;
                border: 2px solid rgb(200, 200, 200);
                padding: 2px;
                padding-left:5px;
                font: 9pt "Segoe UI";
            }

            QSpinBox::hover{
                border: 2px solid rgb(52, 59, 72);
            }

            QSpinBox::up-button {
                subcontrol-origin: padding;
                subcontrol-position: top right;

                width: 12px;
                height: 10px;
                background-image: url(icons:chevron-up-12.svg);
                border-left-width: 1px;
                border-left-color: rgb(200,200,200);
                border-left-style: solid;
            }

            QSpinBox::down-button {
                subcontrol-origin: padding;
                subcontrol-position: bottom right;
                width: 12px;
                height: 10px;
                background-image: url(icons:chevron-down-12.svg);
                border-left-width: 1px;
                border-left-color: rgb(200,200,200);
                border-left-style: solid;
            }"""
        else:
            stylesheet = """
            QSpinBox{
                color: rgb(255, 255, 255);
                background-color: rgb(27, 29, 35);
                border-radius: 3px;
                border: 2px solid rgb(52, 59, 72);
                padding: 2px;
                padding-left:7px;
                font: 8pt "Segoe UI";
            }

            QSpinBox::hover{
                border: 2px solid rgb(82, 94, 88);
            }

            QSpinBox::up-button {
                subcontrol-origin: padding;
                subcontrol-position: top right;

                width: 13px;
                height: 10px;
                background-image: url(icons:light/cil-arrow-top-12.png);
                border-left-width: 1px;
                border-left-color: rgb(52, 59, 72);
                border-left-style: solid;
            }

            QSpinBox::down-button {
                subcontrol-origin: padding;
                subcontrol-position: bottom right;
                width: 13px;
                height: 10px;
                background-image: url(icons:light/cil-arrow-bottom-12.png);
                border-left-width: 1px;
                border-left-color: rgb(52, 59, 72);
                border-left-style: solid;
            }"""
        return stylesheet

    def style_double_spin_box(self):
        if self.theme == "light":
            stylesheet = """
            QDoubleSpinBox{
                color: rgb(0, 0, 0);
                border-radius: 3px;
                border: 2px solid rgb(200, 200, 200);
                padding: 2px;
                padding-left:2px;
                font: 8pt "Segoe UI";
            }

            QDoubleSpinBox::hover{
                border: 2px solid rgb(52, 59, 72);
            }

            QDoubleSpinBox::up-button {
                subcontrol-origin: padding;
                subcontrol-position: top right;

                width: 12px;
                height: 10px;
                background-image: url(icons:chevron-up-12.svg);
                border-left-width: 1px;
                border-left-color: rgb(200,200,200);
                border-left-style: solid;
            }

            QDoubleSpinBox::down-button {
                subcontrol-origin: padding;
                subcontrol-position: bottom right;
                width: 12px;
                height: 10px;
                background-image: url(icons:chevron-down-12.svg);
                border-left-width: 1px;
                border-left-color: rgb(200,200,200);
                border-left-style: solid;
            }"""
        else:
            stylesheet = """
            QDoubleSpinBox{
                color: rgb(255, 255, 255);
                background-color: rgb(27, 29, 35);
                border-radius: 3px;
                border: 2px solid rgb(52, 59, 72);
                padding: 2px;
                padding-left:2px;
                font: 8pt "Segoe UI";
            }

            QDoubleSpinBox::hover{
                border: 2px solid rgb(82, 94, 88);
            }

            QDoubleSpinBox::up-button {
                subcontrol-origin: padding;
                subcontrol-position: top right;

                width: 13px;
                height: 10px;
                background-image: url(icons:light/cil-arrow-top-12.png);
                border-left-width: 1px;
                border-left-color: rgb(52, 59, 72);
                border-left-style: solid;
            }

            QDoubleSpinBox::down-button {
                subcontrol-origin: padding;
                subcontrol-position: bottom right;
                width: 13px;
                height: 10px;
                background-image: url(icons:light/cil-arrow-bottom-12.png);

                border-left-width: 1px;
                border-left-color: rgb(52, 59, 72);
                border-left-style: solid;
            }
            """
        return stylesheet

    def style_line_edit(self):
        if self.theme == "light":
            stylesheet = """
                QLineEdit {
                    background-color: rgb(255, 255, 255);
                    border-radius: 2px;
                    border : 1px solid rgb(20, 25, 20);
                    color: rgb(30, 30, 30);
                }
                QLineEdit::hover{
                    border: 1px solid rgb(82, 94, 88);
                }
            """
        else:
            stylesheet = """
                QLineEdit {
                    background-color: #17202b;
                    border-radius: 2px;
                    border : 1px solid #394150;
                    color: rgb(255, 255, 255);
                }
                QLineEdit::hover{
                    border: 1px solid rgb(82, 94, 88);
                }
            """
        return stylesheet
