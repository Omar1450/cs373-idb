#!/usr/bin/env python3

"""
models.py
"""

import json

from flask.ext.sqlalchemy import SQLAlchemy

from tests import t_db 

team_membership = t_db.Table('team_membership', 
    t_db.Column('summoner_id', t_db.Integer, t_db.ForeignKey('summoner.id')),
    t_db.Column('team_id', t_db.String(50), t_db.ForeignKey('team.id'))
    )

class Summoner(t_db.Model):
    """
    A Summoner is the equivalent of a player in League of Legends, each Summoner has a pool of champions he or she much unlock to be able to player
    A Summoner can play Ranked Matches in order to increase his Rank, declared as (tier, division, lp). In order to be promoted in division, and eventually tier,
    he or she must earn League Points, or LP, by winning Matches.
    Thus, win rate is important.
    A Summoner can also join social circles called Teams, where teams have definitive rosters that can compete in Ranked matches as well.
    A Summoner can earn Mastery Points with any corresponding unlocked Champion, where mastery points describes the relative skill the summoner has with the champion
    """
    __tablename__ = 'summoner'
    id = t_db.Column(t_db.Integer, primary_key=True)
    name = t_db.Column(t_db.String(50))
    rank = t_db.Column(t_db.Integer)
    tier = t_db.Column(t_db.String(50))
    division = t_db.Column(t_db.String(10))
    lp = t_db.Column(t_db.Integer)
    champions = t_db.relationship("SummonerChampionMastery", backref=t_db.backref("summoner"))
    teams = t_db.relationship("Team", secondary=team_membership, backref=t_db.backref("summoners"))
    total_games = t_db.Column(t_db.Integer)
    win_percentage = t_db.Column(t_db.Float)
    #search_vector = t_db.Column(TSVectorType('name', 'summoner_id', 'rank'))

    def __init__(self, s_id, name, tier, division, lp, win_per, total_games):
        self.id = s_id
        self.name = name
        self.rank = 0
        if (tier.lower() == "bronze"):
            self.rank += 100
        elif (tier.lower() == "silver"):
            self.rank += 200
        elif (tier.lower() == "gold"):
            self.rank += 300
        elif (tier.lower() == "platinum"):
            self.rank += 400
        elif (tier.lower() == "diamond"):
            self.rank += 500
        elif (tier.lower() == "master"):
            self.rank += 600
        elif (tier.lower() == "challenger"):
            self.rank += 700

        if (division == "I"):
            self.rank += 80
        if (division == "II"):
            self.rank += 60
        if (division == "III"):
            self.rank += 40
        if (division == "IV"):
            self.rank += 20
        if (division == "V"):
            self.rank += 0

        self.tier = tier
        self.division = division
        self.lp = lp
        self.win_percentage = win_per
        self.total_games = total_games

def summoner_to_json(summoner):
    # champ_list = summoner.champions
    # champ_list = sorted(champ_list, key=lambda m : m.mastery_score)

    return {
        "id":               summoner.id,
        "name":             summoner.name,
        "rank":             summoner.rank,
        "tier":             summoner.tier,
        "division":         summoner.division,
        "lp":               summoner.lp,
        "win_percentage":   summoner.win_percentage,
        "total_games":      summoner.total_games,
        "teams":            [{"id": t.id, "tag": t.tag} for t in summoner.teams],
        "top_3_champs": [{"id": c.champion.id, "name": c.champion.name, "masteryScore" : c.mastery_score} for c in sorted(summoner.champions, key=lambda m: m.mastery_score)[0:3]]
    }

class Team(t_db.Model):
    """
    Teams are composed of Summoners, with the minimum of 1 Summoner per team. Each team name is unique. Each Team can play in a competitive setting in ranked matches
    """
    __tablename__ = 'team'
    id = t_db.Column(t_db.String(50), primary_key=True)
    name = t_db.Column(t_db.String(255))
    tag = t_db.Column(t_db.String(50))
    status = t_db.Column(t_db.Boolean)
    win_percentage = t_db.Column(t_db.Float)
    total_games = t_db.Column(t_db.Integer)
    most_recent_member_timestamp = t_db.Column(t_db.String(255))

    def __init__(self, id, name, tag, status, win_p, total_games, most_recent_member_timestamp):
        self.id = id
        self.name = name
        self.tag = tag
        self.status = status
        self.win_percentage = win_p
        self.total_games = total_games
        self.most_recent_member_timestamp = most_recent_member_timestamp

def team_to_json(team):
    return {
        "id":                           team.id,
        "name":                         team.name,
        "tag":                          team.tag,
        "status":                       team.status,
        "win_percentage":               team.win_percentage,
        "total_games":                  team.total_games,
        "most_recent_member_timestamp": team.most_recent_member_timestamp,
        "summoners": [{"id": s.id, "name": s.name} for s in team.summoners]    
    }

class Champion(t_db.Model):
    """
    Champions are the characters that Summoners can play in this game. Each Champion has unique abilities and personalized t_db.Model stats which change with level.
    """
    __tablename__ = 'champion'
    id = t_db.Column(t_db.Integer, primary_key=True)
    name = t_db.Column(t_db.String(50))
    title = t_db.Column(t_db.String(50))
    hp = t_db.Column(t_db.Float)
    mp = t_db.Column(t_db.Float)
    movespeed = t_db.Column(t_db.Float)
    spellblock = t_db.Column(t_db.Float)
    portrait_url = t_db.Column(t_db.String(50))
    summoners = t_db.relationship("SummonerChampionMastery", backref=t_db.backref("champion"))

    def __init__(self, id, name, title, hp, mp, movespeed, spellblock, portrait_url):
        self.id = id
        self.name = name
        self.title = title
        self.hp = hp
        self.mp = mp
        self.movespeed = movespeed
        self.spellblock = spellblock
        self.portrait_url = portrait_url

def champion_to_json(champion):
    return {
        "id":         champion.id,
        "name":       champion.name,
        "title":      champion.title,
        "hp":         champion.hp,
        "mp":         champion.mp,
        "movespeed":  champion.movespeed,
        "spellblock": champion.spellblock,
        "icon_url":   champion.portrait_url
    }

class SummonerChampionMastery(t_db.Model):               
    """             
    Maps the t_db.relationship between Summoners and Champions                
    A Summoner can have multiple Champions          
    A Champion can be unlocked by multiple Summoners                
    Each Summoner has respective Mastery Points with a corresponding Champion               
    This many-to-many t_db.relationship is represented thru an association table              
    """             
    __tablename__ = 'summoner_champion_mastery'             
    summ_id = t_db.Column(t_db.Integer, t_db.ForeignKey('summoner.id'), primary_key=True)         
    champ_id = t_db.Column(t_db.Integer, t_db.ForeignKey('champion.id'), primary_key=True)                
    mastery_score = t_db.Column(t_db.Integer)
    
    def __init__(self, score, pid, cid):
        self.mastery_score = score
        self.summ_id = pid
        self.champ_id = cid