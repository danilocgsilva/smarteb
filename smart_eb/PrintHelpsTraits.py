class PrintHelpsTraits:

    def printHelpForDelete(self):
        help_text = "Almost there... You need inform the applications name to delete with the following sintaxe:\n"
        help_text += "-> smeb delete:your_app_name <-\n"
        help_text += "If you wanna to delete several applications at same time, type:\n"
        help_text += "-> smeb delete:your_app_1,your_app_2,your_app_3 <-"
        print(help_text)

    def printHelpForDestroy(self):
        help_text = "Almost there... You need inform the applications name to be destroyied altogher along with its environments. The sintaxy is:\n"
        help_text += "-> smeb destroy:your_app_name <-\n"
        help_text += "If you wanna to destroy several applications at same time and kill all its environments as well, type:\n"
        help_text += "-> smeb destroy:your_app_1,your_app_2,your_app_3 <-"
        print(help_text)