import sys

class UserCall:

    def __init__(self):
        self.userCommand = None
        self.arguments = None
    
    def getUserCall(self) -> str:
        try:
            self.userCommand = sys.argv[1]
            searchArguments = self.userCommand.split(":")
            if len(searchArguments) > 1:
                self.arguments = searchArguments[1]
        except IndexError:
            self.userCommand = ""

        return self

    def getUserCommand(self) -> str:
        return self.userCommand

    def getUserArguments(self) -> str:
        return self.arguments

