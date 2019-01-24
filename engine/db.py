"""
Coded by: Thirsty-Robot (Axel C. Uribe);
Email: Thirsty-Robot@protonmail.com;
License : MIT;
"""

from flask_pymongo import PyMongo
from flask import session
from .RiotEngine import Engine
import bcrypt
import uuid

engine = Engine()
err_register = {}
err_login = {}

class DataBaseOps():
    def __init__(self, app):
        app.config['MONGO_DBNAME'] = 'gooleague_try'
        app.config['MONGO_URI'] = 'mongodb://admon:miniaxel1@ds141902.mlab.com:41902/gooleague_try'

        # Databases
        self.mongo = PyMongo(app)
        self.users_db = self.mongo.db.user
        self.tasks_db = self.mongo.db.tasks
        self.teams_db = self.mongo.db.teams
        self.blogs_db = self.mongo.db.blog

    def signup(self, name, summoner_username, region, username, email, password, password_check):
        # User verifications
        summoner_check = engine.confirm_summoner(summoner_username, region)
        existing_user = self.users_db.find_one({'username' : username})
        existing_email = self.users_db.find_one({'email' : email})
        user_id = str(uuid.uuid4())
        user_id_search = self.users_db.find_one({'user_id' : user_id})

        # Create differen UIDS
        while user_id_search!=None:
            user_id = str(uuid.uuid4())

        # Verification
        if (existing_user == None and existing_email == None \
             and summoner_check == True and password == password_check):
            # Encoded password and, user id
            pwd = password.encode('utf-8')
            hashed_password = bcrypt.hashpw(pwd, bcrypt.gensalt())
            summoner = engine.search(summoner_username, region)

            # Insert to Database
            self.users_db.insert({
                'Name' : name,
                'UserId' : user_id,
                'Icon': summoner['Icon'],
                'Email' : email,
                'SummonerUsername' : summoner_username,
                'Region' : region,
                'Username' : username,
                'Password' : hashed_password,
                'Followers': [],
                'Roles' : []
            })

            err_register['err'] = 'null'
            return err_register

        # Error handling
        else:
            if existing_email is not None:
                err_register['err'] = 'email'
                return err_register
            elif existing_user is not None:
                err_register['err'] = 'user'
                return err_register
            elif summoner_check == False:
                err_register['err'] = 'summoner'
                return err_register 
            elif password != password_check:
                err_register['err'] = 'password'
                return err_register

    def login(self, email, password):
        # Search for account according to the email
        account = self.users_db.find_one({'Email' : email})

        # Verify account existance
        if (account is not None):
            formated_password = password.encode('utf-8')
            hashed_pass = account['Password']

            # Password dehashing
            if bcrypt.checkpw(formated_password, hashed_pass):
                err_login_resp = {
                    'user_token': account['UserId'],
                    'err' : 0
                }
                return err_login_resp

            # Passwords don't match
            else:
                err_login['err'] = 'Ups, incorrect password. Please try again.'
                return err_login

        # Account not found
        else:
            err_login['err'] = 'Are you sure you have an account?'
            return err_login
    
    def get_session_info(self, user_token):
        # Found account according to cookie
        account = self.users_db.find_one({'UserId' : user_token})
        account_dict = {
            'Icon' : account['Icon'],
            'Username' : account['Username'],
            'Summoner' : account['SummonerUsername'],
            'Roles' : account['Roles']
        }

        return account_dict

    def get_teams(self, user_token):
        teams = self.teams_db.find({'Creator' : user_token})

        if teams is not None:
            return teams

        else:
            return 'Nothing to show'

    def create_team(self, logo, team_name, creator, position):
        team_id = str(uuid.uuid4())

        self.teams_db.insert({
            'TeamLogo' : logo,
            'TeamId' : team_id,
            'TeamName' : team_name,
            'Creator' : creator,
            'Top' : '',
            'Jungle' : '',
            'Mid' : '',
            'Adc' : '',
            'Supp' : '',
            'TeamPoints' : 10
        })

        team_position = self.teams_db.find_one({'TeamId' : team_id})
        team_position[position] = team_position['Creator']
        self.teams_db.save(team_position)

        return team_id

    def get_team(self, team_id):
        team = self.teams_db.find_one({'TeamId' : team_id})
        team_response = {
            'TeamName' : str(team['TeamName']),
            'TeamAdmin' : str(team['Creator']),
            'TeamLogo' : str(team['TeamLogo']),
            'TeamPoint' : team['TeamPoints']
        }

        roles = []

        for key, value in team.items():
            if value == '':
                roles.append(key)

        team_response['Positions'] = roles

        return team_response

    def add_team_mate(self, team_id, user_id, position):
        team = self.teams_db.find_one({'TeamId' : team_id})
        team[position] = user_id
        self.teams_db.save(team)

        return True

    def create_blog_entry(self, user_id, title, tags, content, **kwargs):
        post_id = str(uuid.uuid4())
        post_username = self.users_db.find_one({'UserId' : user_id})
        
        try:
            self.blogs_db.insert({
                'UserId' : user_id,
                'Username' : post_username['Username'],
                'postId' : post_id,
                'Title' : title,
                'Tags' : tags
            })
        
        except self.blogs_db.errors.OperationFailure as e:
            return e

    def get_blog_entries(self, user_id):
        user_id = self.users_db.find_one({'UserId' : user_id})

        for user in user_id['Following']:
            try:
                articles = self.blogs_db.find({'Username' : user})

                return articles
            
            except self.blogs_db.errors.OperationFailure as e:
                return e

    def get_user_info(self, user_id):
        user = self.users_db.find_one({'Username': user_id})

        return user

    def timeline(self, user_id):
        user = self.users_db.find_one({'UserId': user_id})
        following = user['Following']

        for user in following:
            timeline = self.blogs_db.find({'Username': user})

        return timeline