from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TimeField, IntegerField, SubmitField, EmailField, PasswordField
from wtforms.validators import DataRequired, Length, NumberRange

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

class PreferencesForm(FlaskForm):
    fromEmail = EmailField('From e-mail address')
    toEmail = EmailField('To e-mail address')
    notificationDelay = IntegerField('Notification delay',
                            default = 0,
                            validators = [
                                NumberRange(min = 0, max=60,
                                            message= 'Delay must be a number between 0 and 60')
                            ])
    submit = SubmitField('Save')
    cancel = SubmitField('Cancel')

class LoginForm(FlaskForm):
    username = StringField('Username',
                           validators = [
                               DataRequired(),
                               Length(max=25,
                                      message='Username requried')
                           ])
    password = PasswordField('Password',
                           validators = [
                               DataRequired(),
                               Length(max=25,
                                      message='Password requried')
                           ])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField('Username',
                           validators = [
                               DataRequired(),
                               Length(max=25,
                                      message='Username requried')
                           ])
    password = PasswordField('Password',
                           validators = [
                               DataRequired(),
                               Length(max=25,
                                      message='Password requried')
                           ])
    name = StringField('Name',
                           validators = [
                               DataRequired(),
                               Length(max=25,
                                      message='Name requried')
                           ])
    
    submit = SubmitField('Register')
    cancel = SubmitField('Cancel')