import os

class Config(object):
    secret_key = 'any random string'

class DevelopmentConfig(Config):
    debug = True
