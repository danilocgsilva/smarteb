import unittest
import sys
sys.path.insert(1, "..")
from smart_eb.EbLocalConfigurator import EbLocalConfigurator


class test_EbLocalConfigurator(unittest.TestCase):

    def setUp(self):
        self.ebLocalConfigurator = EbLocalConfigurator()
        self.maxDiff = 10000

    def test_getConfigurationContentEmptyContent(self):

        expected_content = self.getBaseContentWithPlaceholders().format(
            "null", "null", "null",
            "null", "null", "null",
            "null", "null", "null",
            "null", "null", "null",
            "null", "null"
        )
        
        self.assertEqual(expected_content, self.ebLocalConfigurator.getConfigurationContent())

    def test_setting_application_name_default_platform_default_region(self):
        default_region = "us-east-1"
        application_name = "Application1"
        default_platform = "PHP 7.4 running on 64bit Amazon Linux 2"

        self.ebLocalConfigurator\
            .setDefaultRegion(default_region)\
            .setApplicationName(application_name)\
            .setDefaultPlatform(default_platform)

        expected_content = self.getBaseContentWithPlaceholders().format(
            "null", "null", application_name,
            "null", "null", default_platform,
            default_region, "null", "null",
            "null", "null", "null",
            "null", "null"
        )

        self.assertEqual(expected_content, self.ebLocalConfigurator.getConfigurationContent())

    def getBaseContentWithPlaceholders(self):
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
