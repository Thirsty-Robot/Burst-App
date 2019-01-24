from flask import Blueprint, request, session, render_template, \
                redirect, url_for, g, jsonify, flash, Markup
from engine.db import DataBaseOps
from engine.RiotEngine import Engine
from project import app

user_routes = Blueprint('user', __name__)
db_ops = DataBaseOps(app)

@user_routes.route('/home')
def home():
    if ('user' in session):
        return render_template('home.html')

    else:
        return redirect(url_for('login'))

@user_routes.route('/teams')
def teams():
    if ('user' in session):
        request_teams = db_ops.get_teams(session['user'])

        return render_template('teams.html', teams=request_teams)

    else:
        return redirect(url_for('login'))

@user_routes.route('/todo')
def todo():
    if 'user' in session:
        return render_template('todo.html')

    else:
        return redirect(url_for('login'))

@user_routes.route('/create_team', methods=['GET', 'POST'])
def create_team():
    if ('user' in session):
        if request.method == 'GET':
            return render_template('create_team.html')

        if (request.method == 'POST'):
            name = request.form['team-name']
            logo = request.files['team-logo']
            position = request.form['Position']
            filename = 'filename'

            team = db_ops.create_team(filename, name, session['user'], position)

            if (team != None):
                return redirect(url_for('team', team_id=team))

    else:
        return redirect(url_for('login'))

@user_routes.route('/team/<team_id>', methods=['GET', 'POST'])
def team(team_id):
    if (request.method == 'GET'):
        team = db_ops.get_team(team_id)

        return render_template('team.html', team=team)
    
    if (request.method == 'POST'):
        if 'user' in session:
            position_to_apply = request.form['Position']

            db_ops.add_team_mate(team_id, session['user'], position_to_apply)

@user_routes.route('/profile')
def profile():
    if ('user' in session):
        account = db_ops.get_session_info(session['user'])
        request_teams = db_ops.get_teams(session['user'])

        return render_template('profile.html', account=account, teams=request_teams)
    
    else:
        return redirect(url_for('login'))

@user_routes.route('/user/<username>')
def user(username):
    account = db_ops.get_user_info(username)
    teams = db_ops.get_teams(account['UserId'])

    return render_template('user.html', account=account, teams=teams)

@user_routes.route('/create_post', methods=['GET', 'POST'])
def create_post():
    if (request.method == 'GET'):
        if 'user' in session:
            return render_template('create_post.html')

        else:
            return redirect(url_for('login'))
    
    if (request.method == 'POST'):
        post_title = request.form['title']
        tags = request.form['tags']
        content = request.form['content']

        db_ops.create_blog_entry(session['user'], post_title, tags, content)