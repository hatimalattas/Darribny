from flask import render_template, url_for, flash, redirect, Blueprint, abort, request
from flask_login import current_user, login_required
from darribny import db
from darribny.models import Reservation, User
from darribny.reviews.forms import ReveiwForm
from datetime import datetime, timedelta

reservations = Blueprint('reservations', __name__)


@reservations.route('/<int:trainer_id>/create', methods=['GET', 'POST'])
@login_required
def create(trainer_id):
    current_date = datetime.now().strftime("%Y-%m-%d")
    trainer = User.query.filter_by(id=trainer_id).first()
    if request.method == "POST":
        dt = request.form["dtp_input1"]
        try:
            dt = datetime.strptime(dt, "%d %B %Y %I:%M %p")
            hours = 1
            hours_added = timedelta(hours=hours)
            reservation = Reservation(start_time=dt,
                                      end_time=dt + hours_added,
                                      location=trainer.city,
                                      user_id=current_user.id,
                                      trainer_id=trainer_id,
                                      status='pending'
                                      )
            db.session.add(reservation)
            db.session.commit()
            flash('Reservation Request has been sent to the trainer, please wait for his/her response', 'success')
            return redirect(url_for('users.dashboard'))

        except ValueError:
            flash("Please choose a date and time", "error")

    return render_template('create_reservation.html', trainer=trainer, current_date=current_date)


@reservations.route('/reservation/<int:reservation_id>', methods=['GET', 'POST'])
@login_required
def reservation(reservation_id):
    form = ReveiwForm()

    reservation = Reservation.query.filter_by(id=reservation_id).first()
    trainer_id = reservation.trainer_id
    trainer = User.query.filter_by(id=trainer_id).first()
    trainee = reservation.trainee

    if request.method == 'POST':  # this block is only entered when the form is submitted

        data = request.form.get('status')
        if data:
            reservation.status = data
            db.session.commit()
            flash('Reservation status has been updated', 'success')
            return redirect(url_for('users.dashboard'))

    return render_template('reservation.html', reservation=reservation, trainer=trainer, trainee=trainee, form=form)


@reservations.route("/<int:reservation_id>/delete", methods=['POST'])
@login_required
def delete_reservation(reservation_id):
    reservation = Reservation.query.get_or_404(reservation_id)
    if reservation.trainee != current_user:
        abort(403)
    db.session.delete(reservation)
    db.session.commit()
    flash('Reservation has been cancelled')
    return redirect(url_for('users.dashboard'))
