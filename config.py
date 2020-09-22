import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
# DEBUG = True

# Connect to the database
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres@localhost:5432/darribny'
# SQLALCHEMY_DATABASE_URI = 'postgres://bsqpwmqbhamiiz:b008118b47273a2e4e90b34bcebd50d60e8540943efdac841316e2058b90a19f@ec2-23-23-242-234.compute-1.amazonaws.com:5432/d17o8q0t643gbo'
SQLALCHEMY_TRACK_MODIFICATIONS = False
