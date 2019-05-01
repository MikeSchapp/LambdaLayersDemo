import boto3
from botocore.exceptions import ProfileNotFound, ClientError


class S3:
    def __init__(self, bucket_name, profile="default"):
        # TODO Default the config to S3 best practice for security
        """
        Used to intertact with boto and AWS. Allows customization of bucket privileges upon creation.
        :param bucket_name: name of the existing bucket, or bucket you would like to create
        :param profile: AWS credential profile, if other than the default profile.
        """
        self.bucket_name = bucket_name
        self.profile = profile
        try:
            session = boto3.Session(profile_name=self.profile)
            self.client = session.client('s3')
        except ProfileNotFound:
            self.client = boto3.client('s3')

    def create_bucket(self, pre_made_response):
        """

        :param pre_made_response: a dictionary object passed into the response in order to supply necessary config to
        bucket creation. See config_reader object for more information.
        :return: boto3 response
        """
        response = self.client.create_bucket(**pre_made_response)
        return response

    def check_if_s3_exists(self):
        """
        Check if the s3 bucket exists in the returned list of buckets for your aws account
        :return: Returns true if found, or false if not found
        """
        try:
            response = self.client.list_buckets()
        except (ClientError, ProfileNotFound) as err:
            print(err)
            exit()
        for item in response["Buckets"]:
            if item["Name"] == self.bucket_name:
                print("Bucket found!")
                return True
        print("Bucket not found")
        return False

    def upload_layer(self, file_path):
        """
        Used to actually upload the pre zipped code
        :param zip_name: the name of the pre-zipped file/folder to upload to the s3 bucket
        :return: boto 3 response
        """
        if file_path:
            with open(file_path[0], "rb") as data:
                response = self.client.put_object(
                    ACL="private",
                    Body=data,
                    Bucket=self.bucket_name,
                    Key="layer.zip"
                )
                return response
        else:
            with open("layer.zip", "rb") as data:
                response = self.client.put_object(
                    ACL="private",
                    Body=data,
                    Bucket=self.bucket_name,
                    Key="layer.zip"
                )
                return response
