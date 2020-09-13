import sys

class UserCall:
    def getUserCall(self) -> str:
        try:
            return sys.argv[1]
        except IndexError:
            return ""


