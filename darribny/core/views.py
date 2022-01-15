from flask import render_template, request, Blueprint
from datetime import datetime

core = Blueprint('core',__name__)

@core.route('/')
def index():
    return render_template('index.html')

@core.route('/about')
def info():
    return render_template('about.html')
