import unittest
import sys
sys.path.insert(1, "..")
from smart_eb.EbClient import EbClient


class test_EbClient(unittest.TestCase):

    def setUp(self):
        self.ebClient = EbClient()

    def test_new_path_not_exists(self):
        non_existent_path = '/path/does/not/exists'
        with self.assertRaises(Exception):
            self.ebClient.new(non_existent_path)

    def test_new_missign_path(self):
        with self.assertRaises(Exception):
            self.ebClient.new()
