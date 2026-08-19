import os

class Config:
    DEBUG = True
    SECRET_KEY = 'verysecret'

class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///tests.db'

class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///events.db'

class ProdConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI', 'undefined')
    SECRET_KEY = os.environ.get('SECRET_KEY', Config.SECRET_KEY)