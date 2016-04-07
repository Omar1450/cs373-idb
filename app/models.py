"""
models.py
"""

import json

from app import db 
from flask.ext.sqlalchemy import SQLAlchemy

summoner_mastery = db.Table('summoner_mastery',
    db.Column('summoner_id', db.Integer, db.ForeignKey('summoner.id')),
    db.Column('champ_id', db.Integer, db.ForeignKey('champion.id'))
    )

team_membership = db.Table('team_membership', 
    db.Column('summoner_id', db.Integer, db.ForeignKey('summoner.id')),
    db.Column('team_id', db.String(50), db.ForeignKey('team.id'))
    )

class Summoner(db.Model):
	"""
	A Summoner is the equivalent of a player in League of Legends, each Summoner has a pool of champions he or she much unlock to be able to player
	A Summoner can play Ranked Matches in order to increase his Rank, declared as (tier, division, lp). In order to be promoted in division, and eventually tier,
	he or she must earn League Points, or LP, by winning Matches.
	Thus, win rate is important.
	A Summoner can also join social circles called Teams, where teams have definitive rosters that can compete in Ranked matches as well.
	A Summoner can earn Mastery Points with any corresponding unlocked Champion, where mastery points describes the relative skill the summoner has with the champion
	"""
	__tablename__ = 'summoner'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50))
	rank = db.Column(db.Integer)
	tier = db.Column(db.String(50))
	division = db.Column(db.Integer)
	lp = db.Column(db.Integer)
	champions = db.relationship("Champion", secondary=summoner_mastery, backref=db.backref("mastery", lazy='dynamic'))
	teams = db.relationship("Team", secondary=team_membership, backref=db.backref("teammembership", lazy='dynamic'))
	total_games = db.Column(db.Integer)
	win_percentage = db.Column(db.Float)
	#search_vector = db.Column(TSVectorType('name', 'summoner_id', 'rank'))

	def __init__(self, s_id, name, tier, division, lp, win_per, total_games):
		self.id = s_id
		self.name = name
		self.rank = 0
		if (tier.lower() == "bronze"):
			self.rank += 10
		elif (tier.lower() == "silver"):
			self.rank += 20
		elif (tier.lower() == "gold"):
			self.rank += 30
		elif (tier.lower() == "platinum"):
			self.rank += 40
		elif (tier.lower() == "diamond"):
			self.rank += 50
		elif (tier.lower() == "master"):
			self.rank += 60
		elif (tier.lower() == "challenger"):
			self.rank += 70
		self.rank += int(division)
		self.tier = tier
		self.division = division
		self.lp = lp
		self.win_percentage = win_per
		self.total_games = total_games

class Team(db.Model):
	"""
	Teams are composed of Summoners, with the minimum of 1 Summoner per team. Each team name is unique. Each Team can play in a competitive setting in ranked matches
	"""
	__tablename__ = 'team'
	id = db.Column(db.String(50), primary_key=True)
	tag = db.Column(db.String(50))
	status = db.Column(db.Boolean)
	win_percentage = db.Column(db.Float)
	total_games = db.Column(db.Integer)
	most_recent_member_timestamp = db.Column(db.Integer)

	def __init__(self, id, tag, status, win_p, total_games, most_recent_member_timestamp):
		self.id = id
		self.tag = tag
		self.status = status
		self.win_percentage = win_p
		self.total_games = total_games
		self.most_recent_member_timestamp = most_recent_member_timestamp

class Champion(db.Model):
	"""
	Champions are the characters that Summoners can play in this game. Each Champion has unique abilities and personalized db.Model stats which change with level.
	"""
	__tablename__ = 'champion'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50))
	title = db.Column(db.String(50))
	hp = db.Column(db.Float)
	mp = db.Column(db.Float)
	movespeed = db.Column(db.Float)
	spellblock = db.Column(db.Float)
	portrait_url = db.Column(db.String(50))

	def __init__(self, id, name, title, hp, mp, movespeed, spellblock, portrait_url):
		self.id = id
		self.name = name
		self.title = title
		self.hp = hp
		self.mp = mp
		self.movespeed = movespeed
		self.spellblock = spellblock
		self.portrait_url = portrait_url

