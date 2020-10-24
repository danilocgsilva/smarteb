from smart_eb.EbClient import EbClient
from smart_eb.UserCall import UserCall
from smart_eb.UserResponse import UserResponse
from smart_eb.EBFormater import EBFormater
from awsguesslocalprofile.AWSGuessLocalProfile import AWSGuessLocalProfile
from pathlib import Path
import os
import re
import sys


def main():

    user_response = UserResponse()

    user_command = UserCall().getUserCall()

    eb_client = EbClient()

    if re.search("^(list|)$", user_command.getUserCommand()):
        user_response.setList(eb_client.list()).printFromList()
    elif user_command.getUserCommand() == "new":
        app_name = get_name()
        full_directory_path = os.path.join(str(Path.home()), app_name)
        ebdata = eb_client.new(full_directory_path, app_name)
        user_response.setEbData(ebdata)
    elif re.search("^delete", user_command.getUserCommand()):
        if not re.search("^delete:", user_command.getUserCommand()):
            user_response.printHelpForDelete()
        else:
            user_arguments = user_command.getUserArguments()
            apps_to_delete = user_arguments.split(",")
            if user_response.getSureForTotalDestructionWithoutSecondChance(apps_to_delete):
                eb_client.killSeveralAppsAtOnce(apps_to_delete)
    elif re.search("^destroy", user_command.getUserCommand()):
        if not re.search("^destroy:", user_command.getUserCommand()):
            user_response.printHelpForDestroy()
        else:
            user_arguments = user_command.getUserArguments()
            apps_to_destroy = user_arguments.split(",")
            if user_response.getSureForTotalDEEPDestructionWithoutSecondChance(apps_to_destroy):
                for app_to_destroy in apps_to_destroy:
                    print("Lets destroy this app: " + app_to_destroy)
                    for environmentId in EBFormater().setEnvironmentResponse(
                        eb_client.eb_client.describe_environments(ApplicationName=app_to_destroy)
                    ).getAllEnvironmentsIds():
                        eb_client.eb_client.terminate_environment(EnvironmentId=environmentId)
                    print("Now the application " + app_to_destroy + " will varnish...")
                    eb_client.deleteApp(app_to_destroy)
    else:
        print("I still does not have implemented such command: " + user_command)

def get_name() -> str:
    return EbClient().get_name()

def create_eb_config(app_name: str):
    EbClient().create_eb_config(app_name)
