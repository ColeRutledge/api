from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy()


class User(db.Model):
  __tablename__ = 'users'

  id = db.Column(db.Integer, primary_key=True)
  user_name = db.Column(db.String(50), nullable=False)
  first_name = db.Column(db.String(50), nullable=False)
  last_name = db.Column(db.String(50), nullable=False)
  email = db.Column(db.String(255), nullable=False, unique=True)
  hashed_password = db.Column(db.String(128))

  @property
  def password(self):
    return self.hashed_password

  @password.setter
  def set_password(self, password):
    self.hashed_password = generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.password, password)

  def get_token(self):
    return create_access_token(identity={'email': self.email, 'id': self.id})

  def to_dict(self):
    return {"id": self.id, "user_name": self.user_name, "first_name": self.first_name, "last_name": self.last_name, "email": self.email}


class Posting(db.Model):
  __tablename__ = 'postings'

  id = db.Column(db.Integer, primary_key=True)
  job_title = db.Column(db.String(255), nullable=False)
  company = db.Column(db.String(255), nullable=False)
  city = db.Column(db.String(100), nullable=False)
  state = db.Column(db.String(50), nullable=False)
  formatted_location = db.Column(db.String(255))
  source = db.Column(db.String(255))
  date = db.Column(db.DateTime)
  snippet = db.Column(db.Text)
  url = db.Column(db.Text, nullable=False)
  latitude = db.Column(db.Float)
  longitude = db.Column(db.Float)
  job_key = db.Column(db.String(100))
  expired = db.Column(db.Boolean)
  indeed_apply = db.Column(db.Boolean)
  ff_location = db.Column(db.String(255))
  rel_time = db.Column(db.String(255))
