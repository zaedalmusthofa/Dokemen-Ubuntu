"""
This is a plugin interface that a bridge between main application and plugin widgets
you can create everything user interface you want in your plugin apps
you also can use a model from main application, so you don't have to create from scratch.
reference: https://stackoverflow.com/questions/66309119/pyqt5-button-signal-doesnt-work-in-a-layout-inside-a-widget

"""


class PluginInterface(object):
    def __init__(self):
        """
        This is the base class that each plugin's must inheritance from.
        Within this class you have to define the methods that must implement into your plugin
        """
        self.description = "Plugin description here!"

    def set_plugin_widget(self, model):
        """
        Create a widget object and return to send into main apps
        Args:
            model: the model of main apps that you can use

        Returns:
            widget object
        """
        raise NotImplementedError

    def set_icon_apps(self):
        """
        Send the image that will use to crete an icon ot the button apps
        Returns:
            icon (image) file
        """
        raise NotImplementedError

    def change_stylesheet(self):
        """
        Change the stylesheet of your widget following the main application theme.
        Returns:
            None, you can write "pass" if you don't want to change
        """
        raise NotImplementedError

    def always_pop_up(self):
        """
        Change the stylesheet of your widget following the main application theme.
        Returns:
            None, you can write "pass" if you don't want to change
        """
        return False



