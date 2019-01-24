from flask import Blueprint, request, session, render_template, \
                redirect, url_for, g, jsonify, flash, Markup
from engine.db import DataBaseOps
from engine.RiotEngine import Engine
from project import app

post_routes = Blueprint('post', __name__)
db_ops = DataBaseOps(app)
engine = Engine()

@post_routes.route('/', methods=['POST'])
def index():
    # Form formatting
    summoner = request.form['summoner-name']
    region = request.form['region']

    # Makes request
    user_query = engine.search(summoner, region)

    # If error is a 404
    if user_query['Error']:
        flash(user_query['Error'])
        return redirect(url_for('login'))
    
    else:
        return redirect(url_for('summoner', region=region, summoner=summoner))

@post_routes.route('/signup', methods=['POST'])
def signup():
    # Get form and parse it
    name = request.form['name']
    username_league = request.form['summoner']
    region = request.form['region']
    email = request.form['email']
    username = request.form['username']
    password = request.form['password']
    password_check = request.form['password_confirm']

    # Upload to database
    reg_user = db_ops.signup(name, username_league, region, username, email, password, password_check)

    # Error checking
    if (reg_user['err']):
        flash(reg_user['err'])
        return redirect(url_for('main.signup'))
    
    else:
        flash('Account created succesfully, please log in.')
        return redirect(url_for('main.login'))

@post_routes.route('/login', methods=['POST'])
def login():
    #Get form and parser form
    email = request.form['email']
    password = request.form['password']

    # Make petition
    log_user = db_ops.login(email, password)

    # Error checking
    if log_user['err']:
        flash(log_user['err'])
        return redirect(url_for('login'))

    else:
        session['user'] = log_user['user_token']
        return redirect(url_for('user.home'))
