from flask import Flask, Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from sqlalchemy import exists
from app.models import db, User, Search

bp = Blueprint('user', __name__, url_prefix="/api/user")


@bp.route('/<int:id>')
def get_searches(id):
  print()
  print('********GETTING USER SEARCHES********')
  print()
  user_searches = Search.query.filter(Search.user_id == id).one()
  print(user_searches)

  searches = {
      'user_id': user_searches.user_id,
      'search_radius': user_searches.search_radius,
      'technologies': user_searches.technologies,
  }

  return {'user_searches': searches}, 200


@bp.route('/login', methods=['POST'])
def login():

  data = request.get_json()
  email = data['email']
  password = data['password']

  print()
  print('********GETTING TOKEN********')
  print()

  (ret, ), = db.session.query(exists().where(User.email == email))
  if ret:
    user = User.query.filter(User.email == email).one()
    return {'token': user.get_token(), 'username': user.user_name, 'id': user.id}\
        if user.check_password(password) else {'error': 'Login failed.'}
  else:
    return {'error': 'Login failed.'}


@bp.route('/register', methods=['POST'])
def register():
  data = request.get_json()

  (ret, ), = db.session.query(exists().where(User.email == data['email']))
  if ret:
    return {'error': 'User already exists. Please try again.'}

  new_user = {
      'user_name': data['userName'],
      'first_name': data['firstName'],
      'last_name': data['lastName'],
      'email': data['email'],
  }

  user = User(**new_user)
  user.set_password = data['password']
  search = Search(user=user)

  print()
  print('*****USER ADDED*****', {**new_user, 'password': user.hashed_password[:30]})
  print()
  db.session.add(user)
  db.session.commit()
  return {'token': user.get_token(), 'username': user.user_name, 'id': user.id}, 201


# @jwt_required
@bp.route('/users')
def get_users():
  print()
  print('********GETTING USERS********')
  print()
  users = User.query.all()
  res = [{
      'id': user.id,
      'user_name': user.user_name,
      'first_name': user.first_name,
      'last_name': user.last_name,
      'email': user.email,
      'password': user.password,
  } for user in users]
  return jsonify(res), 200





# @bp.route('/test')
# def test():
#   print()
#   print('********GETTING USER SETTINGS********')
#   print()
#   user_settings = UserSettings(user_id=1)
#   res = {
#       'user_id': user_settings.user_id,
#       'search_radius': user_settings.search_radius,
#       'tech_one': user_settings.tech_one,
#       'tech_two': user_settings.tech_two,
#       'tech_three': user_settings.tech_three,
#   }

#   db.session.add(user_settings)
#   db.session.commit()

#   return {'user_settings': res}, 200
