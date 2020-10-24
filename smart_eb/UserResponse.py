from smart_eb.PrintHelpsTraits import PrintHelpsTraits
from smart_eb.UserSureResponseTrait import UserSureResponseTrait

class UserResponse(PrintHelpsTraits, UserSureResponseTrait):

    def setList(self, data: list):
        self.data = data
        return self

    def setEbData(self, ebdata: dict):
        self.ebdata = ebdata
        return self

    def printFromList(self):
        print("Here follows the application name in the cloud:")
        for ebdata in self.data:
            print("* " + ebdata.getApplicationName())

    def printFromNew(self):
        just_created_app_name = self.ebdata.getApplicationName()
        print("The name of new application is " + just_created_app_name)


