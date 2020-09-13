from smart_eb.EbClient import EbClient
from smart_eb.UserCall import UserCall
import os
import re
import sys


def main():

    user_command = UserCall().getUserCall()

    if re.search("^(list|)$", user_command):
        print("Lets list")
    elif user_command == "new":
        print("Lets create a new.")
        EbClient().new(os.getcwd())

    # EbClient().new('/')

