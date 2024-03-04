from PyQt6 import QtGui, QtCore, QtWidgets
import os


class SetIconsUI:
    def __init__(self, main_ui):
        """Initialize the MoilApp object with the given main_ui object.

        Args:
            main_ui: A reference to the main user interface object of the application.

        Returns:
            None.
        """
        super().__init__()
        self.ui = main_ui
        self.__realpath = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
        CURRENT_DIRECTORY = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
        QtCore.QDir.addSearchPath("icons", CURRENT_DIRECTORY + "/icons")

        self.ui.label_result.setPixmap(QtGui.QPixmap("icons:moilapp.png"))
        self.ui.frame_image_original.setMinimumSize(QtCore.QSize(0, 200))
        self.ui.label_image_original.setPixmap(QtGui.QPixmap("icons:moilapp.png"))

        label = QtWidgets.QLabel()
        label.setText("  MoilApp v4.1 (c) 2024  ")
        self.ui.statusBar.addPermanentWidget(label)

    def get_theme_main_apps(self, theme):
        """Sets the color theme for the main window of the application.

        Args:
            theme (str): The color theme to apply. Should be either "dark" or "light".
        """
        if theme == "dark":
            self.dark_mode_there()
        else:
            self.light_mode_theme()

    def dark_mode_there(self):
        """Set the UI to dark mode by changing the icons and logo to dark mode.

        This function sets the icons of the UI buttons to the dark mode icons and
        the logo to the dark mode logo. It is called when the user switches the
        UI to the dark mode.
        """
        self.ui.label_logo.setPixmap(QtGui.QPixmap("icons:moil.png"))
        self.ui.label_logo.setScaledContents(True)

        self.ui.extra_left_close_button.setIcon(QtGui.QIcon("icons:light/cil-x.png"))

        self.ui.rotate_left_button.setIcon(QtGui.QIcon("icons:light/rotate-ccw.png"))
        self.ui.rotate_right_button.setIcon(QtGui.QIcon("icons:light/rotate-cw.png"))
        self.ui.zoom_out_button.setIcon(QtGui.QIcon("icons:light/minus.png"))
        self.ui.zoom_in_button.setIcon(QtGui.QIcon("icons:light/plus.png"))
        self.ui.reset_view_button.setIcon(QtGui.QIcon("icons:light/reset.png"))
        self.ui.open_in_new_window_plugins.setIcon(QtGui.QIcon("icons:light/new_window.png"))
        self.ui.add_plugins_button.setIcon(QtGui.QIcon("icons:light/plugin.png"))
        self.ui.delete_plugins_button.setIcon(QtGui.QIcon("icons:light/trash.png"))
        self.ui.close_plugin_button.setIcon(QtGui.QIcon("icons:light/logout.png"))
        self.ui.help_plugins_button.setIcon(QtGui.QIcon("icons:light/help.png"))

        self.ui.pushButton_any_up.setText("")
        self.ui.btn_record_screen.setIcon(QtGui.QIcon("icons:light/record-screen.png"))
        self.ui.btn_about_us.setIcon(QtGui.QIcon("icons:light/user.png"))

        self.ui.play_pause_button.setIcon(QtGui.QIcon("icons:light/play.png"))
        self.ui.rewind_button.setIcon(QtGui.QIcon("icons:light/rewind.png"))
        self.ui.stop_button.setIcon(QtGui.QIcon("icons:light/square.png"))
        self.ui.forward_button.setIcon(QtGui.QIcon("icons:light/forward.png"))
        self.ui.screenshoot_button.setIcon(QtGui.QIcon("icons:light/maximize.png"))
        self.ui.record_button.setIcon(QtGui.QIcon("icons:light/video.png"))

        self.ui.pushButton_any_up.setIcon(QtGui.QIcon("icons:light/up.png"))
        self.ui.pushButton_any_left.setIcon(QtGui.QIcon("icons:light/left.png"))
        self.ui.pushButton_any_right.setIcon(QtGui.QIcon("icons:light/right.png"))
        self.ui.pushButton_any_bottom.setIcon(QtGui.QIcon("icons:light/down.png"))
        self.ui.pushButton_any_center.setIcon(QtGui.QIcon("icons:light/center.png"))

    def light_mode_theme(self):
        """Changes the application's icons to a light theme.

        Args:
            None

        Returns:
            None
        """
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons:github.svg"), QtGui.QIcon.Mode.Normal,
                       QtGui.QIcon.State.Off)
        self.ui.github_button.setIcon(icon)

        self.ui.label_logo.setPixmap(QtGui.QPixmap("icons:moil.png"))
        self.ui.label_logo.setScaledContents(True)

        self.ui.label_10.setPixmap(QtGui.QPixmap("icons:mouse-pointer.png"))
        self.ui.label_10.setScaledContents(True)
        self.ui.label_19.setPixmap(QtGui.QPixmap("icons:mouse-pointer.png"))
        self.ui.label_19.setScaledContents(True)

        self.ui.extra_left_close_button.setIcon(QtGui.QIcon("icons:x.svg"))

        self.ui.rotate_left_button.setIcon(QtGui.QIcon("icons:rotate-ccw.svg"))
        self.ui.rotate_right_button.setIcon(QtGui.QIcon("icons:rotate-cw.svg"))
        self.ui.zoom_out_button.setIcon(QtGui.QIcon("icons:minus.svg"))
        self.ui.zoom_in_button.setIcon(QtGui.QIcon("icons:plus.svg"))

        self.ui.reset_view_button.setIcon(QtGui.QIcon("icons:reset.png"))
        self.ui.close_plugin_button.setIcon(QtGui.QIcon("icons:logout.png"))

        self.ui.btn_record_screen.setText("")
        self.ui.btn_record_screen.setIcon(QtGui.QIcon("icons:record-screen_black.png"))
        self.ui.btn_about_us.setIcon(QtGui.QIcon("icons:user.svg"))

        self.ui.open_in_new_window_plugins.setIcon(QtGui.QIcon("icons:new_window.png"))
        self.ui.add_plugins_button.setIcon(QtGui.QIcon("icons:plugins.png"))
        self.ui.delete_plugins_button.setIcon(QtGui.QIcon("icons:trash.svg"))
        self.ui.help_plugins_button.setIcon(QtGui.QIcon("icons:info.svg"))

        self.ui.play_pause_button.setIcon(QtGui.QIcon("icons:play.svg"))
        self.ui.rewind_button.setIcon(QtGui.QIcon("icons:rewind.svg"))
        self.ui.stop_button.setIcon(QtGui.QIcon("icons:square.svg"))
        self.ui.forward_button.setIcon(QtGui.QIcon("icons:forward.svg"))
        self.ui.screenshoot_button.setIcon(QtGui.QIcon("icons:maximize.svg"))
        self.ui.record_button.setIcon(QtGui.QIcon("icons:video.svg"))

        self.ui.pushButton_any_up.setText("")
        self.ui.pushButton_any_up.setIcon(QtGui.QIcon("icons:up.png"))
        self.ui.pushButton_any_left.setText("")
        self.ui.pushButton_any_left.setIcon(QtGui.QIcon("icons:left.png"))
        self.ui.pushButton_any_right.setText("")
        self.ui.pushButton_any_right.setIcon(QtGui.QIcon("icons:right.png"))
        self.ui.pushButton_any_bottom.setText("")
        self.ui.pushButton_any_bottom.setIcon(QtGui.QIcon("icons:down.png"))
        self.ui.pushButton_any_center.setText("")
        self.ui.pushButton_any_center.setIcon(QtGui.QIcon("icons:center.png"))



