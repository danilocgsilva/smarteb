import os
import boto3

class EbClient:

    def init(self, path: str):

        if not os.path.exists(path):
            raise Exception("The path provided to the init method of EbClient does not exists.")

        eb_client = boto3.client('elasticbeanstalk')

        response = eb_client.create_application(ApplicationName="testing3")

        print(response)
