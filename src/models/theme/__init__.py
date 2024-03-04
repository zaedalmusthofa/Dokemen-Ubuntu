import os
path_file = os.path.dirname(os.path.realpath(__file__))
with open(path_file + "/light_mode.css", "r") as file:
    STYLE_LIGHT_MODE = file.read()

with open(path_file + "/dark_mode.css", "r") as file:
    STYLE_DARK_MODE = file.read()
