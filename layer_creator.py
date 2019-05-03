from LayerCreator.cli import *
import sys
from LayerCreator.layer import Layer
from LayerCreator.s3 import S3
from LayerCreator.cli import LayerCreatorCli

if __name__ == "__main__":
    s3_name = sys.argv[1]
    try:
        aws_profile = sys.argv[2]
        layer = Layer(aws_profile)
        s3 = S3(s3_name, aws_profile)
        creator = LayerCreatorCli(s3, layer)
    except IndexError:
        layer = Layer()
        s3 = S3(s3_name)
        creator = LayerCreatorCli(s3, layer)
    creator.cli_builder()
