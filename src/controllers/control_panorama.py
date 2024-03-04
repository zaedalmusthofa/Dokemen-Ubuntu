import os
import yaml


class PanoramaConfig(object):
    def __init__(self, main_ui):
        """Initializes a new instance of the PanoramaConfig class.

        Args:
            main_ui (object): Main UI object.
        """
        self.ui = main_ui
        path_file = os.path.normpath(os.getcwd() + os.sep + os.pardir)
        self.__cached_file = path_file + "/src/models/cached/cache_config.yaml"
        with open(self.__cached_file, "r") as file:
            self.__panorama_config = yaml.safe_load(file)

    def _block_signal(self, controls):
        """
        Blocks the signals of the given controls.

        Args:
            controls: A list of PyQt controls whose signals should be blocked.

        Returns:
            None

        Raises:
            None
        """
        for control in controls:
            control.blockSignals(True)

    def _unblock_signal(self, controls):
        """
        Unblocks the signals of the given controls.

        Args:
            controls: A list of PyQt controls whose signals should be unblocked.

        Returns:
            None

        Raises:
            None
        """
        for control in controls:
            control.blockSignals(False)

    def block_signal_pano_tube(self):
        """Block signals for panoptic tube spin boxes and double spin boxes.
        This method blocks signals for the following spin boxes and double spin boxes:
        - self.ui.doubleSpinBox_pano_tube_alpha_min
        - self.ui.doubleSpinBox_pano_tube_alpha_max
        - self.ui.doubleSpinBox_pano_tube_crop_top
        - self.ui.doubleSpinBox_pano_tube_crop_buttom

        This method is intended to be used to avoid emitting signals when changing the values of the panoptic tube spin boxes and double spin boxes programmatically.

        Args:
            self: An instance of the class containing this method.

        Returns:
            None


        """
        self._block_signal(
            [
                self.ui.doubleSpinBox_pano_tube_alpha_min,
                self.ui.doubleSpinBox_pano_tube_alpha_max,
                self.ui.doubleSpinBox_pano_tube_crop_top,
                self.ui.doubleSpinBox_pano_tube_crop_buttom
            ]
        )

    def unblock_signal_pano_tube(self):
        """Unblocks the signals for the pano tube settings widgets.

        This function calls the _unblock_signal method to unblock the signals for the pano tube settings widgets.

            Args:
                None.

            Returns:
                None.

            Raises:
                None.

            """
        self._unblock_signal(
            [
                self.ui.doubleSpinBox_pano_tube_alpha_min,
                self.ui.doubleSpinBox_pano_tube_alpha_max,
                self.ui.doubleSpinBox_pano_tube_crop_top,
                self.ui.doubleSpinBox_pano_tube_crop_buttom
            ]
        )

    def block_signal_pano_car(self):
        """
        Blocks the signals of certain UI elements related to the panoramic car view.

        Args:
            None

        Returns:
            None
            """
        self._block_signal(
            [
                self.ui.doubleSpinBox_pano_car_alpha,
                self.ui.doubleSpinBox_pano_car_beta,
                self.ui.doubleSpinBox_pano_car_crop_left,
                self.ui.doubleSpinBox_pano_car_crop_right,
                self.ui.doubleSpinBox_pano_car_crop_top,
                self.ui.doubleSpinBox_pano_car_crop_bottom
            ]
        )

    def unblock_signal_pano_car(self):
        """
        Unblocks signals for a set of widgets related to the panoramic car view.

        This function unblocks signals for the following widgets: doubleSpinBox_pano_car_alpha,
        doubleSpinBox_pano_car_beta, doubleSpinBox_pano_car_crop_left, doubleSpinBox_pano_car_crop_right,
        doubleSpinBox_pano_car_crop_top, doubleSpinBox_pano_car_crop_bottom. This allows changes to
        these widgets to trigger the corresponding slots.

        This function is called by the GUI when the user leaves a specific tab or dialog box in the panoramic
        car view.

        Args:
            None.

        Returns:
            None.

        Raises:
            None.


        """
        self._unblock_signal(
            [
                self.ui.doubleSpinBox_pano_car_alpha,
                self.ui.doubleSpinBox_pano_car_beta,
                self.ui.doubleSpinBox_pano_car_crop_left,
                self.ui.doubleSpinBox_pano_car_crop_right,
                self.ui.doubleSpinBox_pano_car_crop_top,
                self.ui.doubleSpinBox_pano_car_crop_bottom
            ]
        )

    def showing_config_panorama_tube(self):
        """Reads the panorama configuration from a YAML file, and populates the relevant UI elements with the values.

        Opens the cached configuration file using the private attribute `__cached_file` as the file path, and reads its
        contents using PyYAML's `safe_load` method. The relevant UI elements are then set to the corresponding values
        found in the configuration file.

        Note:
            This function blocks signals from the UI elements while updating them with the configuration values.

        Raises:
            IOError: If the configuration file cannot be read.

        """
        with open(self.__cached_file, "r") as file:
            self.__panorama_config = yaml.safe_load(file)
        self.block_signal_pano_tube()
        self.ui.doubleSpinBox_pano_tube_alpha_min.setValue(self.__panorama_config["Pano_tube"]["alpha_min"])
        self.ui.doubleSpinBox_pano_tube_alpha_max.setValue(self.__panorama_config["Pano_tube"]["alpha_max"])
        self.ui.doubleSpinBox_pano_tube_crop_top.setValue(self.__panorama_config["Pano_tube"]["crop_top"])
        self.ui.doubleSpinBox_pano_tube_crop_buttom.setValue(self.__panorama_config["Pano_tube"]["crop_bottom"])
        self.unblock_signal_pano_tube()

    def showing_config_panorama_car(self):
        """Loads the panorama car configuration from a cached YAML file and updates the user interface with its values.

        Reads the cached file at `self.__cached_file` using the PyYAML library to parse the YAML content. The parsed
        configuration values are assigned to the instance variable `self.__panorama_config`. Blocks signals from all the
        widgets associated with the car panorama in the user interface to prevent any unintended updates during the UI
        update process. Then, sets the values of the panorama car configuration widgets in the UI with the parsed values
        from the configuration file. Finally, unblocks signals from all the widgets that were previously blocked.

        Returns:
            None
        """
        with open(self.__cached_file, "r") as file:
            self.__panorama_config = yaml.safe_load(file)
        self.block_signal_pano_car()
        self.ui.doubleSpinBox_pano_car_alpha.setValue(self.__panorama_config["Pano_car"]["alpha"])
        self.ui.doubleSpinBox_pano_car_beta.setValue(self.__panorama_config["Pano_car"]["beta"])
        self.ui.doubleSpinBox_pano_car_crop_left.setValue(self.__panorama_config["Pano_car"]["crop_left"])
        self.ui.doubleSpinBox_pano_car_crop_right.setValue(self.__panorama_config["Pano_car"]["crop_right"])
        self.ui.doubleSpinBox_pano_car_crop_top.setValue(self.__panorama_config["Pano_car"]["crop_top"])
        self.ui.doubleSpinBox_pano_car_crop_bottom.setValue(self.__panorama_config["Pano_car"]["crop_bottom"])
        self.unblock_signal_pano_car()

    def change_properties_panorama_tube(self):
        """Change the properties of the panorama tube.

        Reads the new values for alpha_min, alpha_max, crop_top, and crop_bottom from the
        corresponding UI elements, and updates the __panorama_config dictionary with the new
        values if they meet certain criteria. Then writes the updated dictionary to a YAML file.

        Args:
            self: An instance of the class.

        Returns:
            None.
        """
        alpha_min = self.ui.doubleSpinBox_pano_tube_alpha_min.value()
        alpha_max = self.ui.doubleSpinBox_pano_tube_alpha_max.value()
        crop_top = round(self.ui.doubleSpinBox_pano_tube_crop_top.value(), 3)
        crop_bottom = round(self.ui.doubleSpinBox_pano_tube_crop_buttom.value(), 3)

        if alpha_min < alpha_max - 10:
            self.__panorama_config["Pano_tube"]["alpha_min"] = alpha_min
        if alpha_max > alpha_min + 10:
            self.__panorama_config["Pano_tube"]["alpha_max"] = alpha_max
        if crop_top < crop_bottom - 0.2:
            self.__panorama_config["Pano_tube"]["crop_top"] = crop_top
        if crop_bottom > crop_top + 0.2:
            self.__panorama_config["Pano_tube"]["crop_bottom"] = crop_bottom

        with open(self.__cached_file, "w") as outfile:
            yaml.dump(self.__panorama_config, outfile, default_flow_style=False)

    def change_properties_panorama_car(self):
        """Updates the properties of the car panorama and saves them to a YAML file.

        Args:
            None

        Returns:
            None

        Raises:
            None

        Note:
            Updates the alpha and beta properties of the car panorama from the GUI spinboxes.
            Updates the crop_left, crop_right, crop_top, and crop_bottom properties of the car panorama from the GUI double spinboxes.
            Saves the updated panorama configuration to a YAML file specified in `self.__cached_file`.

        """
        self.__panorama_config["Pano_car"]["alpha"] = self.ui.doubleSpinBox_pano_car_alpha.value()
        self.__panorama_config["Pano_car"]["beta"] = self.ui.doubleSpinBox_pano_car_beta.value()

        crop_left = round(self.ui.doubleSpinBox_pano_car_crop_left.value(), 3)
        crop_right = round(self.ui.doubleSpinBox_pano_car_crop_right.value(), 3)
        crop_top = round(self.ui.doubleSpinBox_pano_car_crop_top.value(), 3)
        crop_bottom = round(self.ui.doubleSpinBox_pano_car_crop_bottom.value(), 3)

        if crop_left < crop_right: # - 0.25:
            self.__panorama_config["Pano_car"]["crop_left"] = crop_left

        if crop_right > crop_left: # + 0.25:
            self.__panorama_config["Pano_car"]["crop_right"] = crop_right

        if crop_top < crop_bottom: # - 0.25:
            self.__panorama_config["Pano_car"]["crop_top"] = crop_top

        if crop_bottom > crop_top: # + 0.25:
            self.__panorama_config["Pano_car"]["crop_bottom"] = crop_bottom

        with open(self.__cached_file, "w") as outfile:
            yaml.dump(self.__panorama_config, outfile, default_flow_style=False)
