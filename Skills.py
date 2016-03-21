from __future__ import division, print_function, unicode_literals
import six

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pyglet
from pyglet.gl import *
from pyglet import image

from cocos.director import *
from cocos.layer import *
from cocos.sprite import Sprite

from const import *

class Clairvoyance():
	def __init__(self, hero, model):
	
		self.cd = 3
		
		self.hero = hero
		self.model = model
		self.cd_left = 0
		self.available = 1
		self.object = 'tile'
		
	def use(self):
		self.model.skill_use = self
	
	def end_cast(self, tile):
		self.hero.turnav = self.hero.turnav - 1
		tile.open_P = 1
		self.cd_left = self.cd
		self.available = 0
		self.model.skill_use = 0
	
	def next_turn(self):
		if self.cd_left:
			self.cd_left = self.cd_left - 1
			if self.cd_left == 0:
				self.available = 1
				
	def cancel(self):
		self.model.skill_use = 0

class Flash_heal():
	def __init__(self, hero, model):
	
		self.heal_power = 5
		self.cd = 3
		
		self.hero = hero
		self.model = model
		self.cd_left = 0
		self.available = 1
		self.object = 'hero'
		
	def use(self):
		self.model.skill_use = self
	
	def end_cast(self, hero):
		self.model.controler.heal_hero(hero.name, self.heal_power)
		self.hero.turnav = self.hero.turnav - 1
		self.cd_left = self.cd
		self.available = 0
		self.model.skill_use = 0
	
	def next_turn(self):
		if self.cd_left:
			self.cd_left = self.cd_left - 1
			if self.cd_left == 0:
				self.available = 1
				
	def cancel(self):
		self.model.skill_use = 0
		
class Weapon_improve():
	def __init__(self, hero, model):
	
		self.add_armor = 2
		self.cd = 3
	
		self.hero = hero
		self.model = model
		self.cd_left = 0
		self.available = 1
		
	def use(self):
		self.hero.turnav = self.hero.turnav - 1
		self.hero.stats.armor = self.hero.stats.armor + self.add_armor
		self.cd_left = self.cd
		self.available = 0
		
	def next_turn(self):
		if self.cd_left:
			self.cd_left = self.cd_left - 1
			if self.cd_left == 0:
				self.available = 1

class Smoke():
	def __init__(self, hero, model):
	
		self.smoke_duration = 3
		self.cd = 3
		
		self.hero = hero
		self.model = model
		self.cd_left = 0
		self.available = 1
		self.object = 'tile'
		
	def use(self):
		self.model.skill_use = self
	
	def end_cast(self, tile):
		tile.smoke = self.smoke_duration
		self.hero.turnav = self.hero.turnav - 1
		self.cd_left = self.cd
		self.available = 0
		self.model.skill_use = 0
	
	def next_turn(self):
		if self.cd_left:
			self.cd_left = self.cd_left - 1
			if self.cd_left == 0:
				self.available = 1
				
	def cancel(self):
		self.model.skill_use = 0
		
Skills = {'warrior_1': Weapon_improve, 'wizard_1': Clairvoyance,
		  'priest_1': Flash_heal, 'rogue_1': Smoke}
