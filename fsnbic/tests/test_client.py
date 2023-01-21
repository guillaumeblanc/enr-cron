import os
import sys
import logging
import unittest
import functools

# Needs add fsnbic parent to path to allow absolute import
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from fsnbic.session import Session
from fsnbic.client import Client
from fsnbic import exception

from fsnbic.tests.test_session import frequency_limit

class TestClient(unittest.TestCase):

    @classmethod
    @frequency_limit
    def setUpClass(cls):

        cls.invalid_user = 'Invalid93#!'
        cls.user = os.environ['FUSIONSOLAR_USER']
        cls.invalid_password = 'Invalid99#!'
        cls.password = os.environ['FUSIONSOLAR_PASSWORD']

        # Create session and login
        cls.session = Session(user=cls.user, password=cls.password)
        cls.session.login()

    @classmethod
    @frequency_limit
    def tearDownClass(cls):
        cls.session.logout()

    def test_invalid_user_request(self):
        with self.assertRaises(exception.LoginFailed) as context:
            s = Session(user=self.invalid_user,
                                password=self.invalid_password)
            with Client(session=s) as client:
                plants = client.get_plant_list()

    @frequency_limit
    def test_not_logged_request(self):
        s = Session(user=self.user, password=self.password)
        client = Client(session=s)
        plants = client.get_plant_list()

    @frequency_limit
    def test_request(self):
        with Client(session=self.session) as client:
            plants = client.get_plant_list()


if __name__ == '__main__':
    unittest.main()
