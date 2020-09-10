import os

class EbClient:

    def init(self, path: str):

        if not os.path.exists(path):
            raise Exception("The path provided to the init method of EbClient does not exists.")

        print("Lets init!")
