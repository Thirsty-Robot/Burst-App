####### DATABASE SCHEMAS ######

    ### USER COLLECTION ###
        ## USER_ID : INT
        ## NAME : STRING
        ## SUMMONER_USERNAME : STRING
        ## REGION : STRING
        ## USERNAME : STRING
        ## PASSWORD (HASHED) : STRING
    
    ### TASKS COLLECTION ###
        ## USER_ID : INT
        ## TASK_ID : INT
        ## TASK_NAME : STRING
        ## PUBLIC : BOOL
        ## TASK : STRING
        ## ACCOMPLISHED : BOOL

###############################

from flask_pymongo import PyMongo
from flask import session
from .RiotEngine import Engine
import bcrypt
import uuid

engine = Engine()
err_register = {}
err_login = {}

class Auth():
    def __init__(self, app):
        app.config['MONGO_DBNAME'] = 'gooleague_try'
        app.config['MONGO_URI'] = 'mongodb://admon:miniaxel1@ds141902.mlab.com:41902/gooleague_try'

        self.mongo = PyMongo(app)
        self.users_db = self.mongo.db.user
        self.tasks = self.mongo.db.tasks

    def signup(self, name, summoner, region, username, email, password, password_check):
        summoner = engine.confirm_summoner(summoner, region)
        existing_user = self.users_db.find_one({'username' : username})
        existing_email = self.users_db.find_one({'email' : email})

        if (existing_user == None and existing_email == None and summoner == True and password == password_check):
            # Encoded password and, user id
            pwd = password.encode('utf-8')
            hashed_password = bcrypt.hashpw(pwd, bcrypt.gensalt())
            user_id = uuid.uuid4()

            # Insert to Database
            self.users_db.insert({
                'name' : name,
                'id' : user_id,
                'email' : email,
                'summoner_username' : summoner,
                'region' : region,
                'username' : username,
                'password' : hashed_password
            })

            err_register['err'] = 'null'
            return err_register

        else:
            if existing_email is not None:
                err_register['err'] = 'email'
                return err_register
            elif existing_user is not None:
                err_register['err'] = 'user'
                return err_register
            elif summoner == False:
                err_register['err'] = 'summoner'
                return err_register 
            elif password != password_check:
                err_register['err'] = 'password'
                return err_register

    def login(self, email, password):
        account = self.users_db.find_one({'email' : email})

        if (account is not None):
            formated_password = password.encode('utf-8')
            hashed_pass = account['password']

            if (bcrypt.checkpw(formated_password, hashed_pass)):
                err_login_resp = {'user_id': str(account['id']), 
                                'err': 'none'
                                }

                return err_login_resp
            else:
                err_login['err'] = 'password'
                return err_login
        else:
            err_login['err'] = '404'
            return err_login