from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import DateField, DateTimeField

class ReservationForm(FlaskForm):
    # no empty titles or text possible
    # we'll grab the date automatically from the Model later
    location = StringField('Location', validators=[DataRequired()])
    start_time = DateField('Birthdate', format='%Y-%m-%d',validators=[DataRequired()])
    submit = SubmitField('')
