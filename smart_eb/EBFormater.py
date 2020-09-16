class EBFormater:

    def __init__(self, eb_application_data: dict):
        self.data_dict = eb_application_data

    def getName(self) -> str:
        return self.data_dict["ApplicationName"]
