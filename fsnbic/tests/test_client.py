
import os
import sys
import datetime
import logging
import unittest
import functools

# Needs add fsnbic parent to path to allow absolute import
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../..')))

from fsnbic.tests.utils import *
import fsnbic

class TestClient(unittest.TestCase):

    @classmethod
    @frequency_limit
    def setUpClass(cls):

        cls.invalid = 'Invalid93#!'
        cls.user = os.environ['FUSIONSOLAR_USER']
        cls.password = os.environ['FUSIONSOLAR_PASSWORD']

        # Create session and login
        cls.session = fsnbic.Session(user=cls.user, password=cls.password)
        cls.session.login()

    @classmethod
    @frequency_limit
    def tearDownClass(cls):
        cls.session.logout()

    def test_login_failed_request(self):
        with self.assertRaises(exception.LoginFailed) as context:
            session = fsnbic.Session(user=self.invalid, password=self.invalid)
            with fsnbic.Client(session=session) as client:
                plants = client.get_plant_list()

    @frequency_limit
    def test_request(self):
        with fsnbic.Client(session=self.session) as client:
            plants = client.get_plant_list()
            client.get_plant_realtime_data(['aaaaaaaaaaa', 'bbbbbbbbbbbb', 'cccccccccccc'])
            client.get_plant_hourly_data(['aaaaaaaaaaa', 'bbbbbbbbbbbb', 'cccccccccccc'], date=datetime.datetime.now())


if __name__ == '__main__':
    unittest.main()
