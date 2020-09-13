import os
import boto3

class EbClient:

    def __init__(self):
        self.eb_client = boto3.client('elasticbeanstalk')

    def new(self, path: str, name: str):
        if not os.path.exists(path):
            raise OSError("The path provided to the init method of EbClient does not exists.")

        response = self.eb_client.create_application(ApplicationName=name)

        print(response)

    def list(self):
        return self.eb_client.describe_applications()

    def get_name(self) -> str:
        return 'name_random'