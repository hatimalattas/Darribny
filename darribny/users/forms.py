# Form Based Imports
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import (StringField, BooleanField, DateTimeField,
                     RadioField,SelectField,TextField,
                     TextAreaField,SubmitField,IntegerField,PasswordField)
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired,Email,EqualTo,AnyOf, NumberRange, Length
from wtforms import ValidationError
from flask_wtf.file import FileField, FileAllowed

# User Based Imports
from flask_login import current_user
from darribny.models import Trainee




class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(message='Email is required!'),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])

    last_name = StringField('Last Name', validators=[DataRequired()])

    mobile = StringField('Mobile', validators=[DataRequired(), Length(min=10, max=10, message='Please enter a valid mobile number!')], render_kw={"placeholder": "05xxxxxxxx"})

    gender = SelectField('Gender',
                          choices=[('NA','Select your gender'),('Male', 'Male'), ('Female', 'Female')], validators= [AnyOf(values=['Male','Female'], message='Choose your gender!')])

    city = SelectField('City',
                          choices=[('NA','Select your city'),('Jeddah', 'Jeddah'), ('Riyadh', 'Riyadh'), ('Dammam', 'Dammam')], validators=[AnyOf(values=['Jeddah','Riyadh','Dammam'], message='Choose your city!')])  
      
    birthdate = DateField('Birthdate', format='%Y-%m-%d',validators=[DataRequired()])

    email = StringField('Email', validators=[DataRequired(message='Email is required!'),Email()])

    username = StringField('Username', validators=[DataRequired(message='Username is required!')])

    password = PasswordField('Password', validators=[DataRequired(), EqualTo('pass_confirm', message='Passwords Must Match!'), Length(min=8, max=80, message='Password must be between 8 and 80 characters long!')])

    pass_confirm = PasswordField('Confirm password', validators=[DataRequired()])

    recaptcha = RecaptchaField()

    submit = SubmitField('Register!')

    def validate_email(self, field):
        # Check if not None for that user email!
        if Trainee.query.filter_by(email=field.data).first():
            raise ValidationError('Your email has been registered already!')

    def validate_username(self, field):
        # Check if not None for that username!
        if Trainee.query.filter_by(username=field.data).first():
            raise ValidationError('Sorry, that username is taken!')


class UpdateUserForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    username = StringField('Username', validators=[DataRequired()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_email(self, field):
        # Check if not None for that user email!
        if Trainee.query.filter_by(email=field.data).first():
            raise ValidationError('Your email has been registered already!')

    def validate_username(self, field):
        # Check if not None for that username!
        if Trainee.query.filter_by(username=field.data).first():
            raise ValidationError('Sorry, that username is taken!')
