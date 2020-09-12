from flask import render_template,url_for,flash, redirect,request,Blueprint
from flask_login import current_user,login_required
from darribny import db
from darribny.models import Reservation
from darribny.reservations.forms import ReservationForm

reservations = Blueprint('reservations',__name__)

@reservations.route('/<int:trainer_id>/create',methods=['GET','POST'])
@login_required
def create(trainer_id):
    form = ReservationForm()
    
    if form.validate_on_submit():

        reservation = Reservation(start_time=form.start_time.data,
                             location=form.location.data,
                             user_id=current_user.id,
                             trainer_id=trainer_id
                             )
        db.session.add(reservation)
        db.session.commit()
        flash('Reservation Confirmed', 'success')
        return redirect(url_for('users.dashboard'))

    return render_template('create-reservation.html',form=form)
