import os, logging
from flask import Flask, render_template, request, flash, redirect, url_for, abort
from flask_migrate import Migrate
from sqlalchemy.exc import IntegrityError, DataError
from logging.handlers import RotatingFileHandler
import yaml
import pika
from models import db, Event
from forms import *
from prefs import Prefs
from routes import main_bp

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
        app.config.from_object('config.TestConfig')
        app.config["WTF_CSRF_ENABLED"] = False
    elif mode == 'dev':
        app.config.from_object('config.DevConfig')
    elif mode == 'prod':
        app.config.from_object('config.ProdConfig')

    db.init_app(app)

    Migrate(app, db)

    app.register_blueprint(main_bp)

    return app