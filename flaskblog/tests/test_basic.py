import os
import unittest

from flaskblog import app, db, mail

from flaskblog.helpers import register

TEST_DB = 'test.db'
 
 
class BasicTests(unittest.TestCase):

	############################
	#### setup and teardown ####
	############################
 
	# executed prior to each test
	def setUp(self):
		app.config['TESTING'] = True
		app.config['WTF_CSRF_ENABLED'] = False
		app.config['DEBUG'] = False
		app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
			os.path.join(app.config['BASEDIR'], TEST_DB)
		self.app = app.test_client()
		db.drop_all()
		db.create_all()
 
		# Disable sending of emails during unit testing
		mail.init_app(app)
		self.assertEqual(app.debug, False)
 
	# executed after each test
	def tearDown(self):
		pass

	def assert_flashes(self, expected_message, expected_category='message'):
		with self.app.session_transaction() as session:
			try:
				category, message = session['_flashes'][0]
			except KeyError:
				raise AssertionError('nothing flashed')
			assert expected_message in message
			assert expected_category == category
 
 
###############
#### tests ####
###############
 
	def test_main_page(self):
		response = self.app.get('/', follow_redirects=True)
		self.assertEqual(response.status_code, 200)
	
	def test_valid_user_registration(self):
		response = register(self, 'tim', 'tim@gmail.com', 'test', 'test')
		self.assertEqual(response.status_code, 200)
		# self.assert_flashes('Account created for tim!')
		# self.assertIn(b'Account created for tim!', response.data)
		# self.assertIn(b'Thanks for registering!', response.data)
 
if __name__ == "__main__":
	unittest.main()
