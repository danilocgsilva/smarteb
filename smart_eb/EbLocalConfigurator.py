class EbLocalConfigurator:

    def __init__(self):
        self.environment = "null"
        self.group_suffix = "null"
        self.application_name = "null"
        self.branch = "null"
        self.default_ec2_keyname = "null"
        self.default_platform = "null"
        self.default_region = "null"
        self.instance_profile = "null"
        self.platform_name = "null"
        self.platform_version = "null"
        self.profile = "null"
        self.repository = "null"
        self.sc = "null"
        self.workspace_type = "null"

    def getContentWithPlaceHolders(self):
        return """branch-defaults:
  default:
    environment: {0}
    group_suffix: {1}
global:
  application_name: {2}
  branch: {3}
  default_ec2_keyname: {4}
  default_platform: {5}
  default_region: {6}
  include_git_submodules: true
  instance_profile: {7}
  platform_name: {8}
  platform_version: {9}
  profile: {10}
  repository: {11}
  sc: {12}
  workspace_type: {13}
"""

    def getConfigurationContent(self):
        return self.getContentWithPlaceHolders().format(
            self.environment, self.group_suffix, self.application_name,
            self.branch, self.default_ec2_keyname, self.default_platform,
            self.default_region, self.instance_profile, self.platform_name,
            self.platform_version, self.profile, self.repository,
            self.sc, self.workspace_type
        )

    def setEnvironment(self, environment: str):
        self.environment = environment
        return self

    def setGroupSuffix(self, group_prefix: str):
        self.group_suffix = group_prefix
        return self

    def setApplicationName(self, application_name: str):
        self.application_name = application_name
        return self

    def setBranch(self, branch: str):
        self.branch = branch
        return self

    def setDefaultEc2Keyname(self, default_ec2_keyname: str):
        self.default_ec2_keyname = default_ec2_keyname
        return self

    def setDefaultPlatform(self, default_platform):
        self.default_platform = default_platform
        return self

    def setDefaultRegion(self, default_region: str):
        self.default_region = default_region
        return self

    def setInstanceProfile(self, instance_profile: str):
        self.instance_profile = instance_profile
        return self

    def setPlatformName(self, platform_name: str):
        self.platform_name = platform_name
        return self

    def setPlatformVersion(self, platform_version: str):
        self.platform_version = platform_version
        return self

    def setProfile(self, profile: str):
        self.profile = profile
        return self

    def setRepository(self, repository: str):
        self.repository = repository
        return self

    def setSc(self, sc: str):
        self.sc = sc
        return self

    def setWorkspacetype(self, workspace_type: str):
        self.workspace_type = workspace_type
        return self

    def getEnvironment(self) -> str:
        return self.environment

    def getDefaultPlatform(self) -> str:
        return self.default_platform

    def getApplicationName(self) -> str:
        return self.application_name

    def guess_environment_name(self):
        self.environment = self.application_name + "-env"
        return self
