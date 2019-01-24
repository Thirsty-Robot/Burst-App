from flask import Blueprint, request, session, render_template, \
                redirect, url_for, g, jsonify, flash, Markup
from engine.db import DataBaseOps
from engine.RiotEngine import Engine

main_routes = Blueprint('main', __name__)
engine = Engine()

@main_routes.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@main_routes.route('/summoner/<region>/<summoner>', methods=['GET'])
def summoner(region, summoner):
    summoner_query = engine.search(summoner, region)

    return render_template('summoner.html', summoner=summoner_query)

@main_routes.route('/signup', methods=['GET'])
def signup():
    # Get Action
    if request.method == 'GET':
        return render_template('signup.html')

@main_routes.route('/login', methods=['GET'])
def login():
    # Get Action
    if request.method == 'GET':
        if 'user' in session:
            return redirect(url_for('user.home'))

        else:
            return render_template('login.html')
