
import os
import unittest
import session

kInvalid = 'Invalid93#!'
kUser = os.environ.get('FUSIONSOLAR_USER', kInvalid)
kPassword = os.environ.get('FUSIONSOLAR_PASSWORD', kInvalid)

class TestLogin(unittest.TestCase):
  def setUp(self):
    self.session = session.Session(user=kUser, password=kPassword)

  def tearDown(self):
    self.session.dispose()

  def test_invalid_user(self):
    with self.assertRaises(ValueError) as context:
      with session.Session(user=kInvalid, password=kInvalid) :
        pass

  def test_invalid_password(self):
    with self.assertRaises(ValueError) as context:
      with session.Session(user=kUser, password=kInvalid) :
        pass

if __name__ == '__main__':
    unittest.main()
