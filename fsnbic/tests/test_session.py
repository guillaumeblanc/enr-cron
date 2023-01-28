import os
import sys
import logging
import unittest
import functools

# Needs add fsnbic parent to path to allow absolute import
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import fsnbic

from fsnbic.tests.utils import *

class TestSession(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.invalid = 'Invalid93#!'
        cls.user = os.environ['FUSIONSOLAR_USER']
        cls.password = os.environ['FUSIONSOLAR_PASSWORD']

    @classmethod
    def tearDownClass(cls):
        pass

    def test_invalid_user(self):
        with self.assertRaises(exception.LoginFailed) as context:
            with fsnbic.Session(user=self.invalid, password=self.invalid):
                pass

    @frequency_limit
    def test_invalid_password(self):
        with self.assertRaises(exception.LoginFailed) as context:
            with fsnbic.Session(user=self.user, password=self.invalid):
                pass

    @frequency_limit
    def test_valid_login(self):
        with fsnbic.Session(user=self.user, password=self.password):
            pass

if __name__ == '__main__':
    unittest.main()
