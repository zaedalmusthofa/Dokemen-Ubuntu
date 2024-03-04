import yaml
import os


class ConfigFileApps(object):
    def __init__(self, main_ui):
        """Initializes a new instance of the class.

        Args:
            main_ui: The main user interface instance.

        Attributes:
            ui: The main user interface instance.
            __cached_file: The path to the configuration file.

        Returns:
            None
        """
        self.ui = main_ui
        path_file = os.path.normpath(os.getcwd() + os.sep + os.pardir)
        self.__cached_file = path_file + "/src/models/cached/cache_config.yaml"
        self.__init_config_file()

    def __init_config_file(self):
        """Initializes the configuration data and writes it to the cached file.

        This function creates the initial configuration data using default values or values
        from the UI double spin boxes. The configuration data includes paths to media files,
        parameter names, coordinates, and other settings for Modes 1 and 2, Pano tube, Pano car,
        and image saving. The zoom values for Modes 1 and 2, and the min/max alpha values for
        Pano tube are rounded to three decimal places. The configuration data is then written
        to the cached file using YAML format.

        Returns:
            None
        """
        if not os.path.exists(self.__cached_file):
            config = {
                "Source_type": None,
                "Media_path": None,
                "Parameter_name": None,
                "Recenter_coord": [None, None],
                "Mode_1": {
                    "coord": [None, None],
                    "alpha": self.ui.doubleSpinBox_alpha.value(),
                    "beta": self.ui.doubleSpinBox_beta.value(),
                    "zoom": round(self.ui.doubleSpinBox_zoom.value(), 3)
                },
                "Mode_2": {
                    "coord": [None, None],
                    "pitch": self.ui.doubleSpinBox_alpha.value(),
                    "yaw": self.ui.doubleSpinBox_beta.value(),
                    "roll": self.ui.doubleSpinBox_roll.value(),
                    "zoom": round(self.ui.doubleSpinBox_zoom.value(), 3)
                },
                "Pano_tube": {
                    "alpha_min": round(self.ui.doubleSpinBox_pano_tube_alpha_min.value(), 3),
                    "alpha_max": round(self.ui.doubleSpinBox_pano_tube_alpha_max.value(), 3),
                    "crop_top": round(self.ui.doubleSpinBox_pano_tube_crop_top.value(), 3),
                    "crop_bottom": round(self.ui.doubleSpinBox_pano_tube_crop_buttom.value(), 3)
                },
                "Pano_car": {
                    "coord": [None, None],
                    "alpha": round(self.ui.doubleSpinBox_pano_car_alpha.value(), 3),
                    "beta": round(self.ui.doubleSpinBox_pano_car_beta.value(), 3),
                    "crop_left": round(self.ui.doubleSpinBox_pano_car_crop_left.value(), 3),
                    "crop_right": round(self.ui.doubleSpinBox_pano_car_crop_right.value(), 3),
                    "crop_top": round(self.ui.doubleSpinBox_pano_car_crop_top.value(), 3),
                    "crop_bottom": round(self.ui.doubleSpinBox_pano_car_crop_bottom.value(), 3)
                },
                "Image_saved": {}
            }
            with open(self.__cached_file, "w") as outfile:
                yaml.dump(config, outfile, default_flow_style=False)

