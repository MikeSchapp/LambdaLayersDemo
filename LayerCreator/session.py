import boto3
from botocore.exceptions import ProfileNotFound, ClientError
from LayerCreator import utils


class Session:
    def __init__(self, profile="default"):
        """
        Creates all the necessary clients to interact with AWS
        :param profile: alternate aws profile to be used with the credential file.
        """
        self.profile = profile
        try:
            session = boto3.Session(profile_name=self.profile)
            self._s3_client = session.client('s3')
            self._lambda_client = session.client('lambda')
        except ProfileNotFound:
            self._s3_client = boto3.client('s3')
            self._lambda_client = boto3.client('lambda')
        self._zip_path = None
        self._bucket = None
        self._layer_name = None
        self._runtime = []

    def check_if_s3_exists(self):
        """
        Check if the s3 bucket exists in the returned list of buckets for your aws account
        :return: Returns true if found, or false if not found
        """
        try:
            response = self._s3_client.list_buckets()
        except (ClientError, ProfileNotFound) as err:
            print(err)
            exit()
        for item in response["Buckets"]:
            if item["Name"] == self._bucket:
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
        self._layer_name = layer_name
        if self._bucket:
            if self._zip_path:
                with open(self._zip_path, "rb") as data:
                    response = self._s3_client.put_object(
                        ACL="private",
                        Body=data,
                        Bucket=self._bucket,
                        Key=layer_name + ".zip"
                    )
                    return response
            else:
                with open("layer.zip", "rb") as data:
                    response = self._s3_client.put_object(
                        ACL="private",
                        Body=data,
                        Bucket=self._bucket,
                        Key=layer_name + ".zip"
                    )
                    return response
        else:
            raise KeyError("Specified bucket does not exist")

    def zip_layer(self, file_location, language):
        self._zip_path = utils.zip_layer(file_location, language)

    def set_zip(self, zip_path):
        self._zip_path = zip_path

    def set_bucket(self, bucket_name):
        self._bucket = bucket_name

    def append_runtime(self, runtime):
        self._runtime.append(runtime)

    def publish_layer_version(self, **kwargs):
        """

        :param kwargs:
        :return:
        """
        pre_made_response = {}
        layer_name = kwargs.get("LayerName", "LayerBuilder")
        description = kwargs.get("Description", "Layer created with layer builder")
        key = kwargs.get("S3Key", self._layer_name)
        bucket = kwargs.get("S3Bucket", self._bucket)
        version = kwargs.get("S3ObjectVersion", None)
        runtime = kwargs.get("CompatibleRuntimes", self._runtime)
        license_info = kwargs.get("LicenseInfo", "N/A")
        pre_made_response["LayerName"] = layer_name
        pre_made_response["Description"] = description
        pre_made_response["Content"]["S3Key"] = key
        pre_made_response["Content"]["S3Bucket"] = bucket
        if version:
            pre_made_response["Content"]["S3ObjectVersion"] = version
        pre_made_response["CompatibleRuntime"] = runtime
        pre_made_response["LicenseInfo"] = license_info
        response = self._lambda_client.publish_layer_version(**pre_made_response)
        return response
