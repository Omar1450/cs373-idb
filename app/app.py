import logging
import os
import time
import ast

from flask import Flask, render_template, request, redirect, url_for, send_file, jsonify
from flask.ext.script import Manager, Server
from flask.ext.sqlalchemy import SQLAlchemy


logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s: %(message)s')

logger = logging.getLogger(__name__)

logger.debug("Starting flask...")

app = Flask(__name__, static_url_path='')

DATABASE_URI = \
    '{engine}://{username}:{password}@{hostname}/{database}'.format(
        engine='mysql+pymysql',
    username=os.getenv('MYSQL_USER'),
    password=os.getenv('MYSQL_PASSWORD'),
    hostname=os.getenv('MYSQL_HOST'),
    database=os.getenv('MYSQL_DATABASE'))

app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_ECHO'] = True

logger.debug("%s", DATABASE_URI)

manager = Manager(app)

db = SQLAlchemy(app)

import models
from models import *

logger.debug("finished start up")

@manager.command
def populate():
  summ_f = open("summoners.txt", "r")
  team_f = open("teams.txt", "r")
  chmp_f = open("champions.txt", "r")

  o1 = str(team_f.readline()) 
  o2 = str(summ_f.readline())
  o3 = str(chmp_f.readline())

  team_data = json.loads(o1)
  summ_data = json.loads(o2)
  chmp_data = ast.literal_eval(o3)

  for t in team_data:
    boo = True if team_data[t]["team_status"] == "RANKED" else False
    new_team = Team(team_data[t]["fullTeamId"], team_data[t]["team_name"], 
      team_data[t]["team_tag"], boo , team_data[t]["team_win_perc"], 
      team_data[t]["team_total_games"], str(team_data[t]["team_lastJoinDate"]))
    db.session.add(new_team)

  db.session.commit()

  for c in chmp_data:
    new_chmp = Champion(chmp_data[c]["id"], chmp_data[c]["name"], chmp_data[c]["title"], chmp_data[c]["stats"]["hp"],
                        chmp_data[c]["stats"]["mp"], chmp_data[c]["stats"]["movespeed"], chmp_data[c]["stats"]["spellblock"], "")
    db.session.add(new_chmp)

  db.session.commit()

  for s in summ_data:
    new_summ = Summoner(int(summ_data[s]["player_id"]), s, summ_data[s]["rank"]["tier"], 
                summ_data[s]["rank"]["division"], summ_data[s]["rank"]["league_points"], summ_data[s]["win_perc"], summ_data[s]["total_games"])
    for s_t in summ_data[s]["teams"]:
      team_link = Team.query.filter(Team.id == s_t["fullTeamId"]).first()
      new_summ.teams.append(team_link)
    for s_c in summ_data[s]["champ_mastery"]:
      champ_link = Champion.query.filter(Champion.id == s_c["champID"]).first()

      # , int(s["player_id"]), s_c["champID"]
      mastery = SummonerChampionMastery(s_c["mastery_score"] , int(summ_data[s]["player_id"]), s_c["champID"])

      db.session.add(mastery)

      new_summ.champions.append(mastery)
      champ_link.summoners.append(mastery)

    db.session.add(new_summ)

  db.session.commit()

@manager.command
def create_db():
  logger.debug("creating db..")
  app.config['SQLALCHEMY_ECHO'] = True
  db.drop_all()
  db.create_all()

@manager.command
def create_travis_db():
  logger.debug("creating db..")
  app.config['SQLALCHEMY_ECHO'] = True
  db.drop_all()
  db.create_all()

@manager.command
def create_dummy_data():

  # wrong
  champion = Champion(5, "john", "asdfasf", 20.5, 60.2, 55.5, 2.2, "example.com")
  team = Team(10, "asdfasdfaskljlkj", True, 60.0, 105, 89)
  summoner = Summoner(15, "bob", "bronze", 1, 50, 25.0, 100)
  summoner2 = Summoner(20, "bob", "bronze", 1, 50, 25.0, 100)
  mastery = SummonerChampionMastery(50)
  summoner.champions.append(mastery)
  summoner.teams.append(team)
  champion.summoners.append(mastery)

  mastery2 = SummonerChampionMastery(70)
  summoner2.champions.append(mastery2)
  champion.summoners.append(mastery2)
  db.session.add(summoner)
  db.session.add(champion)
  db.session.add(team)
  db.session.commit()

@app.route('/')
def splash():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/champions')
def champions():
    return render_template('champions.html')

@app.route('/champion/<int:id>')
def champion(id):
    return render_template('champ.html', id=id)

@app.route('/teams')
def teams(teams):
    return render_template('teams.html')

@app.route('/team/<int:id>')
def team(id):
    return render_template('team.html', id=id)

@app.route('/summoners')
def summoners():
    return render_template('summoners.html')

@app.route('/summoner/<int:id>')
def summoner(id):
    return render_template('summoner.html', id=id)

@app.route('/api/champions')
def api_champions():
    champions = Champion.query.all()
    return jsonify({"champions": [champion_to_json(c) for c in champions]})

@app.route('/api/summoners')
def api_summoners():
    summoners = Summoner.query.all()
    return jsonify({"summoners": [summoner_to_json(s) for s in summoners]})


@app.route('/api/teams')
def api_teams():
    teams = Team.query.all()
    return jsonify({"teams": [team_to_json(t) for t in teams]})

def jsonify_single_obj(obj, func):
    if obj == None:
        return jsonify({})
    else:
        return jsonify(func(obj))

@app.route('/api/champion/<int:id>')
def api_champion(id):
    champion = Champion.query.filter(Champion.id == id).first()
    return jsonify_single_obj(champion, champion_to_json)

@app.route('/api/summoner/<int:id>')
def api_summoner(id):
    summoner = Summoner.query.filter(Summoner.id == id).first()
    return jsonify_single_obj(summoner, summoner_to_json)

@app.route('/api/team/<id>')
def api_team(id):
    team = Team.query.filter(Team.id == id).first()
    return jsonify_single_obj(team, team_to_json)

if __name__ == '__main__':

    manager.run()
