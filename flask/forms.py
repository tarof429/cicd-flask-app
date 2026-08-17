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
                     format="%m/%d/%Y",
                     validators=[
                         DataRequired()
                     ]
    )
    time = TimeField('Time',
                     format="%I:%M %p",
                     validators=[
                         DataRequired()
                     ]
    )
    submit = SubmitField('Submit')