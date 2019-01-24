"""
Coded by: Thirsty-Robot (Axel C. Uribe);
Email: Thirsty-Robot@protonmail.com;
License : MIT;
"""

from riotwatcher import RiotWatcher
from requests import HTTPError
import os
import json

# Api enviroment variable
api_key = 'RGAPI-e42b0ebf-fa4a-466d-8b9d-ed62fa7084fc'

# RiotWatcher constructor
watcher = RiotWatcher(api_key)

# Search summoner class
class Engine():
    def __init__(self):
        self.free_champ_dict = []

    # Summoner Search method
    # Requests Riot's API for summoner information
    # Returns a dictionary
    def search(self, name: str, region: str):
        # Ping for 404 callback
        try:
            # Search summoner and ranked status
            summoner     = watcher.summoner.by_name(region, name)
            ranked_stats = watcher.league.positions_by_summoner(region, summoner['id'])

            # Parsed information in dictionary
            user_response = {
                'Icon'  : summoner['profileIconId'],
                'Name'  : summoner['name'],
                'Level' : summoner['summonerLevel'],
                'Tier'  : ranked_stats[0]['tier'],
                'Rank'  : ranked_stats[0]['rank'],
                'Error' : 0
            }

            # Returns parsed information
            return user_response 

        # Get error as err
        except HTTPError as err:
            # Error message is 404
            if err.response.status_code == 404:                
                # Parsed dictionary with error boolean set to 1
                user_response = {
                    'Error' : 1
                }

                # Return dictionary
                return user_response

            # If there is any other type of error
            else:
                # Parsed dictionary with type 2 error
                user_respose = {
                    'Error' : 2
                }

                # Return dictionary
                return user_respose

    def confirm_summoner(self, name, region):
        try:
            summoner = watcher.summoner.by_name(region, name)

            return True

        except HTTPError as err:
            if err.response.status_code == 404:
                return False

    def simple_search(self, name, region):
        try:
            summoner = watcher.summoner.by_name(region, name)

            response = {
                'icon' : summoner['profileIconId'],
                'name' : summoner['name']
            }

            return response
        
        except HTTPError as err:
            if err.response.status_code == 404:
                return 0