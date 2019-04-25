from Objects.creator import *
import sys

from Objects.layer import Layer
from Objects.s3 import S3

if __name__ == "__main__":
    s3_name = sys.argv[1]
    try:
        aws_profile = sys.argv[2]
        layer = Layer(aws_profile)
        s3 = S3(s3_name, aws_profile)
        creator = LayerCreatorInterface(s3, layer)
    except IndexError:
        layer = Layer()
        s3 = S3(s3_name)
        creator = LayerCreatorInterface(s3, layer)
    creator.cli_builder()
