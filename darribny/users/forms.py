# Form Based Imports
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import (StringField, BooleanField, DateTimeField,
                     RadioField,SelectField,TextField,
                     TextAreaField,SubmitField,IntegerField,PasswordField)
from wtforms.fields.html5 import DateField, DateTimeField
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

    mobile = StringField('Mobile', validators=[DataRequired()], render_kw={"placeholder": "05xxxxxxxx"})

    gender = SelectField('Gender',
                          choices=[('NA','Select your gender'),('Male', 'Male'), ('Female', 'Female')], validators= [AnyOf(values=['Male','Female'], message='Choose your gender!')])

    role = SelectField('Role',
                          choices=[('NA','Select your role'),('trainee', 'Trainee'), ('trainer', 'Trainer')], validators= [AnyOf(values=['trainee','trainer'], message='Choose your role!')])

    city = SelectField('City',
                          choices=[('NA','Select your city'),('Jeddah', 'Jeddah'), ('Riyadh', 'Riyadh'), ('Dammam', 'Dammam')], validators=[AnyOf(values=['Jeddah','Riyadh','Dammam'], message='Choose your city!')])  
      
    birthdate = DateField('Birthdate', format='%Y-%m-%d',validators=[DataRequired()])

    email = StringField('Email', validators=[DataRequired(message='Email is required!'),Email()])

    username = StringField('Username', validators=[DataRequired(message='Username is required!')])

    password = PasswordField('Password', validators=[DataRequired(), EqualTo('pass_confirm', message='Passwords Must Match!')])

    pass_confirm = PasswordField('Confirm password', validators=[DataRequired()])

    # recaptcha = RecaptchaField()

    submit = SubmitField('Register!')

    def validate_email(self, field):
        # Check if not None for that user email!
        if Trainee.query.filter_by(email=field.data).first():
            raise ValidationError('Your email has been registered already!')

    def validate_username(self, field):
        # Check if not None for that username!
        if Trainee.query.filter_by(username=field.data).first():
            raise ValidationError('Sorry, that username is taken!')

    def validate_mobile(self, field):
        # Check if not None for that username!
        if len(field.data) != 10:
            raise ValidationError('Invalid mobile number!')


class UpdateUserForm(FlaskForm):
    picture = FileField('', validators=[FileAllowed(['jpg', 'png'])])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    mobile = StringField('Mobile', validators=[DataRequired()], render_kw={"placeholder": "05xxxxxxxx"})
    gender = SelectField('Gender',
                          choices=[('NA','Select your gender'),('Male', 'Male'), ('Female', 'Female')], validators= [AnyOf(values=['Male','Female'], message='Choose your gender!')])
    city = SelectField('City',
                          choices=[('NA','Select your city'),('Jeddah', 'Jeddah'), ('Riyadh', 'Riyadh'), ('Dammam', 'Dammam')], validators=[AnyOf(values=['Jeddah','Riyadh','Dammam'], message='Choose your city!')])    
    birthdate = DateField('Birthdate', format='%Y-%m-%d',validators=[DataRequired()])
    submit = SubmitField('Save Changes')

    def validate_email(self, email):
        if email.data != current_user.email:
            if Trainee.query.filter_by(email=email.data).first():
                raise ValidationError('Email has been registered')

    def validate_username(self, username):
        if username.data != current_user.username:
            if Trainee.query.filter_by(username=username.data).first():
                raise ValidationError('Username has been registered')
