"""
models.py
"""

import json

from sqlalchemy import *
from sqlalchemy.orm import relationship

from database import Base

class Summoner(Base):
	"""
	A Summoner is the equivalent of a player in League of Legends, each Summoner has a pool of champions he or she much unlock to be able to player
	A Summoner can play Ranked Matches in order to increase his Rank, declared as (tier, division, lp). In order to be promoted in division, and eventually tier,
	he or she must earn League Points, or LP, by winning Matches.
	Thus, win rate is important.
	A Summoner can also join social circles called Teams, where teams have definitive rosters that can compete in Ranked matches as well.
	A Summoner can earn Mastery Points with any corresponding unlocked Champion, where mastery points describes the relative skill the summoner has with the champion
	"""
	__tablename__ = 'summoner'
	id = Column(Integer, primary_key=True)
	name = Column(String)
	rank = Column(Integer)
	tier = Column(String)
	division = Column(Integer)
	lp = Column(Integer)
	champions = relationship("summ2champ_asc", back_populates="summoner")
	teams = relationship("summ2team_asc", back_populates="summoner")
	total_games = Column(Integer)
	win_percentage = Column(Float)
	#search_vector = Column(TSVectorType('name', 'summoner_id', 'rank'))

	def __init__(self, s_id, name, tier, division, lp, win_per, total_games):
		self.id = s_id
		self.name = name
		if (tier.lowercase() == "bronze"):
			self.rank += 10
		elif (tier.lowercase() == "silver"):
			self.rank += 20
		elif (tier.lowercase() == "gold"):
			self.rank += 30
		elif (tier.lowercase() == "platinum"):
			self.rank += 40
		elif (tier.lowercase() == "diamond"):
			self.rank += 50
		elif (tier.lowercase() == "master"):
			self.rank += 60
		elif (tier.lowercase() == "challenger"):
			self.rank += 70
		self.rank += int(division)
		self.tier = tier
		self.division = division
		self.lp = lp
		self.win_percentage = win_per
		self.total_games = total_games

class Team(Base):
	"""
	Teams are composed of Summoners, with the minimum of 1 Summoner per team. Each team name is unique. Each Team can play in a competitive setting in ranked matches
	"""
	__tablename__ = 'team'
	id = Column(String, primary_key=True)
	tag = Column(String)
	status = Column(Boolean)
	win_percentage = Column(Float)
	total_games = Column(Integer)
	most_recent_member_timestamp = Column(Date)
	summoners = relationship("summ2team_asc", back_populates="team")

	def __init__(self, id, tag, status, win_p, total_games, most_recent_member_timestamp):
		self.id = id
		self.tag = tag
		self.status = status
		self.win_percentage = win_p
		self.total_games = total_games
		self.most_recent_member_timestamp = most_recent_member_timestamp

class Champion(Base):
	"""
	Champions are the characters that Summoners can play in this game. Each Champion has unique abilities and personalized base stats which change with level.
	"""
	__tablename__ = 'champion'
	id = Column(Integer, primary_key=True)
	name = Column(String)
	title = Column(String)
	hp = Column(Float)
	mp = Column(Float)
	movespeed = Column(Float)
	spellblock = Column(Float)
	summoners = relationship("summ2champ_asc", back_populates="champion")
	portrait_url = Column(String)

	def __init__(self, id, name, title, hp, mp, movespeed, spellblock, portrait_url):
		self.id = id
		self.name = name
		self.title = title
		self.hp = hp
		self.mp = mp
		self.movespeed = movespeed
		self.spellblock = spellblock
		self.portrait_url = portrait_url

class summ2team_asc(Base):
	"""
	Maps the relationship between Summoners and Teams
	A Summoner can be in multiple teams
	A Team can have multiple summoners
	This many-to-many relationship is represented thru an association table
	"""
	__tablename__ = 'summ2team_asc'
	# id = Column(Integer, primary_key=True)
	summ_id = Column(Integer, ForeignKey('summoner.id'), primary_key=True)
	team_id = Column(String, ForeignKey('team.id'), primary_key=True)

class summ2champ_asc(Base):
	"""
	Maps the relationship between Summoners and Champions
	A Summoner can have multiple Champions
	A Champion can be unlocked by multiple Summoners
	Each Summoner has respective Mastery Points with a corresponding Champion
	This many-to-many relationship is represented thru an association table
	"""
	__tablename__ = 'summ2champ_asc'
	# id = Column(Integer, primary_key=True)
	summ_id = Column(Integer, ForeignKey('summoner.id'), primary_key=True)
	champ_id = Column(Integer, ForeignKey('champion.id'), primary_key=True)
	mastery_score = Column(Integer)
