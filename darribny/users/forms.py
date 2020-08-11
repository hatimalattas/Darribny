# from flask_wtf import FlaskForm
# from wtforms import (StringField, BooleanField, DateTimeField,
#                      RadioField,SelectField,TextField,
#                      TextAreaField,SubmitField,IntegerField,DateField,PasswordField)
# from wtforms.validators import DataRequired, Email, EqualTo
# from wtforms import ValidationError
# from flask_wtf.file import FileField, FileAllowed
# from flask_login import current_user
# from darribny.models import Trainee, Trainer

# class LoginForm(FlaskForm):
#     email = StringField('Email', validators=[DataRequired(),Email()])
#     password = PasswordField('Password', validators=[DataRequired()])
#     submit = SubmitField('Log In')

# class RegistrationForm(FlaskForm):
#     first_name = StringField('First Name', validators=[DataRequired()])
#     last_name = StringField('Last Name', validators=[DataRequired()])
#     mobile = IntegerField('Country Code', validators=[DataRequired()])
#     city = RadioField('Select your city', choices=[('choice_one','Jeddah'),('choice_two','Riyadh'),('choice_three','Dammam')],validators=[DataRequired()])
#     gender = RadioField('Select your gender', choices=[('choice_one','Male'),('choice_two','Female')],validators=[DataRequired()])
#     birthdate = DateField('Birthdate', format='%Y-%m-%d',validators=[DataRequired()])
#     email = StringField('Email', validators=[DataRequired(),Email()])
#     username = StringField('Username', validators=[DataRequired()])
#     password = PasswordField('Password', validators=[DataRequired(), EqualTo('pass_confirm', message='Passwords Must Match!')])
#     pass_confirm = PasswordField('Confirm password', validators=[DataRequired()])
#     submit = SubmitField('Register!')

#     def check_email(self, field):
#         if Trainee.query.filter_by(email=field.data).first():
#             raise ValidationError('Your email has been registerd already!')
#     def check_username(self, field):
#         if Trainee.query.filter_by(username=field.data).first():
#             raise ValidationError('Your username has been registerd already!')

# class UpdateForm(FlaskForm):

#     email = StringField('Email',validators=[DataRequired(),Email()])
#     username = StringField('Username',validators=[DataRequired()])
#     picture = FileField('Update Profile Picture',validators=[FileAllowed(['jpg','png'])])
#     submit = SubmitField('Update')

#     def check_email(self, field):
#         if Trainee.query.filter_by(email=field.data).first():
#             raise ValidationError('Your email has been registerd already!')
#     def check_username(self, field):
#         if Trainee.query.filter_by(username=field.data).first():
#             raise ValidationError('Your username has been registerd already!')

# Form Based Imports
from flask_wtf import FlaskForm
from wtforms import (StringField, BooleanField, DateTimeField,
                     RadioField,SelectField,TextField,
                     TextAreaField,SubmitField,IntegerField,PasswordField)
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired,Email,EqualTo
from wtforms import ValidationError
from flask_wtf.file import FileField, FileAllowed

# User Based Imports
from flask_login import current_user
from darribny.models import Trainee




class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    mobile = IntegerField('Mobile', validators=[DataRequired()])
    city = RadioField('Select your city', choices=[('choice_one','Jeddah'),('choice_two','Riyadh'),('choice_three','Dammam')],validators=[DataRequired()])
    gender = RadioField('Select your gender', choices=[('choice_one','Male'),('choice_two','Female')],validators=[DataRequired()])
    birthdate = DateField('Birthdate', format='%Y-%m-%d',validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(),Email()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('pass_confirm', message='Passwords Must Match!')])
    pass_confirm = PasswordField('Confirm password', validators=[DataRequired()])
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
