import os

class Config:
    DEBUG = True
    SECRET_KEY = 'verysecret'

class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///tests.db'
    MESSAGE_BROKER_TYPE = os.environ.get('MESSAGE_BROKER_TYPE', 'none')

class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI', 'sqlite:///events.db')
    SECRET_KEY = os.environ.get('SECRET_KEY', Config.SECRET_KEY)    
    MESSAGE_BROKER_TYPE = os.environ.get('MESSAGE_BROKER_TYPE', 'rabbitmq')

class ProdConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI', 'undefined')
    SECRET_KEY = os.environ.get('SECRET_KEY', Config.SECRET_KEY)
    MESSAGE_BROKER_TYPE = os.environ.get('MESSAGE_BROKER_TYPE', 'none')