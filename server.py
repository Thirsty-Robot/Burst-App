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

# Database and other constructors
engine = Engine()
auth = Auth(app)

# Index route
@app.route('/')
def index():
    return render_template('index.html')

# Summoner route
@app.route('/summoner', methods = ['POST'])
def summoner():
    # Post request method
    if request.method == 'POST':

        # Form formatting
        result = request.form
        username = result['Summoner-name']
        region = result['Region']

        # Makes request
        user_query = engine.search(username, region)
   
        # Error checking
        if (user_query['Error'] == 0):
            return render_template('summoner.html', icon=user_query['Icon'], summoner_name=user_query['Name'], level=user_query['Level'], 
                            tier=user_query['Tier'])
        
        # If error is a 404
        elif (user_query['Error'] == 1):
            flash('Ups, summoner not found not found')
            return redirect(url_for('index'))

        # If error is of type 2 (403, 402, 401)
        elif (user_query['Error'] == 2):
            flash('Ups, something went wrong, please try again later')
            return redirect(url_for('index'))

# Sign-up method
@app.route('/signup', methods=['GET', 'POST'])
def signup():

    # Get Action
    if request.method == 'GET':
        return render_template('signup.html')

    # Post Action
    if request.method == 'POST':

        # Get form and parse it
        user = request.form
        name = user['name']
        username_league = user['summoner']
        region = user['region']
        email = user['email']
        username = user['username']
        password = user['password']
        password_check = user['password_confirm']

        # Upload to database
        reg_user = auth.signup(name, username_league, region, username, email, password, password_check)

        # Error checking
        if (reg_user['err'] == 'null'):
            flash('Account created succesfully, please log in.')
            return redirect(url_for('login'))

        elif (reg_user['err'] == 'password'):
            flash('Are you sure you know how to type your password? Please try again')
            return redirect(url_for('signup'))
        
        elif (reg_user['err'] == 'summoner'):
            flash("The summoner you entered doesn't exists. Please try again.")
            return redirect(url_for('signup'))

        elif (reg_user['err'] == 'user'):
            flash("This username already exists")
            return redirect(url_for('signup'))

        elif (reg_user['err'] == 'email'):
            flash("There is an account registered with this email, please sign up.")
            return redirect(url_for('signup'))

# Log-in method
@app.route('/login', methods=['GET', 'POST'])
def login():

    # Get Action
    if request.method == 'GET':
        if 'user' in session:
            return redirect(url_for('home'))

        else:
            return render_template('login.html')

    # Post Action
    if (request.method == 'POST'):
        #Get form and parser form
        user = request.form
        email = str(user['email'])
        password = str(user['password'])

        # Make petition
        log_user = auth.login(email, password)

        # Error checking
        if (log_user['error'] == 'none'):
            session['user'] = log_user['user_id']

            return redirect(url_for('home'))

        elif (log_user['error'] == 'password'):
            flash("Hey, thats the wrong password")
            return redirect(url_for('login'))

        elif (log_user['error'] == '404'):
            flash("Are you sure you have an account? You can create one whenever you want")
            return redirect(url_for('login'))


@app.route('/home')
def home():
    if ('user' in session):
        return 'Hello '+session['user']

    else:
        return redirect(url_for('login'))

# Main loop
if (__name__ == '__main__'):
    app.run(debug=1)
