from smart_eb.EbClient import EbClient
from smart_eb.UserCall import UserCall
import os
import re
import sys


def main():

    user_command = UserCall().getUserCall()

    eb_client = EbClient()

    if re.search("^(list|)$", user_command):
        print("Lets list")
        print(eb_client.list())
    elif user_command == "new":
        print("Lets create a new.")
        eb_client.new(os.getcwd(), get_name())

    # EbClient().new('/')

def get_name() -> str:
    return EbClient().get_name()
