# Flask modules
from flask import Flask
from flask import render_template
from flask import request
from flask import flash
from flask import Markup
from flask import url_for
from flask import redirect
from flask_wtf.csrf import CSRFProtect

# Request modules
from engine.RiotEngine import Engine
from engine.auth import Auth

# Create app
app = Flask(__name__)

# App configurations
app.secret_key = '$2y$16$nTty7HIXs24iphrgBSZ1CODdtU7PcpdZKj/rjCjqVlNHuY09bDihu'
csrf = CSRFProtect(app)
csrf.init_app(app)

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

        # Gets form
        result = request.form

        # Formats form
        username = result['Summoner-name']
        region = result['Region']

        # Makes requesr
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

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')

    if request.method == 'POST':
        user = request.form
        name = user['name']
        username_league = user['league-user']
        region = user['region']
        email = user['email']
        username = user['username']
        password = user['password']
        password_check = user['password_confirm']

        reg_user = auth.signup(name, username_league, region, username, email, password, password_check)

        if (reg_user == True):
            pass

        else:
            flash('Are you sure you know how to type your password? Please try again')
            return redirect(url_for('signup'))

# Main loop
if (__name__ == '__main__'):
    app.run(debug=1)
