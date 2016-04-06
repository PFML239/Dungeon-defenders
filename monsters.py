from __future__ import division, print_function, unicode_literals
import six

import sys
import os

from const import *

power = {1: 'power_strong', 0: 'power_weak'}
orc = {'damage': 90, 'power_strong': 140, 'power_weak': 80, 'strong': 4, 'weak': 3}
fly = {'damage': 80, 'power_strong': 220, 'power_weak': 20, 'strong': 2, 'weak': 2}

class Orc():
	def __init__(self, model, tile):
		self.spike = 1
		self.phase = 0
		self.power = orc[power[self.spike]]
		self.model = model
		self.tile = tile
		self.tile.name = 'orc_strong'
		
	def new_turn(self):
		self.phase = self.phase + 1
		if self.spike and self.phase == orc['strong']:
			self.phase = 0
			self.spike = 0
			self.power = orc['power_weak']
			self.tile.name = 'orc_weak'
		if (self.spike == 0) and self.phase == orc['weak']:
			self.phase = 0
			self.spike = 1
			self.power = orc['power_strong']
			self.tile.name = 'orc_strong'
	
	def fight(self, hero):
		self.hero = hero
		if (self.power >= hero.stats.power):
			damage = max(0, orc['damage'] - hero.stats.armor)
			self.model.controler.damage_hero(self.hero.name, damage)
			return('lose')
		else:
			damage = max(0, orc['damage'] - hero.stats.armor - hero.stats.attack)
			self.model.controler.damage_hero(self.hero.name, damage)
			self.model.monsters.remove(self)
			self.tile.monster = 0
			self.tile.name = 'floor'
			return('win')
		
class Fly():
	def __init__(self, model, tile):
		self.spike = 1
		self.phase = 0
		self.power = fly[power[self.spike]]
		self.model = model
		self.tile = tile
		self.tile.name = 'fly_strong'
		
	def new_turn(self):
		self.phase = self.phase + 1
		if self.spike and self.phase == fly['strong']:
			self.phase = 0
			self.spike = 0
			self.power = fly['power_weak']
			self.tile.name = 'fly_weak'
		if (self.spike == 0) and self.phase == fly['weak']:
			self.phase = 0
			self.spike = 1
			self.power = fly['power_strong']
			self.tile.name = 'fly_strong'
	
	def fight(self, hero):
		self.hero = hero
		if (self.power >= hero.stats.power):
			damage = max(0, fly['damage'] - hero.stats.armor)
			self.model.controler.damage_hero(self.hero.name, damage)
			return('lose')
		else:
			damage = max(0, fly['damage'] - hero.stats.armor - hero.stats.attack)
			self.model.controler.damage_hero(self.hero.name, damage)
			self.model.monsters.remove(self)
			self.tile.monster = 0
			self.tile.name = 'floor'
			return('win')
			
DM_Monsters = {'orc': Orc, 'fly' : Fly}