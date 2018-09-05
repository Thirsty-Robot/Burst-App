# Flask modules
from flask import Flask
from flask import render_template
from flask import request
from flask import flash
from flask import Markup
from flask import url_for
from flask import redirect
from flask import session
from flask import g
from flask_wtf.csrf import CSRFProtect
import os

# Request modules
from engine.RiotEngine import Engine
from engine.auth import Auth

# Create app
app = Flask(__name__)
app.secret_key = os.urandom(24)

from routes import *

# Main loop
if (__name__ == '__main__'):
    app.run(debug=1)
