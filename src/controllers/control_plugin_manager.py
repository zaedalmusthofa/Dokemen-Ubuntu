import os
import re
import shutil
import sys
import cv2
import yaml
from PyQt6 import QtWidgets, QtGui, QtCore
from pathlib import Path
from .control_plugin_collection import PluginCollection


class PluginManager(object):
    def __init__(self, main_control):
        """Initializes the PluginManager object.

        Args:
            main_control: A reference to the main control object.

        Attributes:
            main_control: A reference to the main control object.
            plugin: A PluginCollection object that manages the plugins.
            apps_activated: A list of booleans indicating whether each plugin is activated.
            index: An integer representing the index of the currently selected plugin.
        """
        super().__init__()
        self.main_control = main_control
        self.plugin = PluginCollection("plugins")
        self.apps_activated = None
        self.index = None
        self.widget = None
        self.text_title = None
        self.init_available_plugin()
        self.init_cached_file()
        self.connect_to_event()

    def connect_to_event(self):
        """
        Connects the main window buttons to their corresponding actions.

        This method is responsible for setting up event connections between the buttons in the main window and their corresponding actions. Specifically, the following connections are established:

        - When the "Add Plugins" button is clicked, the `install_new_plugin` method is called.
        - When the "Delete Plugins" button is clicked, the `action_delete_apps` method is called.
        - When the "Close" button is clicked, the `main_control.back_to_home` method is called.
        - When the "Help" button is clicked, the `help_menu_plugin` method is called.
        Note: You should replace the description of the actions to match their actual functionality.

        """
        # self.main_control.ui.add_plugins_button.clicked.connect(self.install_new_plugin)
        self.main_control.ui.delete_plugins_button.clicked.connect(self.action_delete_apps)
        self.main_control.ui.close_plugin_button.clicked.connect(self.main_control.back_to_home)
        self.main_control.ui.help_plugins_button.clicked.connect(self.help_menu_plugin)
        self.main_control.ui.open_in_new_window_plugins.clicked.connect(self.open_plugins_in_new_window)

    def init_cached_file(self):
        file_path = os.path.join(os.getcwd(), "models", "cached", "plugin_cached.yaml")
        if not os.path.exists(file_path):
            config = {"plugin_run": None}
            with open(file_path, "w") as outfile:
                yaml.dump(config, outfile)

    def init_available_plugin(self):
        """Initializes the available plugins by adding buttons for each one to the UI.

        Clears any existing buttons from the UI layout, then iterates over the list of available plugins
        and adds a button for each one. The icon for each plugin is retrieved using the `get_icon_` method
        of the `PluginCollection` object.

        Returns:
            None
        """
        self.main_control.ui.add_plugins_button.hide()
        for i in range(self.main_control.ui.layout_application.count()):
            self.main_control.ui.layout_application.itemAt(i).widget().close()

        for i in range(len(self.plugin.name_application)):
            icon = self.plugin.get_icon_(i)
            button = self.add_btn_apps_plugin(icon, self.plugin.name_application[i])
            button.clicked.connect(self.open_plugin_apps)
            self.main_control.ui.layout_application.addWidget(button)

    def install_new_plugin(self):
        """Opens a file dialog for selecting a new plugin folder and installs it into the plugin store.

        Args:
            None

        Returns:
            None

        Raises:
            None
        """
        options = QtWidgets.QFileDialog.Option.DontUseNativeDialog
        dir_plugin = QtWidgets.QFileDialog.getExistingDirectory(None,
                                                                'Select Application Folder', "../plugin_store", options)
        if dir_plugin:
            original = dir_plugin
            name_plug = os.path.basename(os.path.normpath(original))
            path_file = os.path.dirname(os.path.realpath(__file__))
            target = path_file + '/plugins/'
            name_exist = Path(target + name_plug)
            if name_exist.exists():
                QtWidgets.QMessageBox.warning(None, "Warning !!", "Plugins already exist!!")
            else:
                listApp = self.plugin.name_application
                self.main_control.model.copy_directory(original, target)
                self.plugin.reload_plugins()
                newList = self.plugin.name_application
                name = [item for item in newList if item not in listApp]

                def listToString(listIn):
                    return " ".join(listIn)

                index = newList.index(listToString(name))
                icon = self.plugin.get_icon_(index)
                button = self.add_btn_apps_plugin(icon, self.plugin.name_application[index])
                button.clicked.connect(self.open_plugin_apps)
                self.main_control.ui.layout_application.addWidget(button)
                self.pop_up_message_box("Plugins was successfully added!!")

    def add_plugin_by_github(self, name):
        # path_file = os.path.dirname(os.path.realpath(__file__))
        path_file = os.path.abspath(".")
        target = path_file + '/plugins/'
        name_exist = Path(target + name)
        if name_exist.exists():
            QtWidgets.QMessageBox.warning(None, "Warning !!", "Plugins already exist!!")
            return False

        else:
            return True

    def refresh_the_plugin_available(self):
        listApp = self.plugin.name_application
        self.plugin.reload_plugins()
        newList = self.plugin.name_application
        name = [item for item in newList if item not in listApp]

        def listToString(listIn):
            return " ".join(listIn)

        index = newList.index(listToString(name))
        icon = self.plugin.get_icon_(index)
        button = self.add_btn_apps_plugin(icon, self.plugin.name_application[index])
        button.clicked.connect(self.open_plugin_apps)
        self.main_control.ui.layout_application.addWidget(button)
        self.pop_up_message_box("Plugins was successfully added!!")

    def refresh_theme_widget(self):
        """
        Refreshes the theme of the currently selected plugin widget, if any.
        Returns:
            None
        """
        if self.index is not None:
            self.plugin.change_theme(self.index)

    def open_pinned_plugin(self, index):
        try:
            self.index = index
            self.main_control.ui.delete_plugins_button.show()
            self.main_control.ui.close_plugin_button.show()
            for i in range(self.main_control.ui.layout_plugin.count()):
                self.main_control.ui.layout_plugin.itemAt(i).widget().close()

            self.widget = self.plugin.get_widget(self.index, self.main_control.model)
            self.main_control.ui.layout_plugin.addWidget(self.widget)
            self.main_control.ui.widget_container_content.setCurrentIndex(1)
            self.main_control.ui.frame_btn_moilapp.hide()
            self.main_control.ui.frame_button_view.hide()
            self.main_control.ui.label_plugin_name.show()
            self.main_control.ui.open_in_new_window_plugins.show()
            self.text_title = ' '.join(''.join(sent) for sent in re.findall('.[^A-Z]*',
                                                                            self.plugin.name_application[self.index]))
            if self.text_title is not None or self.text_title != "":
                self.main_control.ui.label_plugin_name.setText(self.text_title)
            self.apps_activated = self.plugin.name_application[self.index]

        except:
            file_path = os.path.join(os.getcwd(), "models", "cached", "plugin_cached.yaml")
            with open(file_path, "r") as file:
                config = yaml.safe_load(file)
            config["plugin_run"] = None
            with open(file_path, "w") as outfile:
                yaml.dump(config, outfile, default_flow_style=False)
            self.main_control.ui.delete_plugins_button.hide()
            self.main_control.ui.label_plugin_name.hide()
            self.main_control.ui.close_plugin_button.hide()
            self.main_control.ui.open_in_new_window_plugins.hide()
            self.index = None

    def open_plugin_apps(self):
        """
        Opens the selected plugin application and displays its widget in the plugin layout.

        Raises:
            IndexError: If the selected plugin index is not found in `self.plugin.name_application`.

        Side Effects:
            - Sets `self.index` to the index of the selected plugin.
            - Shows the "Delete Plugins" and "Close Plugin" buttons in the main control UI.
            - Closes all widgets in the plugin layout before adding the selected plugin's widget.
            - Changes the current widget container to the plugin layout.
            - Hides the "MOIL App" and "View" buttons in the main control UI.
            - Sets `self.apps_activated` to the selected plugin's name.

        """
        button = self.main_control.sender()
        # button.setStyleSheet("background-color: rgb(25,25,25)")
        index = self.plugin.name_application.index(button.objectName())
        if index != self.index:
            self.index = self.plugin.name_application.index(button.objectName())
            self.main_control.ui.delete_plugins_button.show()
            self.main_control.ui.close_plugin_button.show()
            self.main_control.ui.add_plugins_button.hide()
            for i in range(self.main_control.ui.layout_plugin.count()):
                self.main_control.ui.layout_plugin.itemAt(i).widget().close()

            if self.plugin.set_always_pop_up(self.index):
                self.open_plugins_in_new_window()

            else:
                self.widget = self.plugin.get_widget(self.index, self.main_control.model)
                self.main_control.ui.layout_plugin.addWidget(self.widget)
                self.main_control.ui.widget_container_content.setCurrentIndex(1)
                self.main_control.ui.frame_btn_moilapp.hide()
                self.main_control.ui.frame_button_view.hide()
                self.main_control.ui.label_plugin_name.show()
                self.main_control.ui.open_in_new_window_plugins.show()
                self.text_title = ' '.join(''.join(sent) for sent in re.findall('.[^A-Z]*', button.objectName()))
                if self.text_title is not None or self.text_title != "":
                    self.main_control.ui.label_plugin_name.setText(self.text_title)
                self.apps_activated = button.objectName()
                file_path = os.path.join(os.getcwd(), "models", "cached", "plugin_cached.yaml")
                with open(file_path, "r") as file:
                    config = yaml.safe_load(file)
                config["plugin_run"] = self.index
                with open(file_path, "w") as outfile:
                    yaml.dump(config, outfile, default_flow_style=False)

        else:
            self.widget.raise_()
            if self.widget.isMinimized():
                self.widget.showMaximized()

            QtWidgets.QMessageBox.information(None, "Information", "Plugins already opened!!")

    def open_plugins_in_new_window(self):
        self.main_control.ui.add_plugins_button.show()
        self.main_control.ui.stackedWidget_2.setCurrentIndex(0)
        for i in range(self.main_control.ui.layout_plugin.count()):
            self.main_control.ui.layout_plugin.itemAt(i).widget().close()

        self.widget = self.plugin.get_widget(self.index, self.main_control.model)

        def close_event(event):
            msgBox = QtWidgets.QMessageBox(None)
            reply = msgBox.question(None, 'Quit', 'Are you sure you want to quit?',
                                    QtWidgets.QMessageBox.StandardButton.Yes |
                                    QtWidgets.QMessageBox.StandardButton.No,
                                    QtWidgets.QMessageBox.StandardButton.No)

            if reply == QtWidgets.QMessageBox.StandardButton.Yes:
                event.accept()
                self.index = None
            else:
                event.ignore()

        # def destroy_window():
        #     reply = QtWidgets.QMessageBox.question(self.widget, 'Quit', 'Are you sure you want to quit?',
        #                                            QtWidgets.QMessageBox.StandardButton.Yes |
        #                                            QtWidgets.QMessageBox.StandardButton.No,
        #                                            QtWidgets.QMessageBox.StandardButton.No)
        #     if reply == QtWidgets.QMessageBox.StandardButton.Yes:
        #         self.widget.close()
        #         self.index = None

        # shortcut = QtGui.QShortcut(QtCore.Qt.Key.Key_Escape, self.widget)
        # shortcut.activated.connect(close_event)

        self.widget.closeEvent = close_event
        self.widget.setWindowTitle(self.text_title)
        self.widget.show()
        self.main_control.ui.widget_container_content.setCurrentIndex(0)
        self.main_control.ui.frame_btn_moilapp.show()
        self.main_control.ui.frame_button_view.show()
        self.main_control.ui.delete_plugins_button.hide()
        self.main_control.ui.label_plugin_name.hide()
        self.main_control.ui.close_plugin_button.hide()
        self.main_control.ui.open_in_new_window_plugins.hide()

    def add_btn_apps_plugin(self, icon_, name):
        """Create and return a QPushButton widget with an icon and a name.

        Args:
            icon_: A string specifying the path of the icon file.
            name: A string specifying the name of the plugin.

        Returns:
            A QPushButton widget with the specified icon and name.
        """
        button = QtWidgets.QPushButton()
        button.setObjectName(name)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(button.sizePolicy().hasHeightForWidth())
        button.setSizePolicy(sizePolicy)
        button.setMinimumSize(QtCore.QSize(40, 25))
        button.setMaximumSize(QtCore.QSize(35, 16777215))
        text_title = ' '.join(''.join(sent) for sent in re.findall('.[^A-Z]*', name))
        button.setToolTip(text_title)
        button.setStatusTip(text_title)
        button.setIconSize(QtCore.QSize(30, 30))

        if icon_ is not None:
            if self.main_control.model.theme == "light":
                icon = QtGui.QIcon(icon_)
                button.setIcon(icon)
            else:
                # auto generate invert color image under developing
                icon = QtGui.QIcon(icon_)
                button.setIcon(icon)
        return button

    def action_delete_apps(self):
        """
        Deletes the currently activated plugin application.

        Args:
            None

        Returns:
            None

        Raises:
            None
        """
        index = self.plugin.name_application.index(self.apps_activated)
        self.delete_apps(index)

    def delete_apps(self, index):
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
        name = self.plugin.name_application[index]
        path = self.plugin.path_folder[index]
        path = path.split(".")[1]

        # path_file = os.path.dirname(os.path.realpath(__file__))
        path_file = os.path.abspath(".")
        path = path_file + '/plugins/' + path

        with open(os.path.join(os.getcwd(), "models", "cached", "plugin_cached.yaml"), "r") as file:
            config = yaml.safe_load(file)
        config["plugin_run"] = None
        with open(os.path.join(os.getcwd(), "models", "cached", "plugin_cached.yaml"), "w") as outfile:
            yaml.dump(config, outfile, default_flow_style=False)

        reply = QtWidgets.QMessageBox.question(None, 'Message',
                                               "Are you sure want to delete \n" +
                                               name + " application ?\n",
                                               QtWidgets.QMessageBox.StandardButton.Yes |
                                               QtWidgets.QMessageBox.StandardButton.No,
                                               QtWidgets.QMessageBox.StandardButton.No)

        if reply == QtWidgets.QMessageBox.StandardButton.Yes:
            self.remove_plugin_folder(path)
            self.plugin.reload_plugins()
            self.init_available_plugin()
            self.pop_up_message_box("Plugins was successfully deleted !!")
            self.main_control.back_to_home()

    def remove_plugin_folder(self, path):
        try:
            shutil.rmtree(path, ignore_errors=False, onerror=self.handle_remove_readonly)
        except FileNotFoundError:
            print(f"Folder not found: {path}")
        except Exception as e:
            print(f"Error occurred while deleting folder: {e}")

    @classmethod
    def handle_remove_readonly(cls, func, path, _):
        import stat
        # Clear the read-only attribute and attempt to delete the file again
        os.chmod(path, stat.S_IWRITE)
        func(path)

    def help_menu_plugin(self):
        """Displays a help message for the currently selected plugin in a pop-up box.

        If the currently selected widget is the home screen, displays a generic message.
        Otherwise, displays a message that includes the plugin's description.

        Returns:
            None
        """
        if self.main_control.ui.widget_container_content.currentIndex() == 0:
            message = "Help menu plugin under development \n" \
                      "we Will inform you after finish!!\n"

        else:
            print(self.plugin.get_description(self.index))
            message = "Help menu plugin under development \n" \
                      "we Will inform you after finish!!\n\n" \
                      "Note App: " + self.plugin.get_description(self.index)
        self.pop_up_message_box(message)

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
        msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
        msg.setStyleSheet("font-family: Segoe UI; font-size:14px;")
        msg.setWindowTitle("Information")
        # setting message for Message Box
        msg.setText("Information !! \n\n" + message)
        msg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        msg.show()

        def close_msg():
            msg.done(0)

        QtCore.QTimer.singleShot(6000, close_msg)
