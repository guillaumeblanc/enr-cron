
import os
import logging
import unittest
import functools
from . import session
# import session


def frequency_limit(func):
    '''Handle frequency limits cases, which cannot ben considered as fails.'''
    @functools.wraps(func)
    def wrap(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except session.FrequencyLimit:
            logging.warning(
                'Couldn\'t complete test due to exceeding frequency limits.')
    return wrap


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

    def test_invalid_user(self):
        with self.assertRaises(session.LoginFailed) as context:
            with session.Session(user=self.invalid_user, password=self.invalid_password):
                pass

    @frequency_limit
    def test_invalid_password(self):
        with self.assertRaises(session.LoginFailed) as context:
            with session.Session(user=self.user, password=self.invalid_password):
                pass

    def test_invalid_user_request(self):
        with self.assertRaises(session.LoginFailed) as context:
            s = session.Session(user=self.invalid_user,
                                password=self.invalid_password)
            with session.FusionRequest(session=s) as fr:
                stations = fr.get_station_list()

    @frequency_limit
    def test_request(self):
        with session.FusionRequest(session=self.session) as fr:
            stations = fr.get_station_list()

    @frequency_limit
    def test_not_logged_request(self):
        s = session.Session(user=self.user, password=self.password)
        fr = session.FusionRequest(session=s)
        stations = fr.get_station_list()


if __name__ == '__main__':
    unittest.main()
