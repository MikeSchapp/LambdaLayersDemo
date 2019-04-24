from LayerCreator.Objects.creator import *
import sys
if __name__ == "__main__":
    s3_name = sys.argv[1]
    try:
        aws_profile = sys.argv[2]
        s3 = S3Api(s3_name, aws_profile)
        creator = LayerCreatorInterface(s3)
    except IndexError:
        s3 = S3Api(s3_name)
        creator = LayerCreatorInterface(s3)
    creator.cli_builder()
