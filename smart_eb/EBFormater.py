class EBFormater:

    def setApplicationData(self, applicationData: dict):
        self.application_data_dict = applicationData
        return self

    def setEnvironmentData(self, environmentData: dict):
        self.environments_data = environmentData
        return self

    def setEnvironmentResponse(self, environmentResponse: dict):
        self.environments_response = environmentResponse
        self.environments_data = self.environments_response["Environments"]
        return self

    def getApplicationName(self) -> str:
        return self.application_data_dict["ApplicationName"]

    def getAllEnvironmentsIds(self) -> list:
        environmentsIds = []
        for environmentData in self.environments_data:
            environmentsIds.append(environmentData["EnvironmentId"])
        return environmentsIds
