from flask_wtf import FlaskForm
from wtforms import SubmitField, ValidationError
from wtforms.fields.html5 import DateTimeField
from wtforms.validators import DataRequired
from datetime import datetime


class ReservationForm(FlaskForm):
    start_time = DateTimeField('Choose a date and time in this format: YYYY-DD-MM HH:MM', format='%Y-%m-%d %H:%M', validators=[DataRequired()], render_kw={"placeholder": 'YYYY-DD-MM HH:MM'})
    submit = SubmitField('Book!')

    def validate_start_time(self, start_time):
        if start_time.data < datetime.now():
            raise ValidationError("Start datetime is invalid.")