from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app, jsonify
from mm import db, login_manager
from flask_login import UserMixin
from sqlalchemy.ext.declarative import DeclarativeMeta
import simplejson as json

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
	password = db.Column(db.String(60), nullable=False)
	posts = db.relationship('Post', backref='author', lazy=True)

	def get_reset_token(self, expires_sec=1800):
		s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
		return s.dumps({'user_id': self.id}).decode('utf-8')
	
	@staticmethod
	def verify_reset_token(token):
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			user_id = s.loads(token)['user_id']
		except:
			return None
		return User.query.get(user_id)

	@property
	def serialize(self):
		return {
			'id' : self.id,
			'username' : self.username,
			'email' : self.email,
			'image_file' : self.image_file,
		}
	def __repr__(self):
		return f"User('{self.username}', '{self.email}', '{self.image_file}'"


class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), nullable=False)
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	content = db.Column(db.Text, nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

	@property
	def serialize(self):
		return {
			'id' : self.id,
			'title' : self.title,
			'date_posted' : self.date_posted,
			'content' : self.content,
			'user_id' : self.user_id,
			# 'creator' : User.query.get_or_404(self.user_id).serialize,
			# This is an example how to deal with Many2Many relations
			# 'many2many' : self.serialize_many2many
		}

	def __repr__(self):
		return f"Post('{self.title}', '{self.date_posted}'"


class AlchemyEncoder(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj.__class__, DeclarativeMeta):
			# an SQLAlchemy class
			fields = {}
			for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
				data = obj.__getattribute__(field)
				try:
					json.dumps(data) # this will fail on non-encodable values, like other classes
					fields[field] = data
				except TypeError:
					fields[field] = None
			# a json-encodable dict
			return fields

		return json.JSONEncoder.default(self, obj)