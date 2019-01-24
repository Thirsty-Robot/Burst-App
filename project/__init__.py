from flask import Flask
from flask import Blueprint, request, session, render_template, \
                redirect, url_for, g, jsonify, flash, Markup
from flask_pymongo import PyMongo
import os

# Create app
app = Flask(__name__, static_url_path='/static')
app.secret_key = os.urandom(24)

from .blueprints.main import main_routes
from .blueprints.post import post_routes
from .blueprints.user import user_routes

# Blueprints
app.register_blueprint(main_routes)
app.register_blueprint(post_routes)
app.register_blueprint(user_routes)
