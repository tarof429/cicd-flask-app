class Config:
    DEBUG = True
    SECRET_KEY = 'verysecret'

class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///tests.db'

class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///events.db'