from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from darribny import db
from werkzeug.security import generate_password_hash,check_password_hash
from darribny.models import Trainee, Reservation
from darribny.users.forms import RegistrationForm, LoginForm, UpdateUserForm
from darribny.users.picture_handler import add_profile_pic


users = Blueprint('users', __name__)

@users.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        trainee = Trainee(email=form.email.data,
                    username=form.username.data,
                    first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    city=form.city.data,
                    birthdate=form.birthdate.data,
                    mobile=form.mobile.data,
                    gender=form.gender.data,
                    password=form.password.data)

        db.session.add(trainee)
        db.session.commit()
        flash('Thanks for registering! Now you can login!', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', form=form)

@users.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()

    if form.validate_on_submit():
        # Grab the user from our User Models table
        trainee = Trainee.query.filter_by(email=form.email.data).first()
        # Check that the user was supplied and the password is right
        # The verify_password method comes from the User object
        # https://stackoverflow.com/questions/2209755/python-operation-vs-is-not
        if trainee:
            if trainee.check_password(form.password.data) and trainee is not None:
                #Log in the user
                login_user(trainee)
                flash('Logged in successfully.', 'success')

                # If a user was trying to visit a page that requires a login
                # flask saves that URL as 'next'.
                next = request.args.get('next')

                # So let's now check if that next exists, otherwise we'll go to
                # the welcome page.
                if next == None or not next[0]=='/':
                    next = url_for('users.dashboard')

                return redirect(next)
        flash('Wrong email or password.', 'error')
        
    return render_template('login.html', form=form)

@users.route("/logout")
def logout():
    logout_user()
    flash('Logged out successfully', 'success')
    return redirect(url_for('core.index'))


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():

    form = UpdateUserForm()

    if form.validate_on_submit():
        print(form)
        if form.picture.data:
            username = current_user.username
            pic = add_profile_pic(form.picture.data,username)
            current_user.profile_image = pic

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('User Account Updated', 'success')
        return redirect(url_for('users.account'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    profile_image = url_for('static', filename='profile_pics/' + current_user.profile_image)
    return render_template('account.html', profile_image=profile_image, form=form)

@users.route("/dashboard")
@login_required
def dashboard():
    return render_template('dashboard.html')

@users.route("/<username>")
def user_reservations(username):
    page = request.args.get('page', 1, type=int)
    trainee = Trainee.query.filter_by(username=username).first_or_404()
    reservations = Reservation.query.filter_by(trainee=trainee).order_by(Reservation.date.desc()).paginate(page=page, per_page=5)
    return render_template('trainee_reservations.html', reservations=reservations, trainee=trainee)
