from smart_eb.EbClient import EbClient
from smart_eb.UserCall import UserCall
import os
import re
import sys
from smart_eb.UserResponse import UserResponse


def main():

    user_response = UserResponse()

    user_command = UserCall().getUserCall()

    eb_client = EbClient()

    if re.search("^(list|)$", user_command.getUserCommand()):
        user_response.setList(eb_client.list()).printFromList()
    elif user_command.getUserCommand() == "new":
        ebdata = eb_client.new(os.getcwd(), get_name())
        user_response.setEbData(ebdata).printFromNew()
    elif re.search("^delete", user_command.getUserCommand()):
        if not re.search("^delete:", user_command.getUserCommand()):
            user_response.printHelpForDelete()
        else:
            user_arguments = user_command.getUserArguments()
            apps_to_delete = user_arguments.split(",")
            if user_response.getSureForTotalDestructionWithoutSecondChance(apps_to_delete):
                for app in apps_to_delete:
                    eb_client.delete(app)

    else:
        print("I still does not have implemented such command: " + user_command)

    # EbClient().new('/')

def get_name() -> str:
    return EbClient().get_name()
