from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy()


bookmarks = db.Table(
    'bookmarks',
    db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('posting_id', db.Integer, db.ForeignKey('postings.id'), primary_key=True),
)


class User(db.Model):
  __tablename__ = 'users'

  id = db.Column(db.Integer, primary_key=True)
  user_name = db.Column(db.String(50), nullable=False)
  first_name = db.Column(db.String(50), nullable=False)
  last_name = db.Column(db.String(50), nullable=False)
  email = db.Column(db.String(255), nullable=False, unique=True)
  hashed_password = db.Column(db.String(128))

  postings = db.relationship('Posting', secondary=bookmarks, back_populates='users')
  searches = db.relationship('Search', back_populates='user', cascade='all, delete-orphan')

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


class Search(db.Model):
  __tablename__ = 'searches'

  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
  search_radius = db.Column(db.Integer, default=25, nullable=False)
  technologies = db.Column(db.JSON, default='javascript', nullable=False)
  # market_id = db.Column(db.Integer, db.ForeignKey('markets.id'), nullable=False)

  user = db.relationship('User', back_populates='searches')


class Posting(db.Model):
  __tablename__ = 'postings'

  id = db.Column(db.Integer, primary_key=True)
  search_terms = db.Column(db.String(100), nullable=False)
  search_loc = db.Column(db.String(100), nullable=False)
  title = db.Column(db.String(255), nullable=False)
  location = db.Column(db.String(255), nullable=False)
  company = db.Column(db.String(255), nullable=False)
  salary = db.Column(db.String(255), nullable=False)
  date = db.Column(db.String(255), nullable=False)
  snippet = db.Column(db.Text, nullable=False)
  description = db.Column(db.Text, nullable=False)
  link = db.Column(db.Text, nullable=False)
  formatted_sal = db.Column(db.Integer)
  js_count = db.Column(db.Integer)
  python_count = db.Column(db.Integer)
  ruby_count = db.Column(db.Integer)
  net_count = db.Column(db.Integer)
  java_count = db.Column(db.Integer)

  users = db.relationship('User', secondary=bookmarks, back_populates='postings')


class AvgMktSalary(db.Model):
  __tablename__ = 'avg_mkt_salaries'

  id = db.Column(db.Integer, primary_key=True)
  search_terms = db.Column(db.String(100), nullable=False)
  search_loc = db.Column(db.String(100), nullable=False)
  formatted_sal = db.Column(db.Integer)


class MarketMetric(db.Model):
  __tablename__ = 'market_metrics'

  id = db.Column(db.Integer, primary_key=True)
  search_terms = db.Column(db.String(100), nullable=False)
  search_loc = db.Column(db.String(100), nullable=False)
  pos_counts_mkt = db.Column(db.Integer)
  pos_pcts_mkt = db.Column(db.Float)
  pos_overall_mkt_pct = db.Column(db.Float)


# source = db.Column(db.String(255))
# city = db.Column(db.String(100), nullable=False)
# state = db.Column(db.String(50), nullable=False)
