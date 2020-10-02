# Form Based Imports
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import (StringField, BooleanField, DateTimeField,
                     RadioField,SelectField,TextField,
                     TextAreaField,SubmitField,IntegerField,PasswordField, SelectMultipleField)
from wtforms.fields.html5 import DateField, DateTimeField
from wtforms.validators import DataRequired,Email,EqualTo,AnyOf,NumberRange,Length
from wtforms import ValidationError
from flask_wtf.file import FileField, FileAllowed

# User Based Imports
from flask_login import current_user
from darribny.models import User

class LoginForm(FlaskForm):
    email = StringField('', validators=[DataRequired(message='Email is required!'),Email()], render_kw={"placeholder": 'Email'})
    password = PasswordField('', validators=[DataRequired()], render_kw={"placeholder": 'Password'})
    submit = SubmitField('Log In')


class RegistrationForm(FlaskForm):
    first_name = StringField('', validators=[DataRequired()],render_kw={"placeholder": 'First Name'})
    last_name = StringField('', validators=[DataRequired()], render_kw={"placeholder": 'Last Name'})
    mobile = StringField('', validators=[DataRequired()], render_kw={"placeholder": " Mobile 05xxxxxxxx"})
    gender = SelectField('',
                          choices=[('NA','Gender'),('Male', 'Male'), ('Female', 'Female')], validators= [AnyOf(values=['Male','Female'], message='Select a Gender')])
    role = SelectField('',
                          choices=[('NA','Role'),('trainee', 'Trainee'), ('trainer', 'Trainer')], validators= [AnyOf(values=['trainee','trainer'], message='Select a Role')])
    city = SelectField('',
                          choices=[('NA','City'),('Jeddah', 'Jeddah'), ('Riyadh', 'Riyadh'), ('Dammam', 'Dammam')], validators=[AnyOf(values=['Jeddah','Riyadh','Dammam'], message='Select a City')])  
    birthdate = DateField('Date of Birth', format='%Y-%m-%d',validators=[DataRequired()], render_kw={"placeholder": 'Birthdate'})
    email = StringField('', validators=[DataRequired(message='Email is required!'),Email()],render_kw={"placeholder": 'Email'})
    password = PasswordField('', validators=[DataRequired()],render_kw={"placeholder": 'Password'})
    # password = PasswordField('', validators=[DataRequired(), EqualTo('pass_confirm', message='Passwords Must Match!')],render_kw={"placeholder": 'Password'})
    # pass_confirm = PasswordField('', validators=[DataRequired()],render_kw={"placeholder": 'Confirm Password'})
    submit = SubmitField('Register!')

    def validate_email(self, field):
        # Check if not None for that user email!
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Your email has been registered already!')

    def validate_mobile(self, field):
        if User.query.filter_by(mobile=field.data).first():
            raise ValidationError('Your mobile number has been registered already!')

        if len(field.data) != 10:
            raise ValidationError('Invalid mobile number!')


class UpdateUserForm(FlaskForm):
    picture = FileField('', validators=[FileAllowed(['jpg', 'png','jpeg'])])
    first_name = StringField('', validators=[DataRequired()], render_kw={"placeholder": 'First Name'})
    last_name = StringField('', validators=[DataRequired()], render_kw={"placeholder": 'Last Name'})
    mobile = StringField('', validators=[DataRequired()], render_kw={"placeholder": "05xxxxxxxx"})
    gender = SelectField('',
                          choices=[('NA','Gender'),('Male', 'Male'), ('Female', 'Female')], validators= [AnyOf(values=['Male','Female'], message='Choose your gender!')])
    city = SelectField('',
                          choices=[('NA','City'),('Jeddah', 'Jeddah'), ('Riyadh', 'Riyadh'), ('Dammam', 'Dammam')], validators=[AnyOf(values=['Jeddah','Riyadh','Dammam'], message='Choose your city!')])    
    birthdate = DateField('Date of Birth', format='%Y-%m-%d',validators=[DataRequired()])
    bio = TextAreaField('Bio', render_kw={"placeholder": 'Bio'})
    price = IntegerField('Price Per Session', render_kw={"placeholder": 'Price Per Session'})
    sports = SelectMultipleField(
        'Sports', validators=[DataRequired()],
        choices=[
            ('Cardio', 'Cardio'),
            ('Boxing', 'Boxing'),
            ('MMA', 'MMA')
        ]
    )
    submit = SubmitField('Save Changes')

    def validate_email(self, email):
        if email.data != current_user.email:
            if User.query.filter_by(email=email.data).first():
                raise ValidationError('Email has been registered')

    def validate_mobile(self, mobile):
        # Check if not None for that username!
        if len(mobile.data) != 10:
            raise ValidationError('Invalid mobile number!')
        if mobile.data != current_user.mobile:
            if User.query.filter_by(mobile=mobile.data).first():
                raise ValidationError('Mobile number has been registered')

class FilterForm(FlaskForm):
    city = SelectField('City',
                          choices=[('','Any'),('Jeddah', 'Jeddah'), ('Riyadh', 'Riyadh'), ('Dammam', 'Dammam')])

    sport = SelectField(
        'Sport',
        choices=[
            ('', 'Any'),
            ('Cardio', 'Cardio'),
            ('Boxing', 'Boxing'),
            ('MMA', 'MMA')
        ]
    )
    submit = SubmitField('Search')
