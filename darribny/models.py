from darribny import db,login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from sqlalchemy.dialects import postgresql as pg


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model,UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    profile_image = db.Column(db.String(128),nullable=False,default='default_profile.png')
    email = db.Column(db.String(64),unique=True,index=True)
    password_hash = db.Column(db.String(128))
    birthdate = db.Column(db.DateTime, nullable=False)
    first_name = db.Column(db.String(64),nullable=False)
    last_name = db.Column(db.String(64),nullable=False)
    gender = db.Column(db.String(64),nullable=False)
    city = db.Column(db.String(64),nullable=False)
    mobile = db.Column(db.String(10),unique=True,nullable=False)
    role = db.Column(db.String(64), nullable=False, default='trainee')
    price = db.Column(db.Integer,nullable=False, default=25)
    sports = db.Column(pg.ARRAY(db.String(120)))
    bio = db.Column(db.Text, default='Hi there!')

    reservations = db.relationship('Reservation',backref='trainee',lazy=True)
    favorites = db.relationship('Favorite',backref='trainee',lazy=True)

    def __init__(self,email,password,birthdate, first_name, last_name, gender, city, mobile, role):
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.birthdate = birthdate
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.city = city
        self.mobile = mobile
        self.role = role

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)


class Favorite(db.Model):

    __tablename__ = 'favorites'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    status = db.Column(db.Boolean(), nullable=False, default=False)

class Reservation(db.Model):

    __tablename__ = 'reservations'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    trainer_id = db.Column(db.Integer,nullable=False)
    location = db.Column(db.String(64), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False, unique=True)
    end_time = db.Column(db.DateTime, nullable=False, unique=True)
    status = db.Column(db.String(64), nullable=False, default='pending')

    reviews = db.relationship('Review',backref='reservations',lazy=True)

    def __init__(self,location,start_time,user_id,trainer_id, end_time, status):
        self.user_id = user_id
        self.trainer_id = trainer_id
        self.location = location
        self.start_time = start_time
        self.end_time = end_time
        self.status = status

class Review(db.Model):

    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    reservation_id = db.Column(db.Integer,db.ForeignKey('reservations.id'),nullable=False)
    rating = db.Column(db.Integer,nullable=False)
    comment = db.Column(db.Text)

    def __init__(self,reservation_id,rating,comment):
        self.reservation_id = reservation_id
        self.rating = rating
        self.comment = comment

