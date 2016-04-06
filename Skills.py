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
		
		self.lvl = 1
		self.learnt = 1
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
		
		self.lvl = 1
		self.learnt = 1
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
	
		self.lvl = 1
		self.learnt = 1
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
		
		self.lvl = 1
		self.learnt = 1
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

class Check_the_line():
	def __init__(self, hero, model):
	
		self.cd = 3
		
		self.lvl = 2
		self.learnt = 0
		self.hero = hero
		self.model = model
		self.cd_left = 0
		self.available = 1
		self.object = 'tile'
		
	def use(self):
		self.model.skill_use = self
	
	def end_cast(self, tile):
		if (self.hero.map_posx == tile.map_pos_x)^(self.hero.map_posy == tile.map_pos_y):
			if (self.hero.map_posx == tile.map_pos_x):
				dx = 0
				dy = -(self.hero.map_posy - tile.map_pos_y)/abs(self.hero.map_posy - tile.map_pos_y)
			elif (self.hero.map_posy == tile.map_pos_y):
				dx = -(self.hero.map_posx - tile.map_pos_x)/abs(self.hero.map_posx - tile.map_pos_x)
				dy = 0
			x = self.hero.map_posx + dx
			y = self.hero.map_posy + dy
			monster = 0 
			while (x >= 0) and (y >= 0) and (x < Quad_side) and (y < Quad_side) and (monster == 0):
				new_tile = self.model.map.get((x, y))
				if (new_tile.monster):
					new_tile.open_P = 1
					monster = 1
				x = x + dx
				y = y + dy
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
		  'priest_1': Flash_heal, 'rogue_1': Smoke, 'rogue_2' : Check_the_line}
