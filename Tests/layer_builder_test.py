from datetime import datetime
import boto3
import LayerCreator
from botocore.stub import Stubber


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
    test = LayerCreator.Session()
    test.set_bucket('mike-stub-test')
    test._s3_client = s3
    new_response = test.check_if_s3_exists()
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
    test = LayerCreator.Session()
    test.set_bucket('mike-stub-test')
    test._s3_client = s3
    new_response = test.check_if_s3_exists()
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
    with open("test.zip", "rb") as data:
        expected_params = {
            "ACL": "private",
            "Body": data,
            "Bucket": "mike-stub-test",
            "Key": "layer.zip"}
    stubber.add_response('put_object', response, expected_params)
    stubber.activate()
    test = LayerCreator.Session()
    test.set_bucket('mike-stub-test')
    test._s3_client = s3
    test.set_zip("test.zip")
    new_response = test.upload_layer("My_Awesome_Layer")
    new_response["Bucket"] = "dummy_data"
    assert new_response == response


def test_stub_put_object_self_named():
    session = boto3.Session(profile_name="mfa")
    s3 = session.client('s3')
    layer = Layer()
    s3_client = S3('mike-stub-test')
    test = LayerCreatorCli(s3_client, layer)
    test.zip_name = ["test.zip"]
    test.s3.client = s3
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
        "Body": "dummy_data",
        "Bucket": "mike-stub-test",
        "Key": "layer.zip"}

    stubber.add_response('put_object', response, expected_params)
    stubber.activate()
    layer = Layer()
    s3_client = S3('mike-stub-test')
    test = LayerCreatorCli(s3_client, layer)
    test.zip_name = ["test.zip"]
    test.s3.client = s3
    new_response = test.s3.upload_layer(test.zip_name)
    new_response["Body"] = "dummy_data"
    print(new_response)
    assert new_response == response
