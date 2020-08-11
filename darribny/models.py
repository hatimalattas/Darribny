from darribny import db,login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return Trainee.query.get(user_id)

class Trainee(db.Model,UserMixin):

    __tablename__ = 'trainees'

    id = db.Column(db.Integer, primary_key=True)
    profile_image = db.Column(db.String(20),nullable=False,default='default_profile.png')
    email = db.Column(db.String(64),unique=True,index=True)
    username = db.Column(db.String(64),unique=True,index=True)
    password_hash = db.Column(db.String(128))
    birthdate = db.Column(db.DateTime, nullable=False)
    first_name = db.Column(db.String(64),nullable=False)
    last_name = db.Column(db.String(64),nullable=False)
    gender = db.Column(db.String(64),nullable=False)
    city = db.Column(db.String(64),nullable=False)
    mobile = db.Column(db.Integer,unique=True,nullable=False)

    reservations = db.relationship('Reservation',backref='trainee',lazy=True)

    def __init__(self,email,username,password,birthdate, first_name, last_name, gender, city, mobile):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.birthdate = birthdate
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.city = city
        self.mobile = mobile

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return f"Trainee Username: {self.username}"

# class Trainer(db.Model,UserMixin):

#     __tablename__ = 'trainers'

#     id = db.Column(db.Integer, primary_key=True)
#     profile_image = db.Column(db.String(20),nullable=False,default='default_profile.png')
#     email = db.Column(db.String(64),unique=True,index=True)
#     username = db.Column(db.String(64),unique=True,index=True)
#     password_hash = db.Column(db.String(128))
#     birthday = db.Column(db.DateTime, nullable=False)
#     first_name = db.Column(db.String(64),nullable=False)
#     last_name = db.Column(db.String(64),nullable=False)
#     gender = db.Column(db.String(64),nullable=False)
#     city = db.Column(db.String(64),nullable=False)
#     mobile = db.Column(db.Integer,unique=True,nullable=False)
#     price = db.Column(db.Integer,nullable=False)
#     description = db.Column(db.Text)

#     reservations = db.relationship('Reservation',backref='trainers',lazy=True)

#     def __init__(self,email,username,password,birthday, first_name, last_name, gender, city, mobile, price):
#         self.email = email
#         self.username = username
#         self.password_hash = generate_password_hash(password)
#         self.birthday = birthday
#         self.first_name = first_name
#         self.last_name = last_name
#         self.gender = gender
#         self.city = city
#         self.mobile = mobile
#         self.price = price

#     def check_password(self,password):
#         return check_password_hash(self.password_hash,password)

#     def __repr__(self):
#         return f"Trainer Username: {self.username}"

class Reservation(db.Model):

    __tablename__ = 'reservations'

    trainees = db.relationship(Trainee)
    # trainers = db.relationship(Trainer)

    id = db.Column(db.Integer, primary_key=True)
    trainee_id = db.Column(db.Integer,db.ForeignKey('trainees.id'),nullable=False)
    # trainer_id = db.Column(db.Integer,db.ForeignKey('trainers.id'),nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    location = db.Column(db.String(64), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)

    def __init__(self,date,location,start_time,trainee_id):
        self.date = date
        self.location = location
        self.start_time = start_time
        self.trainee_id = trainee_id

    def __repr__(self):
        return f"Reservation ID {self.id} -- Date: {self.date} -- Location: {self.location}"

