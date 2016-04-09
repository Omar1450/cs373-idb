import unittest
from flask.ext.testing import TestCase
import json
from sqlalchemy import create_engine
from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask
from unittest import main
import requests

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///testing.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['TESTING'] = True

test_db = SQLAlchemy(app)

import test_models

class TestApp (TestCase):
    
    # set up test database

    SQLALCHEMY_DATABASE_URI = 'sqlite:///testing.db'

    TESTING = True

    def create_app(self):
        return app

    def setUp(self):
        test_db.create_all();

    def tearDown(self):
        test_db.session.remove()
        test_db.drop_all()

    # -----------
    # Champions
    # -----------

    def test_champion_1(self):
        champ = Champion(0, '', '', 0, 0, 0, 0, "")
        self.assertEqual(champ.name,  '')
        self.assertEqual(champ.id, 0)
        self.assertEqual(champ.hp, 0)
        self.assertEqual(champ.mp, 0)
        self.assertEqual(champ.movespeed, 0)
        self.assertEqual(champ.spellblock, 0)
    
    def test_champion_2(self):
        champ = Champion(1, 'name', 'title', 50, 100, 200, 0, "url")
        self.assertEqual(champ.id, 1)
        self.assertEqual(champ.name, 'name')
        self.assertEqual(champ.title, 'title')
        self.assertEqual(champ.hp, 50)
        self.assertEqual(champ.mp, 100)
        self.assertEqual(champ.movespeed, 200)
        self.assertEqual(champ.spellblock, 0)
        self.assertEqual(champ.portrait_url, "url")

    # def test_champion_3(self):
    #     d = json.loads(requests.get('dudecarry.me/champion/412').text)
    #     self.assertEqual(d['name'], 'Thresh')
    #     self.assertEqual(d['id'], 412)
    #     self.assertEqual(d['hp'], 560.2)
    #     self.assertEqual(d['mp'], 273.92)

    # -------------
    # Summoners
    # -------------

    def test_summoner_1(self):
        summoner = Summoner(0, "", "", "", 0, 0, 0)
        self.assertEqual(summoner.id, 0)
        self.assertEqual(summoner.name, "")
        self.assertEqual(summoner.win_percentage, 0.52)       

    def test_summoner_2(self):
        summoner = Summoner(10, "test_name", "bronze", "I", 56, 0.52, 100)
        self.assertEqual(summoner.id, 10)
        self.assertEqual(summoner.name, 'test_name')

    # def test_summoner_3(self):
    #     d = json.loads(request.get('dudecarry.me/summoner/23509228').text)
    #     self.assertEqual(d['name'], 'XRedxDragonX')
    #     self.assertEqual(d['id'], 23509228)

    # -------------
    # Teams
    # -------------

    def test_team_1(self):
        team = Team("", "", "", False, 0, 0, "")
        self.assertEqual(team.id, "")
        self.assertEqual(team.tag, "")
        self.assertEqual(team.win_percentage, 0)       

    def test_team_2(self):
        team = Team("team_id", "test-name", "test_tag", True, 0.52, 56, "123123")
        self.assertEqual(team.id, "team_id")
        self.assertEqual(team.name, 'test-name')

    # def test_team_3(self):
    #     d = json.loads(requests.get('dudecarry.me/team/23509228').text)
    #     self.assertEqual(team['id'], "TEAM-222e7b80-49d9-11e4-806c-782bcb4d0bb2")
    #     self.assertEqual(team['tag'], "OPot")
    #     self.assertEqual(team['win_percentage'], 0.5)       

    # ---------------------------
    # Test database functionality
    # ---------------------------

    def test_db_1(self):
        summ = Summoner(10, "test_name", "bronze", "I", 56, 0.52, 100)
        
        test_db.session.add(summ)
        test_db.session.commit()

        ret = Summoner.query.filter(Summoner.id == 10).first()

        self.assertEqual(summ.id, ret.id)
        self.assertEqual(summ.name, ret.name)
        self.assertEqual(summ.tier, ret.tier)
        self.assertEqual(summ.division, ret.division)
        self.assertEqual(summ.lp, ret.lp)

        test_db.session.delete(summ)
        test_db.session.commit()

    def test_db_2(self):
        champ = Champion(10, "test_name", "bronze champ op", 1, 2, 3, 100, "")
        test_db.session.add(champ)
        test_db.session.commit()

        ret = Champion.query.filter(Champion.id == 10).first()

        self.assertEqual(champ.id, ret.id)
        self.assertEqual(champ.name, ret.name)
        self.assertEqual(champ.hp, ret.hp)
        self.assertEqual(champ.spellblock, ret.spellblock)
        self.assertEqual(champ.movespeed, ret.movespeed)

        test_db.session.delete(champ)
        test_db.session.commit()

    def test_db_3(self):
        tm = Team("team_id", "team_name", "test_tag", True, 0.52, 56, "123123")

        test_db.session.add(tm)
        test_db.session.commit()

        ret = Team.query.filter(Team.id == "team_id").first()

        self.assertEqual(tm.id, ret.id)
        self.assertEqual(tm.name, ret.name)
        self.assertEqual(tm.status, ret.status)
        self.assertEqual(tm.total_games, ret.total_games)
        self.assertEqual(tm.win_percentage, ret.win_percentage)

        test_db.session.delete(tm)
        test_db.session.commit()

    # --------------------------------
    # Test test_models.py API functionality
    # --------------------------------

    def test_apiCall_1(self):
        summ = Summoner(10, "test_name", "bronze", "I", 56, 0.52, 100)
        
        test_db.session.add(summ)
        test_db.session.commit()

        summoner = Summoner.query.filter(Summoner.id == 10).first()

        summ_true = {
            "id":               10,
            "name":             "test_name",
            "rank":             236,
            "tier":             "bronze",
            "division":         "I",
            "lp":               56,
            "win_percentage":   0.52,
            "total_games":      100,
            "teams":            [],
            "top_3_champs":     []
        }


        summ_test = test_models.summoner_to_json(summoner)
       

        self.assertEqual(summ_test, json.dumps(summ_true))

        test_db.session.delete(summ)
        test_db.session.commit()


    def test_apiCall_2(self):
        tm = Team("team_id", "team_name", "test_tag", True, 0.52, 56, "123123")
        test_db.session.add(tm)
        test_db.session.commit()

        team = Team.query.filter(Team.id == "test-id").first()

        team_true = {
            "id":                           "team_id",
            "name":                         "team_name",
            "tag":                          "test_tag",
            "status":                       True,
            "win_percentage":               0.52,
            "total_games":                  56,
            "most_recent_member_timestamp": "123123",
            "summoners":                    []    
        }

        team_test = test_models.team_to_json(team)

        self.assertEqual(team_test, json.dumps(team_true))

        test_db.session.delete(tm)
        test_db.session.commit()

    def test_apiCall_3(self):

        champ = Champion(10, "test_name", "bronze champ op", 1, 2, 3, 100, "")
        test_db.session.add(champ)
        test_db.session.commit()

        champ = Champion.query.filter(Champion.id == 10).first()

        champ_true = {
            "id":         10,
            "name":       "test_name",
            "title":      "bronze champ op",
            "hp":         1,
            "mp":         2,
            "movespeed":  3,
            "spellblock": 100,
            "icon_url":   ""
        }

        champ_test = test_models.champ_to_json(champ)

        self.assertEqual(champ_test, json.dumps(champ_true))

        test_db.session.delete(champ)
        test_db.session.commit()
        self.assertEqual(champ_test, champ_true)


if __name__ == '__main__':
    main()
