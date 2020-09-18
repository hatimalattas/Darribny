from flask_wtf import FlaskForm
from wtforms import SubmitField, DateTimeField
from wtforms.fields.html5 import DateTimeField
from wtforms.validators import DataRequired


class ReservationForm(FlaskForm):
    start_time = DateTimeField('Book a 60 Minute Session Now! (YYYY-DD-MM HH:MM)', format='%Y-%m-%d %H:%M', validators=[DataRequired()])
    status = SubmitField('Accept')
    status = SubmitField('Decline')
    submit = SubmitField('Book!')

class ReservationAccept(FlaskForm):
    accept = SubmitField('Accept')

class ReservationDecline(FlaskForm):
    decline = SubmitField('Decline')
