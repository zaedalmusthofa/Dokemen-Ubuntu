import os
import yaml


class AnypointConfig(object):
    def __init__(self, main_ui):
        """Loads an Anypoint configuration file.

        Args:
            main_ui: An instance of the main user interface.

        Attributes:
            ui: An instance of the main user interface.

        Raises:
            FileNotFoundError: If the Anypoint configuration file cannot be found.

        """
        self.ui = main_ui
        path_file = os.path.normpath(os.getcwd() + os.sep + os.pardir)
        self.__cached_file = path_file + "/src/models/cached/cache_config.yaml"
        with open(self.__cached_file, "r") as file:
            self.__anypoint_config = yaml.safe_load(file)

    def __block_signal(self):
        """Blocks signals for alpha, beta, roll, and zoom double spin boxes.

        This function is used to temporarily block signals for the alpha, beta, roll, and zoom double spin boxes
        in the UI. This is useful when the user has changed one of the values programmatically, to prevent the
        signals from being emitted and triggering additional functions.

        Args:
            self: An instance of the class.

        Returns:
            None
        """
        self.ui.doubleSpinBox_alpha.blockSignals(True)
        self.ui.doubleSpinBox_beta.blockSignals(True)
        self.ui.doubleSpinBox_roll.blockSignals(True)
        self.ui.doubleSpinBox_zoom.blockSignals(True)

    def __unblock_signal(self):
        """
        Unblock the signals of the alpha, beta, roll, and zoom double spin boxes in the GUI.

        This function sets the blockSignals property of the following UI double spin boxes to False, which allows them to receive and emit signals:
        - doubleSpinBox_alpha
        - doubleSpinBox_beta
        - doubleSpinBox_roll
        - doubleSpinBox_zoom

        Returns:
            None
        """
        self.ui.doubleSpinBox_alpha.blockSignals(False)
        self.ui.doubleSpinBox_beta.blockSignals(False)
        self.ui.doubleSpinBox_roll.blockSignals(False)
        self.ui.doubleSpinBox_zoom.blockSignals(False)

    def showing_config_mode_1(self):
        """Reads the cached file to load the configuration data for Mode 1.

        This function reads the YAML data from the cached file and loads it into the
        `self.__anypoint_config` attribute. It then sets the values of the zoom, alpha,
        and beta parameters for Mode 1 in the UI double spin boxes. The function blocks
        signals while updating the spin box values to prevent recursive updates. Once the
        values are set, the function unblocks signals.

        Returns:
            None
        """
        with open(self.__cached_file, "r") as file:
            self.__anypoint_config = yaml.safe_load(file)
        self.__block_signal()
        self.ui.doubleSpinBox_zoom.setValue(self.__anypoint_config["Mode_1"]["zoom"])
        self.ui.doubleSpinBox_alpha.setValue(self.__anypoint_config["Mode_1"]["alpha"])
        self.ui.doubleSpinBox_beta.setValue(self.__anypoint_config["Mode_1"]["beta"])
        self.__unblock_signal()

    def showing_config_mode_2(self):
        """Reads the cached file to load the configuration data for Mode 2.

        This function reads the YAML data from the cached file and loads it into the
        `self.__anypoint_config` attribute. It then sets the values of the pitch, yaw,
        roll, and zoom parameters for Mode 2 in the UI double spin boxes. The function
        blocks signals while updating the spin box values to prevent recursive updates.
        Once the values are set, the function unblocks signals.

        Returns:
            None
        """
        with open(self.__cached_file, "r") as file:
            self.__anypoint_config = yaml.safe_load(file)
        self.__block_signal()
        self.ui.doubleSpinBox_alpha.setValue(self.__anypoint_config["Mode_2"]["pitch"])
        self.ui.doubleSpinBox_beta.setValue(self.__anypoint_config["Mode_2"]["yaw"])
        self.ui.doubleSpinBox_roll.setValue(self.__anypoint_config["Mode_2"]["roll"])
        self.ui.doubleSpinBox_zoom.setValue(self.__anypoint_config["Mode_2"]["zoom"])
        self.__unblock_signal()

    def change_properties_mode_1(self):
        """Updates the configuration data for Mode 1 and writes it to the cached file.

        This function updates the alpha, beta, and zoom parameters for Mode 1 using the
        values in the UI double spin boxes. It rounds the zoom value to three decimal places
        before updating the configuration data. The updated configuration data is then
        written to the cached file using YAML format.

        Returns:
            None
        """
        self.__anypoint_config["Mode_1"]["alpha"] = self.ui.doubleSpinBox_alpha.value()
        self.__anypoint_config["Mode_1"]["beta"] = self.ui.doubleSpinBox_beta.value()
        self.__anypoint_config["Mode_1"]["zoom"] = round(self.ui.doubleSpinBox_zoom.value(), 3)
        with open(self.__cached_file, "w") as outfile:
            yaml.dump(self.__anypoint_config, outfile, default_flow_style=False)

    def change_properties_mode_2(self):
        """Updates the configuration data for Mode 2 and writes it to the cached file.

        This function updates the pitch, yaw, roll, and zoom parameters for Mode 2 using the
        values in the UI double spin boxes. It creates a list of tuples to store the control
        names and their corresponding values, and then iterates through the list to update
        the configuration data for each control. The zoom value is rounded to three decimal
        places before updating the configuration data. The updated configuration data is
        then written to the cached file using YAML format.

        Returns:
            None
        """
        controls = [
            ("pitch", self.ui.doubleSpinBox_alpha.value()),
            ("yaw", self.ui.doubleSpinBox_beta.value()),
            ("roll", self.ui.doubleSpinBox_roll.value()),
            ("zoom", round(self.ui.doubleSpinBox_zoom.value(), 3))
        ]

        for key, value in controls:
            self.__anypoint_config["Mode_2"][key] = value

        with open(self.__cached_file, "w") as outfile:
            yaml.dump(self.__anypoint_config, outfile, default_flow_style=False)



