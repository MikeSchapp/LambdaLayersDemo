from datetime import datetime
import boto3
from Objects.creator import *
from botocore.stub import Stubber


def test_stub_create_s3():
    session = boto3.Session(profile_name="mfa")
    s3 = session.client('s3')
    stubber = Stubber(s3)
    response = {
        "Location": "Test"
    }
    expected_params = {'Bucket': 'mike-stub-test',
                       'CreateBucketConfiguration': {'LocationConstraint': 'us-east-2'},
                       'ObjectLockEnabledForBucket': False}
    stubber.add_response('create_bucket', response, expected_params)
    stubber.activate()
    test = LayerCreatorInterface("mike-stub-test")
    test.s3_api.client = s3
    new_response = test.create_s3()
    assert response == new_response


def test_stub_list_buckets_bucket_exists():
    session = boto3.Session(profile_name="mfa")
    s3 = session.client('s3')
    stubber = Stubber(s3)
    response = {
        'Buckets': [
            {
                'Name': 'test',
                'CreationDate': datetime(2015, 1, 1)
            },
            {
                'Name': 'mike-stub-test',
                'CreationDate': datetime(2015, 1, 1)
            },
        ],
        'Owner': {
            'DisplayName': 'test',
            'ID': 'test'
        }
    }
    expected_params = None
    stubber.add_response('list_buckets', response, expected_params)
    stubber.activate()
    test = LayerCreatorInterface("mike-stub-test")
    test.s3_api.client = s3
    new_response = test.s3_api.check_if_s3_exists(test.bucket_name)
    assert new_response is True


def test_stub_list_buckets_bucket_not_exist():
    session = boto3.Session(profile_name="mfa")
    s3 = session.client('s3')
    stubber = Stubber(s3)
    response = {
        'Buckets': [
            {
                'Name': 'test',
                'CreationDate': datetime(2015, 1, 1)
            },            {
                'Name': 'test2',
                'CreationDate': datetime(2015, 1, 1)
            }
        ],
        'Owner': {
            'DisplayName': 'test',
            'ID': 'test'
        }
    }
    expected_params = None
    stubber.add_response('list_buckets', response, expected_params)
    stubber.activate()
    test = LayerCreatorInterface("mike-stub-test")
    test.s3_api.client = s3
    new_response = test.s3_api.check_if_s3_exists(test.bucket_name)
    assert new_response is False


def test_stub_put_object_prenamed():
    session = boto3.Session(profile_name="mfa")
    s3 = session.client('s3')
    stubber = Stubber(s3)
    response = {
        'Expiration': 'test',
        'ETag': 'test',
        'ServerSideEncryption': 'AES256',
        'VersionId': 'test',
        'SSECustomerAlgorithm': 'test',
        'SSECustomerKeyMD5': 'test',
        'SSEKMSKeyId': 'test',
        'RequestCharged': 'test'
    }
    expected_params = {
        "ACL": "private",
        "Body": "layer.zip",
        "Bucket": "mike-stub-test",
        "Key": "layer.zip"}

    stubber.add_response('put_object', response, expected_params)
    stubber.activate()
    test = LayerCreatorInterface("mike-stub-test")
    test.s3_api.client = s3
    new_response = test.s3_api.upload_layer(test.zip_name, test.bucket_name)
    assert new_response == response


def test_stub_put_object_self_named():
    session = boto3.Session(profile_name="mfa")
    s3 = session.client('s3')
    stubber = Stubber(s3)
    response = {
        'Expiration': 'test',
        'ETag': 'test',
        'ServerSideEncryption': 'AES256',
        'VersionId': 'test',
        'SSECustomerAlgorithm': 'test',
        'SSECustomerKeyMD5': 'test',
        'SSEKMSKeyId': 'test',
        'RequestCharged': 'test'
    }
    expected_params = {
        "ACL": "private",
        "Body": "test.zip",
        "Bucket": "mike-stub-test",
        "Key": "layer.zip"}

    stubber.add_response('put_object', response, expected_params)
    stubber.activate()
    test = LayerCreatorInterface("mike-stub-test")
    test.zip_name = ["test.zip"]
    test.s3_api.client = s3
    new_response = test.s3_api.upload_layer(test.zip_name, test.bucket_name)
    assert new_response == response
