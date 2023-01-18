
import os
import logging
import unittest
from . import session

logging.basicConfig(encoding='utf-8', level=logging.DEBUG)


class TestLogin(unittest.TestCase):

    def setUp(self) -> None:
        self.invalid_user = 'Invalid93#!'
        self.user = os.environ.get('FUSIONSOLAR_USER', self.invalid_user)
        self.invalid_password = 'Invalid99#!'
        self.password = os.environ.get(
            'FUSIONSOLAR_PASSWORD', self.invalid_password)

    def test_invalid_user(self):
        with self.assertRaises(session.LoginFailed) as context:
            with session.Session(user=self.invalid_user, password=self.invalid_password):
                pass

    def test_invalid_password(self):
        with self.assertRaises(session.LoginFailed) as context:
            with session.Session(user=self.user, password=self.invalid_password):
                pass

    def test_request(self):
        with session.Session(user=self.user, password=self.password) as s:
            with session.FusionRequest(session=s) as fr:
                stations = fr.get_station_list()

    def test_invalid_user_request(self):
        with self.assertRaises(session.LoginFailed) as context:
            s = session.Session(user=self.invalid_user,
                                password=self.invalid_password)
            with session.FusionRequest(session=s) as fr:
                stations = fr.get_station_list()

    def test_not_logged_request(self):
        s = session.Session(user=self.user, password=self.password)
        fr = session.FusionRequest(session=s)
        stations = fr.get_station_list()


if __name__ == '__main__':
    unittest.main()
