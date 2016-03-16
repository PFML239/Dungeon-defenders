from __future__ import division, print_function, unicode_literals
import six

import sys
import os

class Controler():
	def __init__(self, model):
		self.model = model
	
	def damage_hero(self, name, damage):
		self.hero = self.model.heroes[name]
		self.hero.stats.health = self.hero.stats.health - damage
		self.model.interface_DM.portraits[name].reload(self.model, name)
		if (self.hero.stats.health <= 0):
			if (self.hero.alive):
				self.hero.alive = 0
				self.model.alive_heroes.remove(self.hero.name)
				self.model.on_gameover()
		