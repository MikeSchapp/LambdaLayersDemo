# Lambda Layers Creator

This function will help package up the specific functions for your layer, 
as well as also create the version and return back a reference to the
layer version for reference in a lambda function.

## Using The Creator
Can be launched via cli, or used within your own code.

To launch via cli call main and enter in the name of the specific bucket
you would like to create or reference.
        
    >python main.py name-of-bucket
        
By default it will use your AWS Credentials, or you can specify a profile to use.

    >python main.py name-of-bucket my-aws-credential-profile
    
This CLI then will guide you through:

1) Creation of a bucket, or using the existing bucket.

2) Zipping the layer files, or selecting a pre-zipped file

3) Uploading the layer to the specified bucket.

## Using for a program

This was designed in order to speed up the process of creating and versioning a lambda layer.

In order to use it

    import LayerCreator
    session = LayerCreator.Session()
    
This will import the module and then allow you to instantiate the boto3 clients necessary to use this program.
(Must have access to both s3 and lambda for this to work)

Steps to use:
1) zip_layer to properly setup the zipfile (If not already zipped). It takes the file path, and the programming language as a parameter.

        session.zip_layer("File Path", "python")

2) set_zip to set the zip path

        session.set_zip("Path to zipfile")

3) set_bucket to set the s3 bucket name that you want to use.

        session.set_bucket("Bucket Name")
        
4) upload_layer to designate a name for the layer and upload it to s3

        session.upload_layer("My Layer")
        
5) publish_layer_version to make the lambda layer available to lambda functions

        session.publish_layer_version(**kwargs(optional))
        
6) This will return the following

        {
            'Content': {
                'Location': 'string',
                'CodeSha256': 'string',
                'CodeSize': 123
            },
            'LayerArn': 'string',
            'LayerVersionArn': 'string',
            'Description': 'string',
            'CreatedDate': 'string',
            'Version': 123,
            'CompatibleRuntimes': [
                'nodejs'|'nodejs4.3'|'nodejs6.10'|'nodejs8.10'|'java8'|'python2.7'|'python3.6'|'python3.7'|'dotnetcore1.0'|'dotnetcore2.0'|'dotnetcore2.1'|'nodejs4.3-edge'|'go1.x'|'ruby2.5'|'provided',
            ],
            'LicenseInfo': 'string'
        }