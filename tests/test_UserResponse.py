import unittest
import sys
sys.path.insert(1, "..")
from smart_eb.UserResponse import UserResponse


class test_UserResponse(unittest.TestCase):
    
    def setUp(self):
        self.userResponse = UserResponse()

    def test_setDataFluentInterface(self):
        resulting_object = self.userResponse.setList({})
        self.assertTrue(isinstance(resulting_object, UserResponse))
