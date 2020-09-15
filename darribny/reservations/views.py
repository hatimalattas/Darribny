from flask import render_template,url_for,flash, redirect,request,Blueprint, abort
from flask_login import current_user,login_required
from darribny import db
from darribny.models import Reservation, User
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

    return render_template('create_reservation.html',form=form)
    
@reservations.route('/reservation/<int:reservation_id>')
@login_required
def reservation(reservation_id):
    reservation = Reservation.query.filter_by(id=reservation_id).first()
    trainer_id = reservation.trainer_id
    trainer = User.query.filter_by(id=trainer_id).first()

    return render_template('reservation.html', reservation=reservation, trainer=trainer)

@reservations.route("/<int:reservation_id>/delete", methods=['POST'])
@login_required
def delete_reservation(reservation_id):
    reservation = Reservation.query.get_or_404(reservation_id)
    # if reservation.trainee != current_user:
    #     abort(403)
    db.session.delete(reservation)
    db.session.commit()
    flash('Reservation has been cancelled')
    return redirect(url_for('users.dashboard'))

# @blog_posts.route("/<int:blog_post_id>/delete", methods=['POST'])
# @login_required
# def delete_post(blog_post_id):
#     blog_post = BlogPost.query.get_or_404(blog_post_id)
#     if blog_post.author != current_user:
#         abort(403)
#     db.session.delete(blog_post)
#     db.session.commit()
#     flash('Post has been deleted')
#     return redirect(url_for('core.index'))

