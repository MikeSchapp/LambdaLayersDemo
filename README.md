# Lambda Layers Creator

This was designed in order to speed up the process of creating and versioning a lambda layer.

In order to use it

    import LayerCreator
    session = LayerCreator.Session()
    
This will import the module and then allow you to instantiate the boto3 clients necessary to use this program.
(Must have access to both s3 and lambda for this to work)

Steps to use:
1) zip_layer to properly setup the zipfile (If not already zipped). It takes the file path, and runtime identifier as a parameter. 
    See https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtimes.html for valid identifiers.

        session.zip_layer("File Path", "python3.7")

2) set_zip to set the zip path

        session.set_zip("Path to zipfile")

3) set_bucket to set the s3 bucket name that you want to use.

        session.set_bucket("Bucket Name")

4) set_runtime to set the lambda layer runtime
    
    See https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtimes.html
    
        session.set_runtime("python3.7")

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