class UserResponse:

    def setList(self, data: list):
        self.data = data
        return self

    def setEbData(self, ebdata: dict):
        self.ebdata = ebdata
        return self

    def printFromList(self):
        print("Here follows the application name in the cloud:")
        for ebdata in self.data:
            print("* " + ebdata.getName())

    def printFromNew(self):
        just_created_app_name = self.ebdata.getName()
        print("The name of new application is " + just_created_app_name)

    def printHelpForDelete(self):
        help_text = "Almost there... You need inform the applications name to delete with the following sintaxe:\n"
        help_text += "-> smeb delete:your_app_name <-\n"
        help_text += "If you wanna to delete several applications at same time, type:\n"
        help_text += "-> smeb delete:your_app_1,your_app_2,your_app_3 <-"
        print(help_text)

    def getSureForTotalDestructionWithoutSecondChance(self, applications: list) -> bool:
        for rep in range(10):
            print(".")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("------------------------------------------------------------------")
        print("ARE YOU SURE YOU WANT DO DELETE WITHOUT ANY REGREAT THE FOLLOWING APPLICATIONS?")
        for app in applications:
            print("* " + app)
        print("YOU CANNOT UNDO THIS ACTION.")
        user_response_to_dander = input("ARE YOU SURE? (type \"yes\" if so): ")
        if user_response_to_dander.lower() == "yes":
            return True
        elif user_response_to_dander == "no":
            print("Ok! Better think a little more...")
        else:
            print("I did not understood the response. But in doubt, better do not proceed do deletion...")
        return False
    
