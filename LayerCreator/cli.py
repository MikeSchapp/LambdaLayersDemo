import shutil
from LayerCreator.utils import *

class LayerCreatorCli:
    def __init__(self, s3, layer, zip_name="layer.zip"):
        # TODO implement a CloudFormation template to register the layer and establish permissions for it
        """
        This object is used for the creation and management of lambda layers. It will create or use an existing s3
        bucket, zip the archive and then upload it to S3.
        """
        self.s3 = s3
        self.layer = layer
        self.zip_name = zip_name
        self.file_path = []

    def cli_builder(self):
        """
        Brings together the different cli methods into one simple call
        """
        if not self.s3.check_if_s3_exists():
            if self.__prompt_for_bucket_input():
                self.__create_s3_cli()
        if self.__prompt_for_file_input():
            if self.__prompt_for_user_upload_input():
                self.__prompt_for_register_layer()

    @staticmethod
    def __prompt_for_bucket_input():
        """ Part 1 of the cli builder"""
        user_input = input("Bucket does not exist. Do you want to create this bucket? (Y, N): ")
        if user_input in ["Y", "y", "yes", "Yes"]:
            return True
        if user_input in ["N", "n", "No", "no"]:
            print("Exiting Program, bucket must exist. Specify s3 bucket you own")
            exit()
        else:
            print("Invalid Entry")
            exit()

    def __prompt_for_file_input(self):
        """Part 2 of the cli builder"""
        user_input = input("Is the layer you want to upload zipped? (Y, N): ")
        if user_input in ["Y", "y", "yes", "Yes"]:
            file_path = input("Please enter the filepath now: ")
            self.file_path.append(file_path)
            return True
        if user_input in ["N", "n", "No", "no"]:
            new_user_input = input("Would you like to zip it?(Y, N): ")
            if new_user_input in ["Y", "y", "yes", "Yes"]:
                file_path = input("Please enter the filepath now: ")
                try:
                    self.__prepare_layer_cli(file_path)
                    print("File Successfully Zipped")
                    return True
                except FileNotFoundError:
                    "File not found, please try again."
                    exit()
            if new_user_input in ["N", "n", "No", "no"]:
                print("Exiting Program, file must be zipped to be uploaded")
                exit()
            else:
                print("Invalid Entry")
        return False

    def __prompt_for_user_upload_input(self):
        """Part 3 of the cli builder"""
        user_input = input("Upload layer?(Y, N): ")
        if user_input in ["Y", "y", "yes", "Yes"]:
            self.__upload_layer_cli()
            return True

        if user_input in ["N", "n", "No", "no"]:
            return False

    def __prompt_for_register_layer(self):
        """Part 4 of the cli builder"""
        user_input = input("Do you want to register this layer?(Y, N): ")
        if user_input in ["Y", "y", "yes", "Yes"]:
            self.__define_layer_version()
            return True

        if user_input in ["N", "n", "No", "no"]:
            return False

    def __s3_response_constructor_cli(self):
        """
        Method to construct a response for the s3 create bucket.
        :return: dictionary of **kwargs
        """
        config = read_config("config.yaml")
        config = config["S3"]
        config["Bucket"] = self.s3.bucket_name
        return config

    def __create_s3_cli(self):
        """
        method to bring together the s3 object and config object to construct a response from the yaml file and pass
        to the create s3 bucket method.

        :return: boto3 response
        """
        pre_made_response = self.__s3_response_constructor_cli()
        response = self.s3.create_bucket(pre_made_response)
        return response

    @staticmethod
    def __prepare_layer_cli(file_path):
        """
        Utility to zip files in preparation for upload
        :param file_path: location of file to zip
        """
        shutil.make_archive('layer', 'zip', file_path)

    def __upload_layer_cli(self):
        """
        Passes in zip file name to the s3 function to upload to the specified s3 bucket
        """
        self.s3.upload_layer(self.file_path)

    def __layer_response_creator(self):
        config = read_config("layer_config.yaml")
        config = config["Layer"]
        config["Content"]["S3Bucket"] = self.s3.bucket_name
        config["Content"]["S3Key"] = self.zip_name
        return config

    def __define_layer_version(self):
        pre_made_response = self.__layer_response_creator()
        self.layer.publish_layer_version(pre_made_response)
