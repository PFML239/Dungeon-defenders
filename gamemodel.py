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
from Skills import Skills
from monsters import DM_Monsters
from magic import DM_Magic
from artefacts import ArtEffects
from controler import Controler


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
		
		self.heroes = {}
		self.heroes['wizard'] = Hero('wizard', 0, self, 0, 0)
		self.heroes['priest'] = Hero('priest', 1, self, 0, Quad_side - 1)
		self.heroes['warrior'] = Hero('warrior', 2, self, Quad_side - 1, Quad_side - 1)
		self.heroes['rogue'] = Hero('rogue', 3, self, Quad_side - 1, 0)
		self.interface_DM = Interface(self)
		
		self.monsters = []
		self.alive_heroes = ['wizard', 'priest', 'warrior', 'rogue']
		self.actual_hero = ['wizard']
		self.controler = Controler(self)
		self.skill_use = 0
		
		c = self.map.get((0, 0))
		c.open_P = 1
		c = self.map.get((Quad_side - 1, 0))
		c.open_P = 1
		c = self.map.get((Quad_side - 1, Quad_side - 1))
		c.open_P = 1
		c = self.map.get((0, Quad_side - 1))
		c.open_P = 1
		c = self.map.get(((Quad_side - 1)/2, (Quad_side - 1)/2))
		c.name = 'treasure'
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
	
	def on_youwin(self):
		self.dispatch_event("on_you_win")
			

		
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
		self.sprite_smoke = Sprite(Images.tile_image['smoke'], (posx, posy), scale = 1/sc)
		self.monster = 0
		self.smoke = 0
		self.buildav = 1
	
	def next_turn(self):
		if self.smoke:
			self.smoke = self.smoke - 1
	
	def next_turn_DM(self):
		self.buildav = 1
		if (self.open_P) or (self.smoke):
			self.buildav = 0
	
	def on_click_P(self):
		self.open_P = 1
	
	def draw(self):
		self.sprite.image = Images.tile_image[self.name]
		self.sprite.draw()
		if self.smoke:
			self.sprite_smoke.draw()
			

class Interface(Layer):
	def __init__(self, model):
		self.model = model
		self.portraits = {'wizard': Hero_portriat_DM(), 'priest': Hero_portriat_DM(),
						 'warrior': Hero_portriat_DM(),'rogue': Hero_portriat_DM()}
		for c in self.portraits:
			self.portraits[c].reload(model, c)
		self.money = 10000
		
	def draw(self):
		w, h = director.get_window_size()
		sc = 1920/w
		self.label = Label('%d' %self.money, font_name='Times New Roman', font_size=20//sc, anchor_x='center', anchor_y='center', color = (255, 0, 0, 255))
		self.label.position = (1670//sc, 1030//sc)
		self.label.draw()
		for c in self.portraits:
			self.portraits[c].draw()
		
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
		c = Sprite(Images.frame_black, (1100//sc, (580 - self.number*B_Menu_size*1.1)//sc), scale = 1/sc)
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
	def reload(self, model, hero_name):
		w, h = director.get_window_size()
		sc = 1920/w
		self.model = model
		self.name = hero_name
		if self.name == 'wizard':
			self.hero = self.model.heroes[self.name]
			self.sprite = Sprite(Images.hero_icons[self.name], (1600//sc, 900//sc), scale = 1/sc)
			self.sprite_black = Sprite(Images.hero_icons_black[self.name], (1600//sc, 900//sc), scale = 1/sc)
			self.label = Label('%d' %self.hero.stats.health, font_name='Times New Roman', font_size=20//sc, anchor_x='center', anchor_y='center', color = (255, 0, 0, 255) )
			self.label.position = 1600//sc, 870//sc
		if self.name == 'priest':
			self.hero = self.model.heroes[self.name]
			self.sprite = Sprite(Images.hero_icons[self.name], (1720//sc, 900//sc), scale = 1/sc)
			self.sprite_black = Sprite(Images.hero_icons_black[self.name], (1720//sc, 900//sc), scale = 1/sc)
			self.label = Label('%d' %self.hero.stats.health, font_name='Times New Roman', font_size=20//sc, anchor_x='center', anchor_y='center', color = (255, 0, 0, 255) )
			self.label.position = 1720//sc, 870//sc
		if self.name == 'warrior':
			self.hero = self.model.heroes[self.name]
			self.sprite = Sprite(Images.hero_icons[self.name], (1600//sc, 780//sc), scale = 1/sc)
			self.sprite_black = Sprite(Images.hero_icons_black[self.name], (1600//sc, 780//sc), scale = 1/sc)
			self.label = Label('%d' %self.hero.stats.health, font_name='Times New Roman', font_size=20//sc, anchor_x='center', anchor_y='center', color = (255, 0, 0, 255) )
			self.label.position = 1600//sc, 750//sc
		if self.name == 'rogue':
			self.hero = self.model.heroes[self.name]
			self.sprite = Sprite(Images.hero_icons[self.name], (1720//sc, 780//sc), scale = 1/sc)
			self.sprite_black = Sprite(Images.hero_icons_black[self.name], (1720//sc, 780//sc), scale = 1/sc)
			self.label = Label('%d' %self.hero.stats.health, font_name='Times New Roman', font_size=20//sc, anchor_x='center', anchor_y='center', color = (255, 0, 0, 255) )
			self.label.position = 1720//sc, 750//sc
	def draw(self):
		if self.hero.alive:
			self.sprite.draw()
			self.label.font_name = '%d' %self.hero.stats.health
			self.label.draw()
		else:
			self.sprite_black.draw()
		
		
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
		self.stats = Stats(self.name)
		self.staff = []
		self.av_art = list(Artefacts)
		self.model = model
		self.turnav = self.techstats.speed
		self.stats.health = self.techstats.max_health
		self.skills = []
		for s in Hero_skills[self.name]:
			self.skills.append(Skill(s[0], s[1], self, self.model))
	
	def replace_hero(self, map_posx, map_posy):
		w, h = director.get_window_size()
		sc = 1920/w
		self.map_posx = map_posx
		self.map_posy = map_posy
		self.sprite.position = (((2*self.map_posx + 1)*Tile_size/2 + left_space)//sc, ((2*self.map_posy + 1)*Tile_size/2 + (h*sc - Quad_side*Tile_size)/2)//sc)
	
	def on_turn(self, tile):
		self.turnav = self.turnav - 1
		replace_hero = 1
		if (tile.name == 'lava'):
			self.model.controler.damage_hero(self.name, lava_damage)
		if (tile.name == 'wall'):
			replace_hero = 0
		if (tile.monster):
			result = tile.monster.monster.fight(self)
			if result == 'lose':
				replace_hero = 0
		if (tile.open_P == 0):
			self.stats.exp = self.stats.exp + self.techstats.exppertile
			if self.stats.lvl < maxlvl:
				if (self.stats.exp >= ExpNeed[self.stats.lvl]):
					self.stats.lvl = self.stats.lvl + 1
					self.stats.exp = 0
			if (tile.name == 'floor'):	
				self.stats.luck = self.stats.luck + luck_per_tile
				if self.stats.luck >= 100:
					self.stats.luck = 0
					if (len(self.staff) < 5):
						art_name = self.av_art[random.randint(0, len(self.av_art) - 1)]
						art = Artefact(art_name, len(self.staff))
						self.av_art.remove(art_name)
						self.staff.append(art)
						art.on_get(self)
		if replace_hero:
			self.replace_hero(tile.map_pos_x, tile.map_pos_y)
		if (tile.name == 'treasure'):
			self.model.on_youwin()
	
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
		
class Skill():
	def __init__(self, name, number, hero, model):
		w, h = director.get_window_size()
		sc = 1920/w
		self.name = name
		self.number = number
		self.sprite = Sprite(Images.skill_image[self.name], ((1208)//sc, (899 - skill_pos[self.number])//sc), scale = 1/sc)
		self.skill = Skills[self.name](hero , model)
	
	def draw(self):
		w, h = director.get_window_size()
		sc = 1920/w
		self.sprite.draw()
		if self.skill.cd_left:
			self.label = Label('%d' %self.skill.cd_left, font_name='Times New Roman', font_size=20//sc, anchor_x='center', anchor_y='center', color = (255, 0, 0, 255) )
			self.label.position = ((1208)//sc, (899 - skill_pos[self.number])//sc)
			self.label.draw()
	
	def use(self):
		if self.skill.available:
			self.skill.use()
		
class Tech_Stats():
	def __init__(self, hero_name):
		self.speed = Tech_stat[hero_name]['speed']
		self.max_health = Tech_stat[hero_name]['maxhp']
		self.exppertile = 10
			
class Stats():
	def __init__(self, hero_name):
		self.exp = 0
		self.int = 0
		self.health = 0
		self.lvl = 1
		self.luck = 0
		self.attack = Tech_stat[hero_name]['attack']
		self.armor = Tech_stat[hero_name]['armor']
		self.power = self.attack*2 + self.armor

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
		self.attack_label = Label('%d' %self.hero.stats.attack, font_name='Times New Roman', font_size=28//sc, anchor_x='center', anchor_y='center', color = (255, 0, 0, 255) )
		self.attack_label.position = 1550//sc, 315//sc
		self.armor_label = Label('%d' %self.hero.stats.armor, font_name='Times New Roman', font_size=28//sc, anchor_x='center', anchor_y='center', color = (255, 0, 0, 255))
		self.armor_label.position = 1550//sc, 245//sc

	def draw(self):
		self.health_label.draw()
		self.lvl_label.draw()
		self.exp_label.draw()
		self.luck_label.draw()
		self.attack_label.draw()
		self.armor_label.draw()
		
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
		for skill in self.hero.skills:
			skill.draw()
	
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
		
class Monster():
	def __init__(self, model, tile, m_name):
		w, h = director.get_window_size()		
		sc = 1920//w
		self.name = m_name
		self.tile = tile
		self.monster = DM_Monsters[self.name](model, tile)
		
GameModel.register_event_type('on_game_over')
GameModel.register_event_type('on_you_win')