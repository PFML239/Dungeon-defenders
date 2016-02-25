from __future__ import division, print_function, unicode_literals
import six

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from const import *

class Curse():
	def cast(self, model):
		self.model = model
		for hero in self.model.heroes:
			if (self.model.heroes[hero].alive):
				self.model.heroes[hero].stats.health = self.model.heroes[hero].stats.health - 20
				if self.model.heroes[hero].stats.health <= 0:
					self.model.heroes[hero].alive = 0
					self.model.alive_heroes.remove(self.model.heroes[hero].name)
					self.model.on_gameover()

DM_spells = ['curse']
DM_Magic = {'curse' : Curse()}