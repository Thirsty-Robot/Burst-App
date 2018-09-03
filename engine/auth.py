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
import bcrypt
import uuid

class Auth():
    def __init__(self, app):
        app.config['MONGO_DBNAME'] = 'gooleague_try'
        app.config['MONGO_URI'] = 'mongodb://admon:miniaxel1@ds141902.mlab.com:41902/gooleague_try'

        self.mongo = PyMongo(app)
        self.users_db = self.mongo.db.user

    def signup(self, name, summoner, region, username, email, password, password_check):
        if (password == password_check):
            hashed_password = bcrypt.hashpw(password, bcrypt.gensalt(14))
            user_id = uuid.uuid4()

            self.users_db.insert({
                'name' : name,
                'id' : user_id,
                'summoner_username' : summoner,
                'region' : region,
                'username' : username,
                'password' : hashed_password
            })

            return True

        else:
            return False
    
    def login(self, username, password):
        pass