import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

app = Flask(__name__ )

app.config['SECRET_KEY'] = 'mysecret'
app.config['RECAPTCHA_PUBLIC_KEY'] = '6LcYjb8ZAAAAAGqHGJsgR4CoJ0qTzmluliAKCl40'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LcYjb8ZAAAAAKdzdYdg8zHt-VRYcOgIPG1ozHGL'


##########################
#### DATABASE SETUP ######
##########################
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)


Bootstrap(app)
###########################
#### LOGIN CONFIGS #######
#########################

login_manager = LoginManager()

# We can now pass in our app to the login manager
login_manager.init_app(app)

# Tell users what view to go to when they need to login.
login_manager.login_view = "users.login"


##################################################


from darribny.core.views import core
from darribny.users.views import users
from darribny.reservations.views import reservations
from darribny.error_pages.handlers import error_pages

app.register_blueprint(core)
app.register_blueprint(users)
app.register_blueprint(reservations)
app.register_blueprint(error_pages)
