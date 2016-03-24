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


