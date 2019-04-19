from LayerCreator.Objects.creator import *
import sys
if __name__ == "__main__":
    s3_name = sys.argv[1]
    try:
        aws_profile = sys.argv[2]
        creator = LayerCreator(s3_name, aws_profile)
    except IndexError:
        creator = LayerCreator(s3_name)
    creator.cli_builder()
