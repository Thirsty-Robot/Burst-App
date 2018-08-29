"""
Coded by : Thirsty-Robot
Email : Thirsty-Robot@protonmail.com
Code finished in : TODO
Github Repository :     
"""

from riotwatcher import RiotWatcher
from requests import HTTPError
import os

# Api enviroment variable
api_key = 'RGAPI-b7414bc9-61e5-4500-b9c6-11dcb6f761bf'

# RiotWatcher constructor
watcher = RiotWatcher(api_key)

# Search summoner class
class Engine(object):
    # Class constructor
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
                    'Error': 1
                }

                # Return dictionary
                return user_response
        
    # Free champs method
    # Returns all free champions for the week
    def free_champs(self, region: str):
        champions = watcher.champion.all(region, free_to_play=True)
        champs    = champions['champions']

        for champ in champs:
            self.free_champ_dict.append(champ)
        
        return self.free_champ_dict

    # Winrate champs method
    # Champions with the most winrate in a certain region
    def winrate_champs(self, region):
        champions = watcher.static_data.champions(region)

        return champions

    def search_champ(self, region, name):
        champions = watcher.champion.all(region)

        for name in champions:
            champion = watcher.static_data.champion(region, name)