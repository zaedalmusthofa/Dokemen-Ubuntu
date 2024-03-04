import inspect
import os
import pkgutil
import sys
sys.path.append("..")
from src.plugin_interface import PluginInterface


class PluginCollection(object):
    def __init__(self, plugin_package):
        """Initialize the plugin loader with the given plugin package.

        Args:
            plugin_package (str): The name of the plugin package.

        Attributes:
            plugins (dict): A dictionary of loaded plugins.
            name_application (str): The name of the application.
            seen_paths (set): A set of paths already seen by the loader.
            path_folder (str): The path to the plugin folder.
            plugin_package (str): The name of the plugin package.

        Returns:
            None
        """
        self.plugins = None
        self.name_application = None
        self.seen_paths = None
        self.path_folder = None
        self.plugin_package = plugin_package
        self.reload_plugins()

    def reload_plugins(self):
        """Reloads the plugins from the specified package.

        This function clears the existing plugin list, name list, and folder path list, then
        walks through the plugin package and appends any valid plugins to the plugin list.

        Args:
            None.

        Returns:
            None.
        """
        self.plugins = []
        self.name_application = []
        self.seen_paths = []
        self.path_folder = []
        self.walk_package(self.plugin_package)

    def get_widget(self, index, model):
        """Returns the widget associated with a plugin at the specified index.

        Args:
            index: The index of the plugin to get the widget for.
            model: The model to use when initializing the plugin's widget.

        Returns:
            The widget associated with the plugin at the specified index, or None if there was an error.
        """
        plugin = self.plugins[index]
        return plugin.set_plugin_widget(model)

    def set_always_pop_up(self, index):
        return self.plugins[index].always_pop_up()

    def get_icon_(self, index):
        """Returns the path of the icon for a given plugin index.

        Args:
            index (int): The index of the plugin.

        Returns:
            str or None: The path to the icon file, or None if the plugin has no icon.
        """
        # path_file = os.path.dirname(os.path.realpath(__file__))
        path_file = os.path.abspath(".")
        icon_source = self.plugins[index].set_icon_apps()
        if icon_source is not None:
            if icon_source[0] == ".":
                icon_source.replace("./", "")
            elif icon_source[0] == "/":
                icon_source.replace("/", "")

            folder = self.path_folder[index]
            path = folder.split(".")[1]
            path = path_file + '/plugins/' + path + "/" + icon_source
        else:
            path = None
        return path

    def change_theme(self, index):
        """Change the stylesheet of the plugin at the given index to the current theme.

        Args:
            index (int): The index of the plugin to update.

        Returns:
            None
        """
        if len(self.plugins) > 0:
            self.plugins[index].change_stylesheet()

    def get_description(self, index):
        """Returns the description of the plugin located at the specified index.

        Args:
            index (int): The index of the plugin whose description is to be retrieved.

        Returns:
            str: The description of the plugin.

        Raises:
            IndexError: If the specified index is out of range.

        """
        return self.plugins[index].description

    def walk_package(self, package):
        """Walk through the specified package and its sub-packages to find all classes
            that are a subclass of PluginInterface and add them to the list of plugins.

        Args:
            package (str): The name of the package to search for plugins in.

        Returns:
            None.

        Raises:
            None.
        """
        path_file = os.path.dirname(os.path.realpath(__file__))
        sys.path.insert(0, path_file)
        imported_package = __import__(package, fromlist=['blah'])

        for _, plugin_name, is_pkg in pkgutil.iter_modules(
                imported_package.__path__, imported_package.__name__ + '.'):
            if not is_pkg:
                try:
                    plugin_module = __import__(plugin_name, fromlist=['blah'])
                    cls_members = inspect.getmembers(plugin_module, inspect.isclass)
                    for (_, c) in cls_members:
                        # only add classes that are a subclass of plugins, but not
                        # plugins itself
                        if issubclass(c, PluginInterface) & (c is not PluginInterface):
                            # print(f'Found Plugin class: {c.__name__}')
                            self.path_folder.append(c.__module__)
                            self.name_application.append(c.__name__)
                            self.plugins.append(c())
                except ImportError as err:
                    print("Your will get problem because: " + str(err))

        # Now that we have looked at all the modules in the current package, start looking
        # recursively for additional modules in sub packages
        all_current_paths = []
        if isinstance(imported_package.__path__, str):
            all_current_paths.append(imported_package.__path__)
        else:
            all_current_paths.extend([x for x in imported_package.__path__])

        for pkg_path in all_current_paths:
            if pkg_path not in self.seen_paths:
                self.seen_paths.append(pkg_path)

                # get subdirectory of current package path directory
                child_pkgs = [
                    p for p in os.listdir(pkg_path) if os.path.isdir(
                        os.path.join(
                            pkg_path, p)) and p[0] != '.']
                # For each subdirectory, apply the walk_package method
                # recursively
                for child_pkg in child_pkgs:
                    self.walk_package(package + '.' + child_pkg)
