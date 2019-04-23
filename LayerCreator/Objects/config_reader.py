import yaml


class ConfigReader:

    @staticmethod
    def read_config():
        with open("config.yaml") as config:
            my_config = yaml.load(config, Loader=yaml.FullLoader)
        return my_config
