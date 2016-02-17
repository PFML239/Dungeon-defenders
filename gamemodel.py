from __future__ import division, print_function, unicode_literals
import six

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pyglet
from pyglet.gl import *
from pyglet import image

from cocos.director import *
from cocos.menu import *
from cocos.scene import *
from cocos.layer import *
from cocos.actions import *
from cocos.sprite import Sprite
from cocos.text import Label

from Images import *
from const import *
from HUD import *

import random

class GameModel( pyglet.event.EventDispatcher):

	def __init__(self):
		self.end_of_init()
	def end_of_init(self):
		super(GameModel, self).__init__()
		self.mapx = Quad_side
		self.mapy = Quad_side
		self.init_map()
		w, h = director.get_window_size()
		
		
		self.heroes = {}
		self.heroes['wizard'] = Hero('wizard', self, 0, (Quad_side - 1)/2)
		self.heroes['rogue'] = Hero('rogue', self, (Quad_side - 1)/2, 0)
		self.heroes['priest'] = Hero('priest', self, (Quad_side - 1)/2, Quad_side - 1)
		self.heroes['warrior'] = Hero('warrior', self, Quad_side - 1, (Quad_side - 1)/2)
		self.alive_heroes = ['wizard', 'priest', 'warrior', 'rogue']
		self.actual_hero = ['wizard']
		c = self.map.get((0, (Quad_side - 1)/2))
		c.open_P = 1
		c = self.map.get(((Quad_side - 1)/2, 0))
		c.open_P = 1
		c = self.map.get(((Quad_side - 1)/2, Quad_side - 1))
		c.open_P = 1
		c = self.map.get((Quad_side - 1, (Quad_side - 1)/2))
		c.open_P = 1
		
	def init_map(self):
		self.map = {}
		self.map['actual_tile'] = (-1, -1)
		w, h = director.get_window_size()
		for i in range (self.mapx):
			for j in range (self.mapy):
				self.map[(i, j)] = Tile(Images.floortile, (2*i + 1)*Tile_size/2 + left_space, (2*j + 1)*Tile_size/2 + (h - Quad_side*Tile_size)/2, i, j)
	
	
	def on_gameover(self):
		
		for hero_name in self.heroes:
			if (self.heroes[hero_name].stats.health <= 0):
				self.dispatch_event("on_game_over")
				

class Hero(Sprite):

	def __init__(self, name, model, map_posx, map_posy):
		super(Hero, self).__init__(Images.heroes[name])
		w, h = director.get_window_size()
		self.name = name
		self.map_posx = map_posx
		self.map_posy = map_posy
		self.position = ((2*self.map_posx + 1)*Tile_size/2 + left_space, (2*self.map_posy + 1)*Tile_size/2 + (h - Quad_side*Tile_size)/2)
		self.stats = Stats()
		self.model = model
		self.portrait = Portraits(self)
		self.icon = Icons(self)
	
	def replace_hero(self, map_posx, map_posy):
		w, h = director.get_window_size()
		self.map_posx = map_posx
		self.map_posy = map_posy
		self.position = ((2*self.map_posx + 1)*Tile_size/2 + left_space, (2*self.map_posy + 1)*Tile_size/2 + (h - Quad_side*Tile_size)/2)
	
	def on_tile(self, tilename):
		if (tilename == 'red'):
			self.stats.health = self.stats.health - 20
		if (self.stats.health <= 0):
			self.model.on_gameover()

class Portraits():

	def __init__(self, hero):
		self.hero = hero
	
	def draw(self):
		c = Sprite(Images.portraits[self.hero.name], (1400, 480))
		c.draw()
		c = HeroStats(self.hero)
		c.draw()
	
class Icons():
	
	def __init__(self, hero):
		self.hero = hero
		if self.hero.name == 'wizard':
			self.number = 0
		if self.hero.name == 'priest':
			self.number = 1
		if self.hero.name == 'warrior':
			self.number = 2	
		if self.hero.name == 'rogue':
			self.number = 3
			
	def draw(self):
		c = Sprite(Images.hero_icons[self.hero.name], (1235 + Icon_size*self.number*1.1, 960))
		c.draw()
		
			
class Stats():
	def __init__(self):
		self.exp = 0
		self.int = 0
		self.health = 100

class HeroStats(Label):
	def __init__(self, hero):
		self.hero = hero
		self.health_label = Label('%d' %self.hero.stats.health, font_name='Times New Roman', font_size=28, anchor_x='center', anchor_y='center', color = (255, 0, 0, 255) )
		self.health_label.position = 1300, 315

	def draw(self):
		self.health_label.draw()		
		
class Tile(Sprite):

	def __init__(self, image, posx, posy ,map_posx, map_posy):
		super(Tile, self).__init__(image, (posx, posy))
		self.namenumber = 0
		self.name = 'floor'
		self.map_pos_x = map_posx
		self.map_pos_y = map_posy
		self.open_P = 0
	
	def on_click_DM(self):
		self.namenumber = (self.namenumber + 1) % len(names)
		self.name = names[self.namenumber]
		self.image = Images.image[self.name] 
	
	def on_click_P(self):
		self.open_P = 1
		
GameModel.register_event_type('on_game_over')