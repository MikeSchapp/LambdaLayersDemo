import yaml


def read_config(config_file):
    """
    Reads yaml file for specific configuration and loads it into a python usable form.
    :return:
    """
    with open(config_file) as config:
        my_config = yaml.load(config)
    return my_config
