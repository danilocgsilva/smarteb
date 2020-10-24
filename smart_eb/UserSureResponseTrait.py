class UserSureResponseTrait:
    
    def getSureForTotalDestructionWithoutSecondChance(self, applications: list) -> bool:
        self.__print_pre_text("ARE YOU SURE YOU WANT DO DELETE WITHOUT ANY REGREAT THE FOLLOWING APPLICATIONS?", applications)
        user_response_to_danger = input("ARE YOU SURE? (type \"yes\" if so): ")
        if user_response_to_danger.lower() == "yes":
            return True
        elif user_response_to_danger == "no":
            print("Ok! Better think a little more...")
        else:
            print("I did not understood the response. But in doubt, better do not proceed do deletion...")
        return False

    def getSureForTotalDEEPDestructionWithoutSecondChance(self, applications: list) -> bool:
        self.__print_pre_text("ARE YOU SURE YOU WANT DO DESTROY WITHOUT ANY REGREAT THE FOLLOWING APPLICATIONS? ITS ENVIRONMENT WILL GO AWAY AS WELL...", applications)
        user_response_to_danger = input("ARE YOU SURE? (type \"yes\" if so): ")
        if user_response_to_danger.lower() == "yes":
            return True
        elif user_response_to_danger == "no":
            print("Ok! Better think a little more...")
        else:
            print("I did not understood the response. But in doubt, better do not proceed do deletion...")
        return False

    def __print_pre_text(self, custom_message: str, applications: list):
        for rep in range(10):
            print(".")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("------------------------------------------------------------------")
        print(custom_message)
        for app in applications:
            print("* " + app)
        print("YOU CANNOT UNDO THIS ACTION.")