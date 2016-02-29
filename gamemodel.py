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
from magic import DM_Magic
from artefacts import ArtEffects

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
		
		sc = 1920//w
		
		self.interface_DM = Interface(self)
		
		self.heroes = {}
		self.heroes['wizard'] = Hero('wizard', 0, self, 0, (Quad_side - 1)/2)
		self.heroes['priest'] = Hero('priest', 1, self, (Quad_side - 1)/2, Quad_side - 1)
		self.heroes['warrior'] = Hero('warrior', 2, self, Quad_side - 1, (Quad_side - 1)/2)
		self.heroes['rogue'] = Hero('rogue', 3, self, (Quad_side - 1)/2, 0)
		
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
		sc = 1920/w
		for i in range (self.mapx):
			for j in range (self.mapy):
				self.map[(i, j)] = Tile(Images.floortile, ((2*i + 1)*Tile_size/2 + left_space)//sc, 
										((2*j + 1)*Tile_size/2 + (h*sc - (Quad_side*Tile_size))/2)//sc, i, j)
	
	
	def on_gameover(self):
		
		if (len(self.alive_heroes) == 0):
			self.dispatch_event("on_game_over")
			

		
class Tile():

	def __init__(self, image, posx, posy ,map_posx, map_posy):
		w, h = director.get_window_size()
		sc = 1920/w
		self.namenumber = 0
		self.name = 'floor'
		self.map_pos_x = map_posx
		self.map_pos_y = map_posy
		self.open_P = 0
		self.sprite = Sprite(Images.tile_image[self.name], (posx, posy), scale = 1/sc)
	
	def on_click_P(self):
		self.open_P = 1
	
	def draw(self):
		self.sprite.image = Images.tile_image[self.name]
		self.sprite.draw()

class Interface(Layer):
	def __init__(self, model):
		self.model = model
		self.portrait = Hero_portriat_DM('wizard')
		
	def draw(self):
		self.portrait.draw()
		
class BuildingMenu(Layer):

	def __init__(self): 
		super(BuildingMenu, self).__init__()
		self.end_of_init()
		
	def end_of_init(self):
		w, h = director.get_window_size()		
		sc = 1920//w
		self.visible = 0
		self.b_types = {}
		self.b_types[0] = SecondB_menu('trap', 0)
		self.b_types[1] = SecondB_menu('monster', 1)
		self.b_types[2] = SecondB_menu('magic', 2)
		self.b_types[3] = SecondB_menu('wall', 3)
		self.scroll = Sprite(Images.menu_scroll, (1500//sc, 380//sc), scale = 1/sc)
		self.active = -1
	
	def draw(self):
		if self.visible:
			w, h = director.get_window_size()		
			sc = 1920//w
			self.scroll.draw()
			for b_type in self.b_types:
				self.b_types[b_type].sprite.draw()
				if self.active == b_type:
					self.b_types[b_type].draw()
			

class SecondB_menu(Layer):
	
	def __init__(self, name, number):
		super(SecondB_menu, self).__init__()
		w, h = director.get_window_size()		
		sc = 1920//w
		self.name = name
		self.number = number
		self.sprite = Sprite(Images.building_menu[self.name], (1100//sc, (580 - self.number*B_Menu_size*1.1)//sc), scale = 1/sc)
		self.objects = Object_list[self.name]
	
	def draw(self):
		w, h = director.get_window_size()
		sc = 1920//w
		c = Sprite(Images.frame_red, (1100//sc, (580 - self.number*B_Menu_size*1.1)//sc), scale = 1/sc)
		c.draw()
		for object in range(len(self.objects)):
			dx, dy = self.get_coordinates(object)
			c = Sprite(Images.B_images[self.name][object],
						((1315 + dx)//sc, (505 + dy)//sc), scale = 1/sc)
			c.draw()
	
	def get_coordinates(self, number):
		x = number%4
		y = number//4
		dx = x*(m_a+ m_b) 
		dy = -y*(m_a+ m_b)
		return(dx, dy)
		
class Magic():
	def __init__(self, name, model):
		self.name = name
		self.model = model
	def cast(self):
		spell = DM_Magic[self.name]
		spell.cast(self.model)
		
class Hero_portriat_DM():
	def __init__(self, hero_name):
		w, h = director.get_window_size()
		sc = 1920/w
		self.name = hero_name
		self.sprite = Sprite(Images.hero_icons[self.name], (1600//sc, 900//sc), scale = 1/sc)
	def draw(self):
		self.sprite.draw()
		
		
class Hero():

	def __init__(self, name, number ,model, map_posx, map_posy):
		w, h = director.get_window_size()
		sc = 1920/w
		self.name = name
		self.number = number
		self.map_posx = map_posx
		self.map_posy = map_posy
		self.sprite = Sprite(Images.heroes[self.name], scale = 1/sc)
		self.sprite.position = (((2*self.map_posx + 1)*Tile_size/2 + left_space)//sc, ((2*self.map_posy + 1)*Tile_size/2 + (h*sc - Quad_side*Tile_size)/2)//sc)
		self.portrait = Portraits(self)
		self.icon = Icons(self)
		
		self.alive = 1
		self.techstats = Tech_Stats(self.name)
		self.stats = Stats()
		self.staff = []
		self.av_art = list(Artefacts)
		self.model = model
		self.turnav = self.techstats.speed
		self.stats.health = self.techstats.max_health
	
	def replace_hero(self, map_posx, map_posy):
		w, h = director.get_window_size()
		sc = 1920/w
		self.map_posx = map_posx
		self.map_posy = map_posy
		self.sprite.position = (((2*self.map_posx + 1)*Tile_size/2 + left_space)//sc, ((2*self.map_posy + 1)*Tile_size/2 + (h*sc - Quad_side*Tile_size)/2)//sc)
	
	def on_turn(self, tile):
		self.turnav = self.turnav - 1
		if (tile.name == 'lava'):
			self.stats.health = self.stats.health - 50
		if (tile.name != 'wall'):
			self.replace_hero(tile.map_pos_x, tile.map_pos_y)
				
		if (tile.open_P == 0):
			self.stats.exp = self.stats.exp + self.techstats.exppertile
			if self.stats.lvl < maxlvl:
				if (self.stats.exp >= ExpNeed[self.stats.lvl]):
					self.stats.lvl = self.stats.lvl + 1
					self.stats.exp = 0
			if (tile.name == 'floor'):	
				self.stats.luck = self.stats.luck + 120
				if self.stats.luck >= 100:
					self.stats.luck = 0
					if (len(self.staff) < 5):
						art_name = self.av_art[random.randint(0, len(self.av_art) - 1)]
						art = Artefact(art_name, len(self.staff))
						self.av_art.remove(art_name)
						self.staff.append(art)
						art.on_get(self)
					
		if (self.stats.health <= 0):
			if (self.alive):
				self.alive = 0
				self.model.alive_heroes.remove(self.name)
				self.model.on_gameover()
				
	def draw(self):
		self.sprite.draw()
		self.icon.draw()
		
class Artefact():
	def __init__(self, name, number):
		w, h = director.get_window_size()
		sc = 1920/w
		self.name = name
		self.number = number
		self.sprite = Sprite(Images.art_image[self.name], ((1562 + 75/2)//sc, (899 - art_pos[self.number])//sc), scale = 1/sc)
	
	def on_get(self, hero):
		if (ArtEffects.get(self.name)):
			ArtEffects[self.name].effect(hero)
	
	def draw(self):
		self.sprite.draw()
		
class Tech_Stats():
	def __init__(self, hero_name):
		self.speed = Tech_stat[hero_name]['speed']
		self.max_health = Tech_stat[hero_name]['maxhp']
		self.exppertile = 10
			
class Stats():
	def __init__(self):
		self.exp = 0
		self.int = 0
		self.health = 0
		self.lvl = 1
		self.luck = 0

class HeroStats(Label):
	def __init__(self, hero):
		w, h = director.get_window_size()
		sc = 1920/w
		self.hero = hero
		self.health_label = Label('%d' %self.hero.stats.health, font_name='Times New Roman', font_size=28//sc, anchor_x='center', anchor_y='center', color = (255, 0, 0, 255) )
		self.health_label.position = 1300//sc, 315//sc
		self.exp_label = Label('%d' %self.hero.stats.exp, font_name='Times New Roman', font_size=28//sc, anchor_x='center', anchor_y='center', color = (255, 0, 0, 255) )
		self.exp_label.position = 1300//sc, 155//sc
		self.luck_label = Label('%d%%' %self.hero.stats.luck, font_name='Times New Roman', font_size=28//sc, anchor_x='center', anchor_y='center', color = (255, 0, 0, 255) )
		self.luck_label.position = 1300//sc, 245//sc
		self.lvl_label = Label('%d' %self.hero.stats.lvl, font_name='Times New Roman', font_size=18//sc, anchor_x='center', anchor_y='center', color = (0, 0, 0, 255) )
		self.lvl_label.position = 1618//sc, 112//sc

	def draw(self):
		self.health_label.draw()
		self.lvl_label.draw()
		self.exp_label.draw()
		self.luck_label.draw()
		
class Portraits():

	def __init__(self, hero):
		self.hero = hero
	
	def draw(self):
		w, h = director.get_window_size()
		sc = 1920/w
		c = Sprite(Images.portraits[self.hero.name], (1400//sc, 480//sc), scale = 1/sc)
		c.draw()
		c = HeroStats(self.hero)
		c.draw()
		for art in self.hero.staff:
			art.draw()
	
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
		w, h = director.get_window_size()
		sc = 1920/w
		if (self.hero.turnav > 0):
			c = Sprite(Images.hero_icons[self.hero.name], ((1235 + Icon_size*self.number*1.1)//sc, 960//sc), scale = 1/sc)
		else:
			c = Sprite(Images.hero_icons_black[self.hero.name], ((1235 + Icon_size*self.number*1.1)//sc, 960//sc), scale = 1/sc)
		c.draw()
		
GameModel.register_event_type('on_game_over')