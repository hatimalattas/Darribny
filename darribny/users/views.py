from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from darribny import db
from werkzeug.security import generate_password_hash, check_password_hash
from darribny.models import User, Reservation
from darribny.users.forms import RegistrationForm, LoginForm, UpdateUserForm, FilterForm
from darribny.users.picture_handler import add_profile_pic

users = Blueprint('users', __name__)


@users.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        trainee = User(email=form.email.data,
                       first_name=form.first_name.data,
                       last_name=form.last_name.data,
                       city=form.city.data,
                       birthdate=form.birthdate.data,
                       mobile=form.mobile.data,
                       gender=form.gender.data,
                       role=form.role.data,
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
        user = User.query.filter_by(
            email=form.email.data).first()
        # Check that the user was supplied and the password is right
        # The verify_password method comes from the User object
        # https://stackoverflow.com/questions/2209755/python-operation-vs-is-not
        if user:
            if user.check_password(form.password.data) and user is not None:
                # Log in the user
                login_user(user)
                flash('Logged in successfully', 'success')

                # If a user was trying to visit a page that requires a login
                # flask saves that URL as 'next'.
                next = request.args.get('next')

                # So let's now check if that next exists, otherwise we'll go to
                # the welcome page.
                if next == None or not next[0] == '/':
                    next = url_for('users.dashboard')

                return redirect(next)
        flash('Wrong email or password.', 'error')

    return render_template('login.html', form=form)


@users.route("/logout")
def logout():
    logout_user()
    flash('Logged out successfully', 'success')
    return redirect(url_for('core.index'))


################################
######## Users Views ########
################################
@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateUserForm()

    if form.validate_on_submit():
        if form.picture.data:
            email = current_user.email
            pic = add_profile_pic(form.picture.data, email)
            current_user.profile_image = pic

        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.mobile = form.mobile.data
        current_user.gender = form.gender.data
        current_user.city = form.city.data
        current_user.birthdate = form.birthdate.data
        current_user.bio = form.bio.data
        current_user.price = form.price.data
        current_user.sports = form.sports.data

        db.session.commit()
        flash('User Account Updated', 'success')
        return redirect(url_for('users.account'))

    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.mobile.data = current_user.mobile
        form.city.data = current_user.city
        form.gender.data = current_user.gender
        form.birthdate.data = current_user.birthdate
        form.bio.data = current_user.bio
        form.price.data = current_user.price
        form.sports.data = current_user.sports

    profile_image = url_for(
        'static', filename='profile_pics/' + current_user.profile_image)
    return render_template('account.html', profile_image=profile_image, form=form)


@users.route("/dashboard", methods=['GET', 'POST'])
@login_required
def dashboard():
    form = FilterForm()
    if current_user.role == 'trainee':
        trainers = User.query.filter_by(role='trainer').all()

        path = "static/profile_pics/"
        pics_url = ['9@9.com.jpeg', 'default_profile.png', '1@1.com.jpg']
        full_pics_url = []
        for url in pics_url:
            full_path = path + url
            full_pics_url.append(full_path)

        data = []
        reservations = Reservation.query.filter_by(user_id=current_user.id)
        for reservation in reservations:
            trainer_id = reservation.trainer_id
            trainer = User.query.filter_by(id=trainer_id).first()
            data.append({
                "id": reservation.id,
                "trainer_first_name": trainer.first_name,
                "trainer_last_name": trainer.last_name,
                "location": reservation.location,
                "start_time": reservation.start_time,
                "status": reservation.status
            })

        if request.method == 'POST':

            if form.validate_on_submit():

                if request.form.get('city') and request.form.get('sport') == '':
                    city = request.form.get('city')
                    trainers = User.query.filter(User.role == 'trainer', User.city == city).all()

                if request.form.get('sport') and request.form.get('city') == '':
                    sport = request.form.get('sport')
                    trainers = User.query.filter(User.role == 'trainer', User.sports.contains(f"{{{sport}}}")).all()

                if request.form.get('city') and request.form.get('sport'):
                    city = request.form.get('city')
                    sport = request.form.get('sport')
                    trainers = User.query.filter(User.role == 'trainer', User.city == city,
                                                 User.sports.contains(f"{{{sport}}}")).all()

        elif request.method == 'GET':
            form.city.data = request.form.get('city')
            form.sport.data = request.form.get('sport')

        return render_template('dashboard.html', trainers=trainers, reservations=data, form=form, path=path,
                               full_pics_url=full_pics_url)

    elif current_user.role == 'trainer':
        reservations = Reservation.query.filter_by(trainer_id=current_user.id)
        return render_template('dashboard.html', reservations=reservations, form=form)


# int: makes sure that the user_id gets passed as in integer
# instead of a string so we can look it up later.
@users.route('/<int:user_id>')
@login_required
def user(user_id):
    # grab the requested user by id number
    user = User.query.filter_by(id=user_id).first()
    return render_template('profile.html', user=user)
