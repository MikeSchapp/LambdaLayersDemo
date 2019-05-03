import os
import yaml
import shutil
import ntpath


def read_config(config_file):
    """
    Reads yaml file for specific configuration and loads it into a python usable form.
    :return:
    """
    with open(config_file) as config:
        my_config = yaml.load(config)
    return my_config


def zip_layer(file_path, language):
    if language == "python":
        language_path = "python/"
    elif language == "ruby":
        language_path = "ruby/gems/"
    elif language == "java":
        language_path = "java/lib/"
    elif language == "node":
        language_path = "nodejs/node_modules/"
    else:
        language_path = "bin/"
    """
    Utility to zip files in preparation for upload
    :param file_path: location of file to zip
    """
    file = ntpath.basename(file_path)
    os.makedirs("Layers/layers_prep/" + language_path)
    shutil.copyfile(file_path, "Layers/layers_prep/" + language_path + file)
    shutil.make_archive('Layers/layer', 'zip', "Layers/layers_prep")
    os.remove("Layers/layers_prep/" + language_path + file)
    os.removedirs("Layers/layers_prep/" + language_path)
    return "Layers/layer.zip"
