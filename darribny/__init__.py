from flask import Flask

app = Flask(__name__ )

from darribny.core.views import core
app.register_blueprint(core)