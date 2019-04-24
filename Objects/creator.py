import shutil
from Objects.config_reader import ConfigReader


class LayerCreatorInterface:
    def __init__(self, s3_api):
        # TODO implement a CloudFormation template to register the layer and establish permissions for it
        """
        This object is used for the creation and management of lambda layers. It will create or use an existing s3
        bucket, zip the archive and then upload it to S3.
        :param profile: Alternate AWS credential profile to be used instead.
        """
        self.s3_api = s3_api
        self.zip_name = []

    def cli_builder(self):
        """
        Brings together the different cli methods into one simple call
        """
        if not self.s3_api.check_if_s3_exists():
            if self.prompt_for_bucket_input():
                self.create_s3()
        if self.prompt_for_file_input():
            self.prompt_for_user_upload_input()

    @staticmethod
    def prompt_for_bucket_input():
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

    def prompt_for_file_input(self):
        """Part 2 of the cli builder"""
        user_input = input("Is the layer you want to upload zipped? (Y, N): ")
        if user_input in ["Y", "y", "yes", "Yes"]:
            file_path = input("Please enter the filepath now: ")
            self.zip_name.append(file_path)
            return True
        if user_input in ["N", "n", "No", "no"]:
            new_user_input = input("Would you like to zip it?(Y, N): ")
            if new_user_input in ["Y", "y", "yes", "Yes"]:
                file_path = input("Please enter the filepath now: ")
                try:
                    self.prepare_layer(file_path)
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

    def prompt_for_user_upload_input(self):
        """Part 3 of the cli builder"""
        user_input = input("Upload layer?(Y, N): ")
        if user_input in ["Y", "y", "yes", "Yes"]:
            self.upload_layer()
            return True

        if user_input in ["N", "n", "No", "no"]:
            return False

    def s3_response_constructor(self):
        """
        Method to construct a response for the s3 create bucket.
        :return: dictionary of **kwargs
        """
        config = ConfigReader.read_config()
        config["Bucket"] = self.s3_api.bucket_name
        return config

    def create_s3(self):
        """
        method to bring together the s3 object and config object to construct a response from the yaml file and pass
        to the create s3 bucket method.

        :return: boto 3 response
        """
        pre_made_response = self.s3_response_constructor()
        response = self.s3_api.create_bucket(pre_made_response)
        return response

    @staticmethod
    def prepare_layer(file_path):
        """
        Utility to zip files in preparation for upload
        :param file_path: location of file to zip
        """
        shutil.make_archive('layer', 'zip', file_path)

    def upload_layer(self):
        """
        Passes in zip file name to the s3 function to upload to the specified s3 bucket
        """
        self.s3_api.upload_layer(self.zip_name)

    def define_layer_version(self):
        # TODO
        pass

