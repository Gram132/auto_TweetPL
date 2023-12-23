import requests
import json
from bs4 import BeautifulSoup

#General Variable
g_Header ={
    'if-Modified-Since':'Sun, 11 May 2023 00:00:00 GMT+1',
    'authority': 'api.sofascore.com',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9,fr;q=0.8',
    'cache-control': 'max-age=0',
    'origin': 'https://www.sofascore.com',
    'referer': 'https://www.sofascore.com/',
    'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
}

#Get Data Statistics
def getData(ID):
    headers = g_Header
    headers['if-none-match']='W/"79c7ad21cd"'
    stats = requests.get(f"https://api.sofascore.com/api/v1/event/{ID}/statistics", headers=headers)
    headers['if-none-match']='W/"2ba0252f79"'
    event = requests.get(f"https://api.sofascore.com/api/v1/event/{ID}", headers=headers)
    return {'stats' :stats ,'event' :event }

#set Data
def setData(ID):
    statsData= getData(ID)['stats'].json()
    game_Metadata= getData(ID)['event'].json()['event']
    
    gameData={}
    gameData['homeTeam']=game_Metadata['homeTeam']['name']
    gameData['awayTeam']=game_Metadata['awayTeam']['name']
    gameData['homeScored']=game_Metadata['homeScore']['current']
    gameData['awayScored']=game_Metadata['awayScore']['current']
    gameData['statistics']= statsData['statistics'][0]
    
    return gameData

def check_ID(id):
    try:
        game_Metadata= getData(id)['event'].json()['event']
        gameData={}
        gameData['homeTeam']=game_Metadata['homeTeam']['name']
        gameData['awayTeam']=game_Metadata['awayTeam']['name']
        game ={'home':gameData['homeTeam'], 'away':gameData['awayTeam']}
        print(game)
        return game
    except:
        return 0
#Get Best players
#def get_bestPlayer(ID,item):
#    headers = g_Header
#    headers['if-none-match']='W/"56c35d4ea3"'
#    stats = requests.get(f"https://api.sofascore.com/api/v1/event/{ID}/{item}", headers=headers)
#    return stats.json()
#homeBestPlayer =get_bestPlayer(11352353,'best-players')['bestHomeTeamPlayer']
#
##Get best player's stats
##homeBestPlayer =get_bestPlayer(11352353,'lineups')
##homeBestPlayer
#player_name_to_find = 'Leandro Trossard'
#
#player_data = get_bestPlayer(11352353,'lineups')['home']['players']
#desired_player = None
#for player in player_data:
#    if player['player']['name'] == player_name_to_find:
#        desired_player = player
#        break
#
## Print the data for the desired player
#if desired_player:
#    print(desired_player)
#else:
#    print(f"Player with name '{player_name_to_find}' not found.")

#print(check_ID(11352373))