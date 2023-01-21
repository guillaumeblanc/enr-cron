import os
import sys
import logging
import unittest
import functools

# Needs add fsnbic parent to path to allow absolute import
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from fsnbic import session
from fsnbic import exception

def frequency_limit(func):
    '''Handle frequency limits cases, which cannot ben considered as fails.'''
    @functools.wraps(func)
    def wrap(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except exception.FrequencyLimit:
            logging.warning(
                'Couldn\'t complete test due to exceeding frequency limits.')
    return wrap


class TestSession(unittest.TestCase):

    @classmethod
    @frequency_limit
    def setUpClass(cls):
        cls.invalid_user = 'Invalid93#!'
        cls.user = os.environ['FUSIONSOLAR_USER']
        cls.invalid_password = 'Invalid99#!'
        cls.password = os.environ['FUSIONSOLAR_PASSWORD']

    @classmethod
    @frequency_limit
    def tearDownClass(cls):
        pass

    def test_invalid_user(self):
        with self.assertRaises(exception.LoginFailed) as context:
            with session.Session(user=self.invalid_user, password=self.invalid_password):
                pass

    @frequency_limit
    def test_invalid_password(self):
        with self.assertRaises(exception.LoginFailed) as context:
            with session.Session(user=self.user, password=self.invalid_password):
                pass

    @frequency_limit
    def test_valid_login(self):
        with session.Session(user=self.user, password=self.password):
            pass

if __name__ == '__main__':
    unittest.main()
