# Lambda Layers Creator

This function will help package up the specific functions for your layer, 
as well as also create the version and return back a reference to the
layer version for reference in a lambda function.

## Using The Creator
Can be launched via cli, or used within your own code.

To launch via cli call, creator and enter in the name of the specific bucket
you would like to create or reference.
        
    >python creator.py name-of-bucket
        
By default it will use your AWS Credentials, or you can specify a profile to use.

    >python creator.py name-of-bucket my-aws-credential-profile
    
This CLI then will guide you through:

1) Creation of a bucket, or using the existing bucket.

2) Zipping the layer files, or selecting a pre-zipped file

3) Uploading the layer to the specified bucket.
