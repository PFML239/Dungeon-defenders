from __future__ import division, print_function, unicode_literals
import six

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from const import *

class Aqua_Shield():
	def effect(self, hero):
		self.hero = hero
		hero.stats.health = hero.stats.health + 20
		
class Glory_Cloak():
	def effect(self, hero):
		self.hero = hero
		hero.techstats.exppertile = hero.techstats.exppertile*2

class Speed_Boots():
	def effect(self, hero):
		self.hero = hero
		hero.techstats.speed = hero.techstats.speed + 1
		
ArtEffects = {'aqua_shield' : Aqua_Shield(), 'glory_cloak': Glory_Cloak(), 'speed_boots': Speed_Boots()}