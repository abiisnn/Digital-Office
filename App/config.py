import os

class Config(object):
    SECRET_KEY = 'any random string'

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/digital_office'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
