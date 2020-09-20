from smart_eb.EBFormater import EBFormater
from smart_eb.EbLocalConfigurator import EbLocalConfigurator
from random import random
import boto3
import math
import os

class EbClient:

    def __init__(self):
        self.eb_client = boto3.client('elasticbeanstalk')

    def new(self, path: str, name: str) -> EBFormater:
        
        ebLocalConfigurator = self.create_eb_config(name, path)
        application_name = ebLocalConfigurator.getApplicationName()

        fileres = open(os.path.join(path, "index.php"), "a")
        fileres.write("<?php\nprint(\"Hello World from " + application_name + "!!!\");\n\n")
        fileres.close()

        response = self.eb_client.create_application(ApplicationName=name)

        self.eb_client.create_configuration_template(
            ApplicationName=application_name,
            TemplateName='template-name-for-' + application_name,
            SolutionStackName="64bit Amazon Linux 2 v3.1.1 running PHP 7.4",
            OptionSettings=[
                {
                    # 'ResourceName': 'string',
                    'Namespace': 'aws:autoscaling:launchconfiguration',
                    'OptionName': 'aws-elasticbeanstalk-ec2-role',
                    # 'Value': 'string'
                },
            ],
        )

        self.eb_client.create_environment(
            ApplicationName=name,
            EnvironmentName=ebLocalConfigurator.getEnvironment(),
            SolutionStackName="64bit Amazon Linux 2 v3.1.1 running PHP 7.4"
        )
        
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
        
    def create_eb_config(
        self, 
        app_name: str,
        path: str
    ):
        if not os.path.exists(path):
            raise OSError("The path provided to the init method of EbClient does not exists.")

        ebLocalConfigurator = EbLocalConfigurator()
        ebLocalConfigurator\
            .setApplicationName(app_name)\
            .setDefaultPlatform("PHP 7.4 running on 64bit Amazon Linux 2")\
            .guess_environment_name()

        folder_to_be_created = os.path.join(path, '.elasticbeanstalk')
        os.makedirs(folder_to_be_created)
        file_to_be_created = os.path.join(folder_to_be_created, 'config.yml')

        f = open(file_to_be_created, "a")
        f.write(ebLocalConfigurator.getConfigurationContent())
        f.close()

        return ebLocalConfigurator
        

    def get_name(self) -> str:
        return 'app-' + str(math.ceil(random() * 10000))