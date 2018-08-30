# Flask modules
from flask import Flask
from flask import render_template
from flask import request
from flask import flash
from flask import Markup
from flask import url_for
from flask import redirect

# Request modules
from engine.Engine import Engine

# Declares flask app constructor
app = Flask(__name__)
app.secret_key = 'TEST_KEY'
engine = Engine()

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
        
        # If error is set equal to true
        elif (user_query['Error'] == 1):
            flash('Ups, summoner not found not found')
            return redirect(url_for('index'))

# Champions route
@app.route('/champion', methods = ['GET', 'POST'])
@app.route('/champion/<name>')
def champions():
    region = 'na1'

    # Get method
    if request.method == 'GET':
        free_champs = engine.free_champs(region)
        winrate = engine.winrate_champs(region)

        return render_template('champions.html', free_champs = free_champs, winrate_champs = winrate)

    ## TODO: FINISH POST METHOD
    elif request.method == 'POST':
        champion_search = engine.free_champs(region)

# Main loop
if (__name__ == '__main__'):
    app.run(debug=1)