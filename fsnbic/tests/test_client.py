import os
import sys
import logging
import unittest
import functools

# Needs add fsnbic parent to path to allow absolute import
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from fsnbic import session
from fsnbic import client

from fsnbic.tests.test_session import frequency_limit

class TestLogin(unittest.TestCase):

    @classmethod
    @frequency_limit
    def setUpClass(cls):

        cls.invalid_user = 'Invalid93#!'
        cls.user = os.environ['FUSIONSOLAR_USER']
        cls.invalid_password = 'Invalid99#!'
        cls.password = os.environ['FUSIONSOLAR_PASSWORD']

        # Create session and login
        cls.session = session.Session(user=cls.user, password=cls.password)
        cls.session.login()

    @classmethod
    @frequency_limit
    def tearDownClass(cls):
        cls.session.logout()

    def test_invalid_user_request(self):
        with self.assertRaises(session.LoginFailed) as context:
            s = session.Session(user=self.invalid_user,
                                password=self.invalid_password)
            with session.Client(session=s) as client:
                stations = client.get_station_list()

    @frequency_limit
    def test_not_logged_request(self):
        s = session.Session(user=self.user, password=self.password)
        client = session.Client(session=s)
        stations = client.get_station_list()

    @frequency_limit
    def test_request(self):
        with session.Client(session=self.session) as client:
            stations = client.get_station_list()


if __name__ == '__main__':
    unittest.main()
