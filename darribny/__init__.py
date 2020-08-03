import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__ )

##########################
#### DATABASE SETUP ######
##########################
SQLALCHEMY_DATABASE_URI = 'postgres://hatimalattas@localhost:5432/darribny'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db)

###########################
### LOGIN CONFIGS ########
##########################
login_manager = LoginManager()
login_manager.login_views = 'users.login'


from darribny.core.views import core
from darribny.error_pages.handlers import error_pages

app.register_blueprint(core)
app.register_blueprint(error_pages)
