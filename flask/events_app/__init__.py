import os, logging
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from logging.handlers import RotatingFileHandler

from .config import *

db = SQLAlchemy()

def configure_logging():
    logs_dir = 'logs'

    os.makedirs(logs_dir, exist_ok = True)

    logsize = 10 * 10 * 1024 # 10MB
    handler = RotatingFileHandler(os.path.join(logs_dir, 'app.log'), 
                                       maxBytes = logsize, backupCount = 3)

    handler.setFormatter(logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    ))
    handler.setLevel(logging.INFO)

    return handler

def create_app(mode=None):
    app = Flask(__name__)

    file_handler = configure_logging()
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)

    if mode is None:
        mode = os.environ.get('RUNTIME_MODE', 'dev')

    if mode == 'test':
        app.config.from_object(TestConfig)
        app.config["WTF_CSRF_ENABLED"] = False
    elif mode == 'dev':
        app.config.from_object(DevConfig)
    elif mode == 'prod':
        app.config.from_object(ProdConfig)

    db.init_app(app)

    Migrate(app, db)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .events import events_bp
    app.register_blueprint(events_bp)

    return app