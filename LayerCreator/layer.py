import boto3
from botocore.exceptions import ProfileNotFound


class Layer:
    def __init__(self, profile="default"):
        self.profile = profile
        try:
            session = boto3.Session(profile_name=self.profile)
            self.client = session.client('lambda')
        except ProfileNotFound:
            self.client = boto3.client('lambda')

    def publish_layer_version(self, pre_made_response):
        response = self.client.publish_layer_version(**pre_made_response)
        return response
