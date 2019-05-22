import os

class Config(object):
    SECRET_KEY = 'any random string'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_SSL = False
    MAIL_USE_TLS = True
    MAIL_USERNAME =  'digitaloffice19@gmail.com'
    MAIL_PASSWORD =  'superpassword123'

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:n0m3l0@localhost/digital_office'
