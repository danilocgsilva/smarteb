from danilocgsilvame_python_helpers.DcgsPythonHelpers import DcgsPythonHelpers
from smart_eb.EBFormater import EBFormater
from smart_eb.EbLocalConfigurator import EbLocalConfigurator
from awsutils.AWSUtils import AWSUtils
from random import random
from zipfile import ZipFile
from shutil import copy2
import boto3
import math
import os
import subprocess
import time
import botocore

class EbClient:

    def __init__(self):
        os.environ['AWS_PROFILE'] = AWSUtils().guessLocalProfile()
        self.eb_client = boto3.client('elasticbeanstalk')
        self.userId = boto3.client('sts').get_caller_identity().get('Account')

    def new(self, path: str, name: str) -> EBFormater:
        
        os.makedirs(path)
        ebLocalConfigurator = self.create_eb_config(name, path)
        application_name = ebLocalConfigurator.getApplicationName()

        fileres = open(os.path.join(path, "index.php"), "a")
        fileres.write("<?php\n\nprint(\"Hello World from " + application_name + "!!!\");\n\n")
        fileres.close()

        customKeyConfigData = '''option_settings:
  - namespace: aws:autoscaling:launchconfiguration
    option_name: EC2KeyName
    value: ''' + AWSUtils().get_key_pair_name()
        self.__add_ebextension(path, "customkey", customKeyConfigData)

        install_composer_scripts = '''container_commands:
  sethome:
    command: "export HOME=/root"
  getcomposer:
    command: "curl -sS https://getcomposer.org/installer | sudo php"
  movetoglobalacessible:
    command: "mv composer.phar /usr/local/bin/composer"
  setcomposerexecutable:
    command: "chmod +x /usr/local/bin/composer"'''
        self.__add_ebextension(path, "commands", install_composer_scripts)

        versionAppName = 'version1'

        self.prepareWithGit(path)

        self.sendToS3(application_name, versionAppName, path)

        print("Creating the application " + name)
        response = self.eb_client.create_application(ApplicationName=name)

        print("Creating the application version " + versionAppName)
        self.eb_client.create_application_version(
            ApplicationName=name,
            VersionLabel=versionAppName,
            SourceBundle={
                'S3Bucket': 'elasticbeanstalk-us-east-1-' + self.userId,
                'S3Key': name + '/' + versionAppName + '.zip'
            },
            Process=True,
        )

        time_to_wait_in_seconds = 5
        print("Waiting " + str(time_to_wait_in_seconds) + " seconds...")
        time.sleep(time_to_wait_in_seconds)

        print("Creating the environment for application " + name)
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

        print("Awaiting to the environment becomes ready. It may be ready within 2 minutes.")

        waiter = self.eb_client.get_waiter('environment_exists')

        try:
            waiter.wait(ApplicationName=name)
            apdata = self.eb_client.describe_environments(ApplicationName=name)
            env_data = apdata["Environments"][0]
            
            env_address = "http://" + env_data["CNAME"]
            print("Now you can access your environment in: " + env_address)

            return EBFormater().setApplicationData(response["Application"])

        except botocore.exceptions.WaiterError:
            print("Does not worked! Sorry...")
        
    def list(self) -> str:
        response_data = self.eb_client.describe_applications()

        eb_data_list = []
        for ebdata in response_data["Applications"]:
            eb_data_list.append(EBFormater().setApplicationData(ebdata))

        return eb_data_list

    def deleteApp(self, app_name: str):

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

        keyNameGuessed = AWSUtils().get_key_pair_name()
        if keyNameGuessed != "":
            ebLocalConfigurator.setDefaultEc2Keyname(keyNameGuessed)
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
        subprocess.call(['git', 'add', '.'])
        subprocess.call(['git', 'commit', '-m', "First commit"])
        os.chdir(current_path)

    def sendToS3(self, app_name_version: str, version: str, path: str):
        original_dir = os.getcwd()
        os.chdir(path)
        zipFilename = version + '.zip'

        zipObj = ZipFile(zipFilename, 'w')

        # for root, subdirs, files in os.walk("."):
        #     if root != ".":
        #         zipObj.write(root[2:])

        # zipObj.write('index.php')
        # zipObj.write(os.path.join('.elasticbeanstalk', 'config.yml'))
        # zipObj.write(os.path.join('.ebextensions', 'customkey.config'))

        # for file in files:
        #     print(os.path.join(root, file))

        for root, subdirs, files in os.walk("."):
            for file in files:
                if file != zipFilename:
                    zipObj.write(os.path.join(root, file))

        zipObj.close()

        s3_client = boto3.client('s3')
        s3_client.upload_file(zipFilename, 'elasticbeanstalk-us-east-1-' + self.userId, app_name_version + "/" + zipFilename)
        os.chdir(original_dir)

    def killSeveralAppsAtOnce(self, apps_list: list):

        for app_option in apps_list:
            if app_option == "":
                option_invalid_message = "There are invalid options in the set of apps to be deleted."
                raise Exception(option_invalid_message)

        if len(apps_list) == 0:
            raise Exception("You provided an empty list for deleting apps")

        for app in apps_list:
            self.deleteApp(app)

    def killDEEPLYSeveralAppsAtOnce(self, apps_to_destroy: list):
        for app_to_destroy in apps_to_destroy:
            print("Lets destroy this app: " + app_to_destroy)
            for environmentId in EBFormater().setEnvironmentResponse(
                self.eb_client.describe_environments(ApplicationName=app_to_destroy)
            ).getAllEnvironmentsIds():
                self.eb_client.terminate_environment(EnvironmentId=environmentId)
            print("Now the application " + app_to_destroy + " will varnish...")
            self.deleteApp(app_to_destroy)


    def __add_ebextension(self, path: str, filename: str, filecontent: str):
        ebextension_path = os.path.join(path, '.ebextensions')
        if not os.path.isfile(ebextension_path):
            os.makedirs(ebextension_path)
        config_env_name = os.path.join(ebextension_path, filename + ".config")

        f = open(config_env_name, "a")
        f.write(filecontent)
        f.close()