from __future__ import division, print_function, unicode_literals
import six

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from const import *

class Aqua_Shield():
	def __init__(self, hero):
		self.hero = hero
	def effect(self):
		self.hero.stats.health = self.hero.stats.health + 20
		
class Glory_Cloak():
	def __init__(self, hero):
		self.hero = hero
	def effect(self):
		self.hero.techstats.exppertile = self.hero.techstats.exppertile*2

class Speed_Boots():
	def __init__(self, hero):
		self.hero = hero
	def effect(self):
		self.hero.techstats.speed = self.hero.techstats.speed + 1
		
ArtEffects = {'aqua_shield' : Aqua_Shield, 'glory_cloak': Glory_Cloak, 'speed_boots': Speed_Boots}