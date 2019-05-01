import boto3
from botocore.exceptions import ProfileNotFound, ClientError


class Session:
    def __init__(self, profile="default"):
        """
        Creates all the necessary clients to interact with AWS
        :param profile: alternate aws profile to be used with the credential file.
        """
        self.profile = profile
        try:
            session = boto3.Session(profile_name=self.profile)
            self.__s3_client = session.client('s3')
            self.__lambda_client = session.client('lambda')
        except ProfileNotFound:
            self.__s3_client = boto3.client('s3')
            self.__lambda_client = boto3.client('lambda')
        self.__zip_path = None
        self.__bucket = None
        self.__layer_name = None

    def check_if_s3_exists(self):
        """
        Check if the s3 bucket exists in the returned list of buckets for your aws account
        :return: Returns true if found, or false if not found
        """
        try:
            response = self.__s3_client.list_buckets()
        except (ClientError, ProfileNotFound) as err:
            print(err)
            exit()
        for item in response["Buckets"]:
            if item["Name"] == self.__bucket:
                print("Bucket found!")
                return True
        print("Bucket not found")
        return False

    def upload_layer(self, layer_name):
        """
        Used to actually upload the pre zipped code
        :param layer_name: What you want to name the layer in the s3 bucket.
        :return: boto 3 response
        """
        self.__layer_name = layer_name
        if self.__bucket:
            if self.__zip_path:
                with open(self.__zip_path, "rb") as data:
                    response = self.__s3_client.put_object(
                        ACL="private",
                        Body=data,
                        Bucket=self.__bucket,
                        Key=layer_name + ".zip"
                    )
                    return response
            else:
                with open("layer.zip", "rb") as data:
                    response = self.__s3_client.put_object(
                        ACL="private",
                        Body=data,
                        Bucket=self.__bucket,
                        Key=layer_name + ".zip"
                    )
                    return response
        else:
            raise KeyError("Specified bucket does not exist")

    def set_zip(self, zip_path):
        self.__zip_path = zip_path

    def set_bucket(self, bucket_name):
        self.__bucket = bucket_name

    def publish_layer_version(self, **kwargs):
        """

        :param kwargs:
        :return:
        """
        pre_made_response = {}
        layer_name = kwargs.get("LayerName", "LayerBuilder")
        description = kwargs.get("Description", "Layer created with layer builder")
        key = kwargs.get("S3Key", self.__layer_name)
        bucket = kwargs.get("S3Bucket", self.__bucket)
        version = kwargs.get("S3ObjectVersion", None)
        runtime = kwargs.get("CompatibleRuntimes", ["python3.7"])
        license_info = kwargs.get("LicenseInfo", "N/A")
        pre_made_response["LayerName"] = layer_name
        pre_made_response["Description"] = description
        pre_made_response["Content"]["S3Key"] = key
        pre_made_response["Content"]["S3Bucket"] = bucket
        if version:
            pre_made_response["Content"]["S3ObjectVersion"] = version
        pre_made_response["CompatibleRuntime"] = runtime
        pre_made_response["LicenseInfo"] = license_info
        response = self.__lambda_client.publish_layer_version(**pre_made_response)
        return response
