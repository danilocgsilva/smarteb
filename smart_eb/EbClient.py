from danilocgsilvame_python_helpers.DcgsPythonHelpers import DcgsPythonHelpers
from smart_eb.EBFormater import EBFormater
from smart_eb.EbLocalConfigurator import EbLocalConfigurator
from awsguesslocalprofile.AWSGuessLocalProfile import AWSGuessLocalProfile
from random import random
from zipfile import ZipFile
from shutil import copy2
import boto3
import math
import os
import subprocess
import time

class EbClient:

    def __init__(self):
        os.environ['AWS_PROFILE'] = AWSGuessLocalProfile().guess()
        self.eb_client = boto3.client('elasticbeanstalk')
        self.userId = boto3.client('sts').get_caller_identity().get('Account')

    def new(self, path: str, name: str) -> EBFormater:
        
        ebLocalConfigurator = self.create_eb_config(name, path)
        application_name = ebLocalConfigurator.getApplicationName()

        fileres = open(os.path.join(path, "index.php"), "a")
        fileres.write("<?php\n\nprint(\"Hello World from " + application_name + "!!!\");\n\n")
        fileres.close()

        versionAppName = 'version1'

        self.sendToS3(application_name, versionAppName)

        self.prepareWithGit(path)

        response = self.eb_client.create_application(ApplicationName=name)

        self.eb_client.create_application_version(
            ApplicationName=name,
            VersionLabel=versionAppName,
            SourceBundle={
                'S3Bucket': 'elasticbeanstalk-us-east-1-' + self.userId,
                'S3Key': name + '/' + versionAppName + '.zip'
            },
            Process=True,
        )

        self.eb_client.create_environment(
            ApplicationName=name,
            EnvironmentName=ebLocalConfigurator.getEnvironment(),
            SolutionStackName="64bit Amazon Linux 2 v3.1.1 running PHP 7.4",
            OptionSettings=[
                {
                    'Namespace': 'aws:autoscaling:launchconfiguration',
                    'OptionName': 'IamInstanceProfile',
                    'Value': 'aws-elasticbeanstalk-ec2-role'
                },
            ],
            VersionLabel=versionAppName
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
            .setDefaultRegion(boto3.session.Session().region_name)\
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

    def prepareWithGit(self, path: str):
        current_path = os.getcwd()
        os.chdir(path)
        subprocess.call(['git', 'init'])
        subprocess.call(['git', 'add', 'index.php', '.elasticbeanstalk/config.yml'])
        subprocess.call(['git', 'commit', '-m', "First commit"])
        os.chdir(current_path)

    def sendToS3(self, app_name_version: str, version: str):

        filename = version + '.zip'
        zipObj = ZipFile(filename, 'w')
        zipObj.write('index.php')
        zipObj.write(os.path.join('.elasticbeanstalk', 'config.yml'))
        zipObj.close()

        s3_client = boto3.client('s3')
        response = s3_client.upload_file(filename, 'elasticbeanstalk-us-east-1-' + self.userId, app_name_version + "/" + filename)
        print(response)

