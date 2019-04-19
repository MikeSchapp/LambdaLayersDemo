import boto3
from botocore.exceptions import ClientError


class CloudFormationApi:
    """
    Object to handle the interaction with AWS, allows for the creation or
    update of an existing stack. Provides static method for checking existence of a stack.
    """

    def __init__(self, template, region="us-east-2", stack_name="CFNAutoLauncher", **kwargs):
        """
        !Optional!
            parameters: a list of dictionaries containing key, value pairs for parameters in cfn template
            tags: a list of dictionaries containing key, value pairs
            termination_protection: boolean for whether to toggle protection on  or off
            capabilities: A list containing capabilities such as CAPABILITY_IAM
            profile: a profile that currently holds mfa credentials
        :param template: string of the url of the CloudFormation Template
        :param stack_name: string of the name of the cloudformation stack you want to create
        :param stack_parameters: dictionary of parameters to be passed in.
        """
        if kwargs.get("profile"):
            session = boto3.Session(profile_name=kwargs.get("profile"))
            self._client = session.client('cloudformation', region_name=region)
        else:
            self._client = boto3.client('cloudformation', region_name=region)
        self._stack_name = stack_name
        self._parameters = kwargs.get("parameters", [{}])
        self._tags = kwargs.get("parameters", [{"Key": "Source", "Value": "Created with cfn_launcher"}])
        self._capabilities = kwargs.get("capabilities", [])
        self._termination_protection = kwargs.get("termination_protection", False)
        template = open(template)
        self._template = template.read()
        if not self.validate_template():
            raise TypeError('Improperly formatted CloudFormation template')

    def validate_template(self):
        """
        Make sure template is valid json or yaml, return false if CloudFormation template fails validation

        :return: Returns a boolean of whether the template passed inspection or not.
        """

        try:
            self._client.validate_template(TemplateBody=self._template)
        except ClientError:
            return False
        print("Template passed validation")
        return True

    def create_stack(self):
        """
        Checks if the stack is created by running check_stack(), then creates the stack if it is not.

        :return returns the response to the create_stack boto call, or prints that stack already exists.
        """
        print("Creating stack")
        if not self.check_stack(self._stack_name):
            response = self._client.create_stack(
                StackName=self._stack_name,
                TemplateBody=self._template,
                Parameters=self._parameters,
                DisableRollback=False,
                TimeoutInMinutes=3,
                Tags=self._tags,
                EnableTerminationProtection=self._termination_protection,
                Capabilities=self._capabilities
            )
            return response
        else:
            print(f'Stack by name of {self._stack_name} already exists')

    def update_stack(self, region_name):
        """
        Runs check_stack() in order to determine whether there is a valid target for the update command

        :return: Returns the response to the command, or prints to console that the stack does not exist.
        """
        print("Updating stack")
        if self.check_stack(self._stack_name):
            response = self._client.update_stack(
                StackName=self._stack_name,
                TemplateBody=self._template,
                UsePreviousTemplate=False,
                Parameters=[
                    {
                        'ParameterKey': "MyBucketName",
                        "ParameterValue": self._bucket_name
                    }
                ],
                Tags=[
                    {
                        'Key': 'CloudFormationType',
                        'Value': 'S3'
                    },
                ],
                Capabilities=[
                    "CAPABILITY_IAM"
                ]
            )
            return response
        else:
            print(f'Stack by name of {self._stack_name} does not exist')

    def delete_stack(self):
        """
        Runs check stack to ensure the stack is available, and then will delete the stack if termination
        protection is off

        :param region_name: Region the stack is located in e.g. us-east-1
        :return: Response to the delete command, if it can successfully identify the stack
        """
        print("Deleting stack")
        if self.check_stack(self._stack_name):
            response = self._client.delete_stack(
                StackName=self._stack_name,
            )
            return response
        else:
            print(f'Stack by name of {self._stack_name} does not exist')

    def check_stack(self, stack_name):
        """
        Checks if the given stack exists. Returns boolean.

        :param stack_name: Name of the stack that will be searched for
        :return: Responds with True if it exists, and False if it does not
        """
        print("Checking status of the stack")
        try:
            response = self._client.describe_stacks(
                StackName=stack_name
            )
        except ClientError:
            return False
        return True

    def cfn_waiter(self, waiter_type, **kwargs):
        """
        !Optional!:
            waiter_config is a dict containing the keys Delay and MaxAttempts. You can specify ints for how often they poll
            and how many attempts are made.
        :param waiter_type: specifies the waiter type as either create, delete, update, change, exists
        :return:
        """
        print(f"Creating {waiter_type} waiter")
        waiter_config = kwargs.get("waiter_config", {"Delay": 10,
                                                     "MaxAttempts": 120})
        if waiter_type == "update":
            waiter = self._client.get_waiter("stack_update_complete")
            message = f"Stack called {self._stack_name} successfully updated"
        elif waiter_type == "create":
            waiter = self._client.get_waiter("stack_create_complete")
            message = f"Stack named {self._stack_name} was successfully created"
        elif waiter_type == "delete":
            waiter = self._client.get_waiter("stack_delete_complete")
            message = f"Stack named {self._stack_name} was successfully deleted"
        elif waiter_type == "exists":
            waiter = self._client.get_waiter("stack_exists")
            message = f"Stack named {self._stack_name} currently exists"
        else:
            print("Please select the appropriate type")

        waiter.wait(
            StackName=self._stack_name,
            WaiterConfig=waiter_config
        )
        print(message)
