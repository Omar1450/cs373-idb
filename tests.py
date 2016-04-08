from unittest import main, TestCase
import requests, json
from models import *
import app

class TestApp (TestCase):
    
    # -----------
    # Champions
    # -----------

    def test_champion_1(self):
        champ = app.champion(id = 412) # Will be implemented later
        self.assertEqual(champ.name,  'Thresh')
        self.assertEqual(champ.id, 412)
        self.assertEqual(champ.hp, 560.2)
        self.assertEqual(champ.mp, 273.92)
        self.assertEqual(champ.movespeed, 335.0)
        self.assertEqual(champ.spellblock, 30.0)
    
    def test_champion_2(self):
        champ = Champion(1, 'name', 'tag', 'title', 50, 100, 200, 0, "url")
        self.assertEqual(champ.id, 1)
        self.assertEqual(champ.name, 'name')
        self.assertEqual(champ.title, 'title')
        self.assertEqual(champ.hp, 50)
        self.assertEqual(champ.mp, 100)
        self.assertEqual(champ.movespeed, 200)
        self.assertEqual(champ.spellblock, 0)
        self.assertEqual(champ.url, "url")

    def test_champion_3(self):
        d = json.loads(request.get('dudecarry.me/champion/412').text)
        self.assertEqual(d['name'], 'Thresh')
        self.assertEqual(d['id'], 412)
        self.assertEqual(d['hp'], 560.2)
        self.assertEqual(d['mp'], 273.92)

    # -------------
    # Summoners
    # -------------

    def test_summoner_1(self):
        summoner = app.summoner(id=23509228) # Will be implemented later
        self.assertEqual(summoner.id, 23509228)
        self.assertEqual(summoner.name, "XRedxDragonX")
        self.assertEqual(summoner.win_percentage, )       

    def test_summoner_2(self):
        summoner = Summoner(1, 'name')
        self.assertEqual(summoner.id, 1)
        self.assertEqual(summoner.name, 'name')

    def test_summoner_3(self):
        d = json.loads(request.get('dudecarry.me/summoner/23509228').text)
        self.assertEqual(d['name'], 'XRedxDragonX')
        self.assertEqual(d['id'], 23509228)

    # -------------
    # Teams
    # -------------

    def test_team_1(self):
        team = app.team(id="TEAM-222e7b80-49d9-11e4-806c-782bcb4d0bb2") # Will be implemented later
        self.assertEqual(team.id, "TEAM-222e7b80-49d9-11e4-806c-782bcb4d0bb2")
        self.assertEqual(team.tag, "OPot")
        self.assertEqual(team.win_percentage, 0.5)       

    def test_team_2(self):
        team = Summoner(1, 'name')
        self.assertEqual(team.id, 1)
        self.assertEqual(team.name, 'name')

    def test_team_3(self):
        d = json.loads(request.get('dudecarry.me/team/23509228').text)
        self.assertEqual(team['id'], "TEAM-222e7b80-49d9-11e4-806c-782bcb4d0bb2")
        self.assertEqual(team['tag'], "OPot")
        self.assertEqual(team['win_percentage'], 0.5)       

    # ---------------------------
    # Test database functionality
    # ---------------------------

    def test_db_1(self):
        summ = Summoner(10, "test_name", "bronze", "I", 56, 0.52, 100)
        db.session.add(summ)
        db.session.commit()

        ret = Summoner.query.filter(Summoner.id == 10)

        self.assertEqual(summ.id, ret.id)
        self.assertEqual(summ.name, ret.name)
        self.assertEqual(summ.tier, ret.tier)
        self.assertEqual(summ.division, ret.division)
        self.assertEqual(summ.lp, ret.lp)

     def test_db_2(self):
        champ = Champion(10, "test_name", "bronze champ op", 1, 2, 0.52, 100, "")
        db.session.add(champ)
        db.session.commit()

        ret = Champion.query.filter(Champion.id == 10)

        self.assertEqual(champ.id, ret.id)
        self.assertEqual(champ.name, ret.name)
        self.assertEqual(champ.hp, ret.hp)
        self.assertEqual(champ.spellblock, ret.spellblock)
        self.assertEqual(champ.movespeed, ret.movespeed)

     def test_db_3(self):
        tm = Team("team_id", "test_tag", True, 0.52, 56, "123123")
        db.session.add(tm)
        db.session.commit()

        ret = Team.query.filter(Team.id == "team_id")

        self.assertEqual(tm.id, ret.id)
        self.assertEqual(tm.name, ret.name)
        self.assertEqual(tm.status, ret.status)
        self.assertEqual(tm.total_games, ret.total_games)
        self.assertEqual(tm.win_percentage, ret.win_percentage)

