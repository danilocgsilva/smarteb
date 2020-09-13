import sys
import re
import tempfile
import unittest
sys.path.insert(1, "..")
from smart_eb.EbClient import EbClient


class test_EbClient(unittest.TestCase):

    def setUp(self):
        self.ebClient = EbClient()

    def test_new_path_not_exists(self):
        non_existent_path = '/path/does/not/exists'
        with self.assertRaises(OSError):
            self.ebClient.new(non_existent_path, "project_name")

    def test_new_missign_path(self):
        with self.assertRaises(OSError):
            self.ebClient.new("", "project_name")

    def test_new_missing_name(self):
        with self.assertRaises(TypeError):
            self.ebClient.new(self.getTmpPathFolder())

    def getTmpPathFolder(self):
        return tempfile.gettempdir()
