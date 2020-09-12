from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from darribny import db
from werkzeug.security import generate_password_hash, check_password_hash
from darribny.models import User, Reservation
from darribny.users.forms import RegistrationForm, LoginForm, UpdateUserForm
from darribny.users.picture_handler import add_profile_pic


users = Blueprint('users', __name__)


@users.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        trainee = User(email=form.email.data,
                          username=form.username.data,
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

        if form.role.data == 'trainee':
            flash('Thanks for registering! Now you can login as trainee!', 'success')
            return redirect(url_for('users.login'))
        elif form.role.data == 'trainer':
            flash('Thanks for registering! Now you can login as trainer!', 'success')
            return redirect(url_for('users.login_trainer'))

    return render_template('register.html', form=form)


@users.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()

    if form.validate_on_submit():
        # Grab the user from our User Models table
        trainee = User.query.filter_by(
            email=form.email.data, role='trainee').first()
        # Check that the user was supplied and the password is right
        # The verify_password method comes from the User object
        # https://stackoverflow.com/questions/2209755/python-operation-vs-is-not
        if trainee:
            if trainee.check_password(form.password.data) and trainee is not None:
                # Log in the user
                login_user(trainee)
                flash('Logged in successfully as a trainee.', 'success')

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


@users.route('/login-trainer', methods=['GET', 'POST'])
def login_trainer():

    form = LoginForm()

    if form.validate_on_submit():
        # Grab the user from our User Models table
        trainee = User.query.filter_by(
            email=form.email.data, role='trainer').first()
        # Check that the user was supplied and the password is right
        # The verify_password method comes from the User object
        # https://stackoverflow.com/questions/2209755/python-operation-vs-is-not
        if trainee:
            if trainee.check_password(form.password.data) and trainee is not None:
                # Log in the user
                login_user(trainee)
                flash('Logged in successfully as a trainer.', 'success')

                # If a user was trying to visit a page that requires a login
                # flask saves that URL as 'next'.
                next = request.args.get('next')

                # So let's now check if that next exists, otherwise we'll go to
                # the welcome page.
                if next == None or not next[0] == '/':
                    next = url_for('users.dashboard_trainer')

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
            username = current_user.username
            pic = add_profile_pic(form.picture.data, username)
            current_user.profile_image = pic

        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.mobile = form.mobile.data
        current_user.gender = form.gender.data
        current_user.city = form.city.data
        current_user.birthdate = form.birthdate.data

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

    profile_image = url_for(
        'static', filename='profile_pics/' + current_user.profile_image)
    return render_template('account.html', profile_image=profile_image, form=form)

@users.route("/dashboard")
@login_required
def dashboard():
    if current_user.role == 'trainee':

        trainers = User.query.filter_by(role='trainer').all()
        reservations = Reservation.query.filter_by(user_id=current_user.id)
        
        # result = User.query.join(Reservation).filter(Reservation.trainee_id == current_user)
        # for row in result:
        #     for res in row.reservations:
        #         print (row.id, row.first_name, res.trainer_id, res.location)

        # result = Reservation.query.join(User).filter(Reservation.trainer_id == User.id)
        # print(result)
        # for row in result:
        #     for res in row.reservations:
        #         print (row.id, row.first_name, res.trainer_id, res.location)

        # trainee = User.query.filter_by(id=current_user.id).first()
        # trainee_reservations = trainee.reservations
        # reservation_trainer_id = trainee_reservations[0].trainer_id
        # print(reservation_trainer_id)

        # for reservation in trainee_reservations:
        #     print(reservation.location)

        # reservation_trainer = User.query.filter_by(id=trainee_reservations.reservations[0].trainer_id).first()
        # print(reservation_trainer.role)

        # reservation = Reservation.query.filter_by(trainer_id=2).first()
        # print(reservation.trainee.role)

        # print(trainee.reservations)

        # reservations = Reservation.query.filter_by(trainee_id=current_user.id).all()
        # print(reservations)
    
        return render_template('dashboard.html', trainers=trainers, reservations=reservations)

    else:
        return 'Unauthorized'



# int: makes sure that the trainer_id gets passed as in integer
# instead of a string so we can look it up later.
@users.route('/dashboard/<int:trainer_id>')
@login_required
def trainer(trainer_id):
    # grab the requested blog post by id number or return 404
    trainer = User.query.filter_by(role='trainer', id=trainer_id).first()
    return render_template('trainer-profile.html', first_name=trainer.first_name, last_name=trainer.last_name, profile_image=trainer.profile_image, username=trainer.username, birthdate=trainer.birthdate, gender=trainer.gender, city=trainer.city, mobile=trainer.mobile, id=trainer.id)


################################
######## Trainers Views ########
################################
@users.route("/account-trainer", methods=['GET', 'POST'])
@login_required
def account_trainer():

    if current_user.role == 'trainer':
        form = UpdateUserForm()

        if form.validate_on_submit():
            if form.picture.data:
                username = current_user.username
                pic = add_profile_pic(form.picture.data, username)
                current_user.profile_image = pic

            current_user.first_name = form.first_name.data
            current_user.last_name = form.last_name.data
            current_user.mobile = form.mobile.data
            current_user.gender = form.gender.data
            current_user.city = form.city.data
            current_user.birthdate = form.birthdate.data

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

        profile_image = url_for(
            'static', filename='profile_pics/' + current_user.profile_image)
        return render_template('account-trainer.html', profile_image=profile_image, form=form)
    else:
        return 'Unauthorized'

@users.route("/dashboard-trainer")
@login_required
def dashboard_trainer():
    if current_user.role == 'trainer':
        return render_template('dashboard-trainer.html')
    else:
        return 'Unauthorized'