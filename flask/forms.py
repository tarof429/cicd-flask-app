from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TimeField, SubmitField
from wtforms.validators import DataRequired, Length

class AddEventForm(FlaskForm):
    title = StringField('Title',
                        validators=[
                            DataRequired(),
                            Length(max=30, message='Title must be 30 characters')
                        ]
    )
    date = DateField('Date',
                     validators=[
                         DataRequired()
                     ]
    )
    time = TimeField('Time',
                     validators=[
                         DataRequired()
                     ]
    )
    submit = SubmitField('Submit')

class UpdateEventForm(FlaskForm):
    title = StringField('Title',
        validators=[
            DataRequired(),
            Length(max=30, message='Title must be 30 characters or fewer')
        ]
    )
    date = DateField('Date')
    time = TimeField('Time')
    submit = SubmitField('Submit')