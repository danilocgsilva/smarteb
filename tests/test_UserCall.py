import unittest
import sys
sys.path.insert(1, "..")
from smart_eb.UserCall import UserCall
from unittest.mock import patch


class test_UserCall(unittest.TestCase):
    def setUp(self):
        self.userCall = UserCall()
    
    def test_getUserCallList(self):
        testargs = ["smeg", "list"]
        expected_command = 'list'
        with patch.object(sys, 'argv', testargs):
            self.assertEqual(expected_command, self.userCall.getUserCall())

    def test_getUserCallNew(self):
        testargs = ["smeg", "new"]
        expected_command = 'new'
        with patch.object(sys, 'argv', testargs):
            self.assertEqual(expected_command, self.userCall.getUserCall())
