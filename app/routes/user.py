from flask import Flask, Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from sqlalchemy import exists
from app.models import db, User

bp = Blueprint('user', __name__, url_prefix="/api/user")


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
      'id': len(User.query.all()) + 1,
      'user_name': data['userName'],
      'first_name': data['firstName'],
      'last_name': data['lastName'],
      'email': data['email'],
  }

  user = User(**new_user)
  user.set_password = data['password']

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
