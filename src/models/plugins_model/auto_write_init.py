import os
import importlib


def update_init_file_for_import(input_path=None):
    if input_path is None:
        directory = "/".join(os.path.dirname(os.path.realpath(__file__)).split("/")[-2:])
        init_file = os.path.join(directory, '__init__.py')
        files = os.listdir(directory)
    else:
        directory = input_path
        init_file = os.path.join(directory, '__init__.py')
        files = os.listdir(directory)

    writer_import = []
    with open(init_file, 'w') as f:
        for file in files:
            if file.endswith('.py') and file != '__init__.py':
                module_name = file[:-3]
                if input_path is None:
                    module_path = os.path.join(directory, module_name).replace('/', '.')
                else:
                    module_path = os.path.join(directory, module_name).replace('./', '')
                if file != "auto_write_init.py":
                    module = importlib.import_module(module_path)
                    for name in dir(module):
                        obj = getattr(module, name)
                        if hasattr(obj, '__class__') and issubclass(obj.__class__, type):
                            string_import = f"from .{module_name} import {obj.__name__}"
                            if string_import not in writer_import:
                                f.write(f"from .{module_name} import {obj.__name__}\n")
                                writer_import.append(string_import)

            elif os.path.isdir(os.path.join(directory, file)):
                subdir = os.path.join(directory, file)
                if file != "__pycache__":
                    for subdir_file in os.listdir(subdir):
                        if subdir_file.endswith('.py') and subdir_file != "__init__.py":
                            module_name = subdir_file[:-3]
                            if input_path is None:
                                module_path = os.path.join(subdir, module_name).replace('/', '.')
                            else:
                                module_path = os.path.join(subdir, module_name).replace('/', '.')[2:]

                            module = importlib.import_module(module_path)
                            for name in dir(module):
                                obj = getattr(module, name)
                                if hasattr(obj, '__class__') and issubclass(obj.__class__, type):
                                    string_import = f"from .{file}.{module_name} import {obj.__name__}"
                                    if string_import not in writer_import:
                                        f.write(f"from .{file}.{module_name} import {obj.__name__}\n")
                                        writer_import.append(string_import)


# testing code
if __name__ == "__main__":
    update_init_file_for_import(".")

