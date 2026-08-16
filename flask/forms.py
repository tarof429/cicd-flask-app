from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class AddEventForm(FlaskForm):
    title = StringField('Title')
    submit = SubmitField('Submit')