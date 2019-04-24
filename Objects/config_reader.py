import yaml


class ConfigReader:

    @staticmethod
    def read_config():
        """
        Reads yaml file for specific configuration and loads it into a python usable form.
        :return:
        """
        with open("config.yaml") as config:
            my_config = yaml.load(config, Loader=yaml.FullLoader)
        return my_config
