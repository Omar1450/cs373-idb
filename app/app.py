import logging
import os

from flask import Flask, render_template, request, redirect, url_for, send_file

logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s: %(message)s')

logger = logging.getLogger(__name__)

logger.debug("Starting flask...")

app = Flask(__name__, static_url_path='')

@app.route('/')
def splash():
    return send_file('index.html')
@app.route('/api/champions')
def champions():
    return ''' 
  [{
    "name": "Thresh",
    "id": 412,
    "icon_url": "http://ddragon.leagueoflegends.com/cdn/6.5.1/img/champion/Thresh.png",
    "title": "the Chain Warden",
    "hp": 560.2,
    "mp": 273.92,
    "movespeed": 335.0,
    "spellblock": 30.0,
    "link": "champ0.html",
  },
  {
    "name": "Veigar",
    "id": 45,
    "icon_url": "http://ddragon.leagueoflegends.com/cdn/6.5.1/img/champion/Veigar.png",
    "title": "the Tiny Master of Evil",
    "hp": 492.76,
    "mp": 392.4,
    "movespeed": 340.0,
    "spellblock": 30.0,
    "link": "champ1.html",
  },
  {
    "name": "Katarina",
    "id": 55,
    "icon_url": "http://ddragon.leagueoflegends.com/cdn/6.5.1/img/champion/Katarina.png",
    "title": "the Sinister Blade",
    "hp": 510.0,
    "mp": 0.0,
    "movespeed": 345.0,
    "spellblock": 32.1,
    "link": "champ2.html",
  }]
'''
@app.route('/api/summoners')
def summoners():
    return ''' 
    [{
    "name": "XRedxDragonX",
    "id": 23509228,
    "icon_url": "http://sk2.op.gg/images/profile_icons/profileIcon592.jpg",
    "rank": {
        "tier": "DIAMOND",
        "division": 4,
        "league_points": 69
    },
    "teams": [
        "OPot"
    ],
    "top_3_champions": [
        412,
        45,
        55
    ],
    "win_percentage": 0.539603960396,
    "total_games": 202,
    "link" : "summoner0.html",
  },
  {
    "name": "Eveloken",
    "id": 72680640,
    "icon_url": "http://sk2.op.gg/images/profile_icons/profileIcon1105.jpg",
    "rank": {
        "tier": "CHALLENGER",
        "division": 1,
        "league_points": 1360
    },
    "teams": [
        "OPot"
    ],
    "top_3_champions": [
        55,
        45,
        412
    ],
    "win_percentage": 0.691842900302,
    "total_games": 331,
    "link" : "summoner1.html",
  },
  {
    "name": "Ah Wunder",
    "id": 36109721,
    "icon_url": "http://sk2.op.gg/images/profile_icons/profileIcon588.jpg",
    "rank": {
        "tier": "GOLD",
        "division": 2,
        "league_points": 54
    },
    "teams": [
        "zonpls",
        "ILILI"
    ],
    "top_3_champions": [
        55,
        45,
        412
    ],
    "win_percentage": 0.530120481928,
    "total_games": 83,
    "link" : "summoner2.html",
  }]

'''
@app.route('/api/teams')
def teams():
    return ''' 
     [{
      "name": "Order of the Iron Potato",
      "id": "TEAM-222e7b80-49d9-11e4-806c-782bcb4d0bb2",
      "tag": "OPot",
      "status": "RANKED",
      "win_percentage": 0.5,
      "total_games": 2,
      "most_recent_member_timestamp": 1413137738000,
      "players": [
          23509228,
          72680640
      ],
      "link" : "team0.html",
  },
  {
      "name": "Team Zon and Friends",
      "id": "TEAM-f5b98c70-3bcd-11e4-834d-782bcb4d1861",
      "tag": "zonpls",
      "status": "RANKED",
      "win_percentage": 0.6,
      "total_games": 5,
      "most_recent_member_timestamp": 1432351174000,
      "players": [
          36109721
      ],
      "link" : "team1.html",
  },
  {
      "name": "Tomato Terrors",
      "id": "TEAM-9b111140-5e80-11e5-87b6-c81f66dd45c9",
      "tag": "ILILI",
      "status": "RANKED",
      "win_percentage": 0.6,
      "total_games": 8,
      "most_recent_member_timestamp": 1445915715000,
      "players": [
          36109721
      ],
      "link" : "team2.html",
  }]
'''
@app.route('/api/champion/<int:id>')
def champion(id):
    return '''
    {
    "name": "Thresh",
    "id": 412,
    "icon_url": "http://ddragon.leagueoflegends.com/cdn/6.5.1/img/champion/Thresh.png",
    "title": "the Chain Warden",
    "hp": 560.2,
    "mp": 273.92,
    "movespeed": 335.0,
    "spellblock": 30.0,
    "link": "champ0.html",
   }
'''
@app.route('/api/summoner/<int:id>')
def summoner(id):
    return '''
    {
    "name": "XRedxDragonX",
    "id": 23509228,
    "icon_url": "http://sk2.op.gg/images/profile_icons/profileIcon592.jpg",
    "rank": {
        "tier": "DIAMOND",
        "division": 4,
        "league_points": 69
    },
    "teams": [
        "OPot"
    ],
    "top_3_champions": [
        412,
        45,
        55
    ],
    "win_percentage": 0.539603960396,
    "total_games": 202,
    "link" : "summoner0.html",
   }
'''
@app.route('/api/team/<int:id>')
def team(id):
    return ''' 
    {
      "name": "Team Zon and Friends",
      "id": "TEAM-f5b98c70-3bcd-11e4-834d-782bcb4d1861",
      "tag": "zonpls",
      "status": "RANKED",
      "win_percentage": 0.6,
      "total_games": 5,
      "most_recent_member_timestamp": 1432351174000,
      "players": [
          36109721
      ],
      "link" : "team1.html",
    }
'''

if __name__ == '__main__':
    app.run(host = '0.0.0.0', debug=True)
