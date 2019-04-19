import boto3
import shutil
import sys
from botocore.exceptions import ClientError, ProfileNotFound


class LayerCreator:
    def __init__(self, bucket_name):
        # TODO Separate out the object into an S3 object and one for layer management
        # TODO implement a CloudFormation template to register the layer and establish permissions for it
        """
        This object is used for the creation and management of lambda layers. It will create or use an existing s3
        bucket, zip the archive and then upload it to S3.
        :param bucket_name: Name of an existing bucket, or a bucket you would like to create.
        """
        try:
            session = boto3.Session(profile_name="mfa")
        except ProfileNotFound:
            print("Ensure that the profile named in LayerCreator exists in AWS Credentials")
        self.client = session.client('s3')
        self.bucket_name = bucket_name
        self.zip_name = []

    def cli_builder(self):
        if not self.check_if_s3_exists():
            if self.prompt_for_bucket_input():
                self.create_s3()
        if self.prompt_for_file_input():
            self.prompt_for_user_upload_input()

    @staticmethod
    def prompt_for_bucket_input():
        user_input = input("Bucket does not exist. Do you want to create this bucket? (Y, N): ")
        if user_input in ["Y", "y", "yes", "Yes"]:
            return True
        if user_input in ["N", "n", "No", "no"]:
            print("Exiting Program, bucket must exist. Specify s3 bucket you own")
            exit()
        else:
            print("Please try again with a different bucket name.")
            exit()

    def prompt_for_file_input(self):
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
        return False

    def prompt_for_user_upload_input(self):
        user_input = input("Upload layer?(Y, N): ")
        if user_input in ["Y", "y", "yes", "Yes"]:
            self.upload_layer()
            return True

        if user_input in ["N", "n", "No", "no"]:
            return False

    def create_s3(self):
        response = self.client.create_bucket(
            Bucket=self.bucket_name,
            CreateBucketConfiguration={
                "LocationConstraint": "us-east-2"
            }
        )
        return response

    def check_if_s3_exists(self):
        try:
            response = self.client.list_buckets()
        except (ClientError, ProfileNotFound) as err:
            print(err)
            exit()
        for item in response["Buckets"]:
            if item["Name"] == self.bucket_name:
                print("Bucket found!")
                return True
            else:
                continue
        print("Bucket not found")
        return False

    @staticmethod
    def prepare_layer(file_path):
        shutil.make_archive('layer', 'zip', file_path)

    def upload_layer(self):
        if self.zip_name:
            response = self.client.put_object(
                ACL="private",
                Body=self.zip_name[0],
                Bucket=self.bucket_name,
                Key="layer.zip"
            )
            return response
        else:
            response = self.client.put_object(
                ACL="private",
                Body="layer.zip",
                Bucket=self.bucket_name,
                Key="layer.zip"
            )
            return response


if __name__ == "__main__":
    s3_name = sys.argv[1]
    creator = LayerCreator(s3_name)
    creator.cli_builder()
