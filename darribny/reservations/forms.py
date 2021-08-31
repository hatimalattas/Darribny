from flask_wtf import FlaskForm
from wtforms import SubmitField, ValidationError
from wtforms.fields.html5 import DateField, TimeField
from datetime import datetime


class ReservationForm(FlaskForm):
    date = DateField("Date")
    time = TimeField("Time")
    submit = SubmitField('Book Session!')

    def validate_date(self, date):
        if date.data < datetime.now().strftime('%d-%m-%Y'):
            raise ValidationError("The date you selected is in the past!")
