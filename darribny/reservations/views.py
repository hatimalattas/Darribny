from flask import render_template,url_for,flash, redirect,request,Blueprint
from flask_login import current_user,login_required
from darribny import db
from darribny.models import BlogPost
from darribny.reservations.forms import ReservationForm

reservations = Blueprint('reservations',__name__)

@reservations.route('/<int:trainer_id>/create',methods=['GET','POST'])
@login_required
def create_reservation():
    form = ReservationForm()

    if form.validate_on_submit():

        blog_post = BlogPost(start_time=form.title.data,
                             location=form.text.data,
                             trainee_id=current_user.id
                             )
        db.session.add(blog_post)
        db.session.commit()
        flash("Reservation Confirmed")
        return redirect(url_for('dashboard.index'))

    return render_template('create-reservation.html',form=form)
