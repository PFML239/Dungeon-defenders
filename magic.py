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
				self.model.controler.damage_hero(self.model.heroes[hero].name, 20)

DM_spells = ['curse']
DM_Magic = {'curse' : Curse()}