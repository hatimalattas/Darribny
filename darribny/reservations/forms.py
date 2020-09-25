from flask_wtf import FlaskForm
from wtforms import SubmitField, DateTimeField
from wtforms.fields.html5 import DateTimeField
from wtforms.validators import DataRequired


class ReservationForm(FlaskForm):
    start_time = DateTimeField('Choose a date and time in this format: YYYY-DD-MM HH:MM', format='%Y-%m-%d %H:%M', validators=[DataRequired()], render_kw={"placeholder": 'YYYY-DD-MM HH:MM'})
    status = SubmitField('Accept')
    status = SubmitField('Decline')
    submit = SubmitField('Book!')

class ReservationAccept(FlaskForm):
    accept = SubmitField('Accept')

class ReservationDecline(FlaskForm):
    decline = SubmitField('Decline')
