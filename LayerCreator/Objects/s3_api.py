import boto3
from botocore.exceptions import ProfileNotFound, ClientError


class S3Api:
    def __init__(self, bucket_name, profile="default"):
        self.bucket_name = bucket_name
        self.profile = profile
        try:
            session = boto3.Session(profile_name=self.profile)
            self.client = session.client('s3')
        except ProfileNotFound:
            self.client = boto3.client('s3')

    def create_bucket(self, pre_made_response):
        response = self.client.create_bucket(**pre_made_response)
        return response

    def check_if_s3_exists(self, bucket_name):
        try:
            response = self.client.list_buckets()
        except (ClientError, ProfileNotFound) as err:
            print(err)
            exit()
        for item in response["Buckets"]:
            if item["Name"] == bucket_name:
                print("Bucket found!")
                return True
        print("Bucket not found")
        return False

    def upload_layer(self, zip_name):
        if zip_name:
            response = self.client.put_object(
                ACL="private",
                Body=zip_name[0],
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
