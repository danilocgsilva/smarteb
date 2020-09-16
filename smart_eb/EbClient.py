from smart_eb.EBFormater import EBFormater
from random import random
import boto3
import math
import os

class EbClient:

    def __init__(self):
        self.eb_client = boto3.client('elasticbeanstalk')

    def new(self, path: str, name: str) -> EBFormater:
        if not os.path.exists(path):
            raise OSError("The path provided to the init method of EbClient does not exists.")

        response = self.eb_client.create_application(ApplicationName=name)
        
        return EBFormater(response["Application"])
        

    def list(self) -> str:
        response_data = self.eb_client.describe_applications()

        eb_data_list = []
        for ebdata in response_data["Applications"]:
            eb_data_list.append(EBFormater(ebdata))

        return eb_data_list

    def delete(self, app_name: str):

        response_data = self.eb_client.describe_applications(
            ApplicationNames=[app_name]
        )
        if len(response_data["Applications"]) == 0:
            print("The application " + app_name + " does not exists. Nothing to delete.")
        else:
            self.eb_client.delete_application(
                ApplicationName=app_name
            )
            print("The application " + app_name + " has been deleted.")
        

    def get_name(self) -> str:
        return 'app-' + str(math.ceil(random() * 10000))