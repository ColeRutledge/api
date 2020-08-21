from os import environ


class Config:
  SECRET_KEY = environ.get('SECRET_KEY')
  SQLALCHEMY_ECHO = True
  JWT_ACCESS_TOKEN_EXPIRES = 10800
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URL')
