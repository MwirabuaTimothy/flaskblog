import unittest
from flaskblog import helpers
def test_valid_user_registration(self):
    response = self.register('tim', 'tim@gmail.com', 'test', 'test')
    self.assertEqual(response.status_code, 200)
    self.assertIn(b'Account created for tim!', response.data)
    # self.assertIn(b'Thanks for registering!', response.data)