from flask_login import UserMixin
from . import db

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False, unique=True)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)

class User (UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(25), unique=True)
    password = db.Column(db.String(25))
    name = db.Column(db.String(25))
    role = db.Column(db.String(25))