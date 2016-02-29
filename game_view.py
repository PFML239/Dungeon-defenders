

from __future__ import division, print_function, unicode_literals
import six

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pyglet
from pyglet.gl import *
from pyglet import image
from pyglet.window import key
from pyglet.window import mouse

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
from gamemodel import *

import random

class GameView(Layer):
	
	def __init__(self, model):
		super(GameView, self).__init__()
		self.mapx = Quad_side
		self.mapy = Quad_side
		self.model = model
		self.end_of_init(model)
		self.cheat = 0
		
	def end_of_init(self, model):	
		self.model.push_handlers(self.on_game_over)
		self.PView = GameView_P(model)
		self.DMView = GameView_DM(model)
		self.curr_player = self.DMView
		self.add(self.curr_player)
	
	def on_game_over(self):
		game_over = GameOver()
		self.add(game_over)
				
	def next_turn(self):
		if (self.curr_player == self.PView):
			self.remove(self.PView)
			self.add(self.DMView)
			self.curr_player = self.DMView
		elif(self.curr_player == self.DMView):
			self.remove(self.DMView)
			self.add(self.PView)
			self.curr_player = self.PView
			
			
class GameView_DM(GameView):
	
	is_event_handler = True	
	
	def end_of_init(self, model):
		self.HUD = HUD_DM()
		self.add(Buttons())
		self.building_menu = BuildingMenu()
		self.add(self.HUD, z = -1)
		self.act_tile = 0
	
	def reload(self):
		self.act_tile = 0
		self.building_menu = BuildingMenu()
		self.building_menu.visible = 0
		self.building_menu.active = -1
		
	def draw(self):
		w, h = director.get_window_size()
		sc = 1920/w
		
		#Actual square drawing
		if (self.act_tile):
			c = Sprite(self.act_tile.sprite.image, (1320//sc, 830//sc), scale = 3.5/sc)
			c.draw()
			
		#map drawing
		for i in range(self.mapx):
			for j in range (self.mapy):
				c = self.model.map.get((i, j))
				c.draw()
				
				#Drawing blue frames for opened tiles
				if (c.open_P == 1):
					Sprite(Images.frame_blue, (((2*i + 1)*Tile_size/2 + left_space)//sc,
												(2*j + 1)*Tile_size/2//sc + (h - Quad_side*Tile_size//sc)/2), scale= 1/sc).draw()
					
		#Drawing heroes
		for hero_name in self.parent.model.heroes:
			hero = self.parent.model.heroes[hero_name]
			if (hero.alive):
				hero.sprite.draw()
		
		if (self.act_tile):
			i, j = self.act_tile.map_pos_x, self.act_tile.map_pos_y
			Sprite(Images.frame_yellow, (((2*i + 1)*Tile_size/2 + left_space)//sc,
										(2*j + 1)*Tile_size/2//sc + (h - Quad_side*Tile_size//sc)/2), scale = 1/sc).draw()
		
		self.model.interface_DM.draw()
		
		if (self.act_tile):
			if (self.act_tile.open_P == 0):
				self.building_menu.draw()
			
	
	def on_key_release(self, keys, modifiers):
		
		turn = 0
		if (self.act_tile):
			x = self.act_tile.map_pos_x
			y = self.act_tile.map_pos_y
			i, j = x, y
			turn = 0
			if (keys == key.LEFT and (x - 1) >= 0):
				i, j = x - 1, y
				turn = 1
			if (keys == key.RIGHT and (x + 1) < Quad_side):
				i, j = x + 1, y
				turn = 1
			if (keys == key.UP and (y + 1) < Quad_side):
				i, j = x, y + 1
				turn = 1
			if (keys == key.DOWN and (y - 1) >= 0):
				i, j = x, y - 1
				turn = 1
		
		if (turn == 1):
			self.act_tile = self.model.map.get((i, j)) 
		
		if (keys == key.ENTER):
			self.parent.next_turn()
			self.parent.curr_player.reload()
	
	def on_mouse_release(self, x, y, buttons, modifiers):
		w, h = director.get_window_size()
		sc = 1920/w
		
		mouse_x, mouse_y = director.get_virtual_coordinates(x, y)
		if (buttons == mouse.LEFT):
			i = (mouse_x*sc - left_space)//Tile_size
			j = (mouse_y*sc - (h*sc - Quad_side*Tile_size)/2)//Tile_size
			
			#Checking that tile is on the map
			if (i >= 0) and (j >= 0) and (i < self.mapx) and (j < self.mapy):
				c = self.parent.model.map.get((i, j))
				if (c.open_P == 0):	
					self.building_menu.visible = 1
				else:
					self.building_menu.visible = 0
				#Actual tile square update
				self.act_tile = c
		
			#Reaction on next turn button  click		
			elif (mouse_x <= w) and (mouse_x >= w - Button_size//sc) and (mouse_y >= 0) and (mouse_y <= Button_size//sc):
				self.parent.next_turn()
				self.parent.curr_player.reload()
			
			elif self.building_menu.visible:
				if (mouse_x <= (1100 + B_Menu_size/2)//sc) and (mouse_x >= (1100 - B_Menu_size/2)//sc):
					if (mouse_y*sc >= 184 - B_Menu_size/2) and (mouse_y*sc <= 184 + 0*B_Menu_size*1.1 + B_Menu_size/2):
						self.building_menu.active = 3
					elif (mouse_y*sc >= 316 - B_Menu_size/2) and (mouse_y*sc <= 184 + 1*B_Menu_size*1.1 + B_Menu_size/2):
						self.building_menu.active = 2
					elif (mouse_y*sc >= 468 - B_Menu_size/2) and (mouse_y*sc <= 184 + 2*B_Menu_size*1.1 + B_Menu_size/2):
						self.building_menu.active = 1			
					elif (mouse_y*sc >= 580 - B_Menu_size/2) and (mouse_y*sc <= 184 + 3*B_Menu_size*1.1 + B_Menu_size/2):
						self.building_menu.active = 0
					else:
						self.act_tile = 0
						self.building_menu.visible = 0
				elif (mouse_x*sc <= 1825) and (mouse_x*sc >= 1175) and (mouse_y*sc <= 645) and (mouse_y*sc >= 115):
					mouse_scroll_x = mouse_x - 1175//sc
					mouse_scroll_y = mouse_y - 115//sc
					i = (mouse_scroll_x*sc - m_c)//(m_a + m_b)
					j = (mouse_scroll_y*sc - m_c)//(m_a + m_b)
					if(mouse_scroll_x*sc <= m_c + i*(m_a + m_b) + m_a) and (mouse_scroll_y*sc <= m_c + j*(m_a + m_b) + m_a):
						number = int(i + (2 - j)*4)
						if (self.building_menu.active != -1) and (self.act_tile.open_P == 0) and (self.building_menu.active != 2):
							name = self.building_menu.b_types[self.building_menu.active].objects[number]
							self.model.map[(self.act_tile.map_pos_x, self.act_tile.map_pos_y)].name = name
						if (self.building_menu.active != -1) and (self.building_menu.active == 2):
							name = self.building_menu.b_types[self.building_menu.active].objects[number]
							spell = Magic(name, self.model)
							spell.cast()
				else:
					self.act_tile = 0
					self.building_menu.visible = 0
			else:
				self.act_tile = 0
				self.building_menu.visible = 0
		else:
			self.act_tile = 0
			self.building_menu.visible = 0
			
class GameView_P(GameView):
	
	is_event_handler = True	
	
	def end_of_init(self, model):
		self.HUD = HUD_P()
		self.add(Buttons())
		self.add(self.HUD, z = -1)
		self.alive_heroes = ['wizard', 'priest', 'warrior', 'rogue']
		self.hero_number = 0
		self.actual_hero = self.model.heroes[self.alive_heroes[self.hero_number]]
		
	def reload(self):
		check = 0
		for hero_name in self.parent.model.heroes:
			hero = self.parent.model.heroes[hero_name]
			if (hero.alive):
				hero.turnav = hero.techstats.speed
				check = 1
		self.hero_number = 0
		self.actual_hero = self.model.heroes['wizard']
		if check:
			self.next_hero(1)
	
	def draw(self):
		w, h = director.get_window_size()
		sc = 1920/w
		#Drawing the map
		for i in range(self.mapx):
			for j in range (self.mapy):			
				c = self.parent.model.map.get((i, j))
				#Checking that tile have been opened
				if (c.open_P == 1):
					c.draw()
				elif (c.open_P == 0):
					greytile = Sprite(Images.greytile, c.sprite.position, scale = 1/sc)
					greytile.draw()
		
		#Drawing heroes
		for hero_name in self.parent.model.heroes:
			hero = self.parent.model.heroes[hero_name]
			#print(hero.name)
			if (hero.alive):
				hero.draw()
		
		hero = self.actual_hero
		if (hero.alive):
			hero.portrait.draw()
		
		#Drawing blue frames for available turns
		if (hero.turnav) or (self.cheat):
			for dx, dy in adject_tiles:
				i = hero.map_posx + dx
				j = hero.map_posy + dy
				if (i >= 0) and (j >= 0) and (i < self.mapx) and (j < self.mapy):
					Sprite(Images.frame_blue, (((2*i + 1)*Tile_size/2 + left_space)//sc,
					(2*j + 1)*Tile_size/2//sc + (h - Quad_side*Tile_size//sc)/2), scale = 1/sc).draw()
	
	def on_key_release(self, keys, modifiers):
		hero = self.actual_hero
		x = hero.map_posx
		y = hero.map_posy
		i, j = x, y
		avturn = 0
		if (keys == key.LEFT and (x - 1) >= 0):
			i, j = x - 1, y
			avturn = 1
		if (keys == key.RIGHT and (x + 1) < Quad_side):
			i, j = x + 1, y
			avturn = 1
		if (keys == key.UP and (y + 1) < Quad_side):
			i, j = x, y + 1
			avturn = 1
		if (keys == key.DOWN and (y - 1) >= 0):
			i, j = x, y - 1
			avturn = 1
		if (avturn == 1):
			if (hero.turnav) or (self.cheat):
				c = self.parent.model.map.get((i, j))
				hero.on_turn(c)
				c.on_click_P()
				if len(self.model.alive_heroes) and (hero.turnav <= 0 or hero.alive == 0):
					self.hero_number = (self.hero_number + 1) %len(self.model.alive_heroes)
					if (hero.alive == 0):
						self.hero_number = (self.hero_number - 1) %len(self.model.alive_heroes)
					self.actual_hero = self.model.heroes[self.model.alive_heroes[self.hero_number]]
					self.next_hero(1)
			else:
				self.label = Message('You have made a turn with this hero already')
				self.add(self.label.label)
				self.label.label.do(FadeIn(0) + Delay(3) + FadeOut(1))
				
		if (keys == key.C):
			self.cheat = 1
			
		if (keys == key.Q):
			#print(1)
			self.hero_number = (self.hero_number - 1) %len(self.model.alive_heroes)
			self.actual_hero = self.model.heroes[self.model.alive_heroes[self.hero_number]]
			self.next_hero(-1)
			
		if (keys == key.E):
			self.hero_number = (self.hero_number + 1) %len(self.model.alive_heroes)
			self.actual_hero = self.model.heroes[self.model.alive_heroes[self.hero_number]]
			self.next_hero(1)
		
		if (keys == key.ENTER):
			self.parent.next_turn()
			self.parent.curr_player.reload()
		
	def on_mouse_release(self, x, y, buttons, modifiers):
		w, h = director.get_window_size()
		sc = 1920/w
		mouse_x, mouse_y = director.get_virtual_coordinates(x, y)
		hero = self.actual_hero
		
		if (buttons == mouse.LEFT):
			i = (mouse_x*sc - left_space)//Tile_size
			j = (mouse_y*sc - (h*sc - Quad_side*Tile_size)/2)//Tile_size
			#Checking that tile is on the map
			if (i >= 0) and (j >= 0) and (i < self.mapx) and (j < self.mapy):
				if ((abs(hero.map_posx - i) + abs(hero.map_posy - j) == 1)):
					if (hero.turnav) or (self.cheat):
						c = self.parent.model.map.get((i, j))
						c.on_click_P()
						hero.on_turn(c)
						if len(self.model.alive_heroes) and (hero.turnav <= 0 or hero.alive == 0):
							self.hero_number = (self.hero_number + 1) %len(self.model.alive_heroes)
							if (hero.alive == 0):
								self.hero_number = (self.hero_number - 1) %len(self.model.alive_heroes)
							self.actual_hero = self.model.heroes[self.model.alive_heroes[self.hero_number]]
							#print(self.actual_hero.name)
							self.next_hero(1)
					else:
						self.label = Message('You have made a turn with this hero already')
						self.add(self.label.label)
						self.label.label.do(FadeIn(0) + Delay(3) + FadeOut(1))
				else:
					#Message about unavaileble turn
					self.label = Message('You must choose an adjective room to the current one')
					self.add(self.label.label)
					self.label.label.do(FadeIn(0) + Delay(3) + FadeOut(1))
			
			#Reaction on next turn button  click
			if (mouse_x <= w) and (mouse_x >= w - Button_size//sc) and (mouse_y >= 0) and (mouse_y <= Button_size//sc):
				self.parent.next_turn()
				self.parent.curr_player.reload()
			
			if (mouse_y <= 1010//sc) and (mouse_y >= 910//sc):				
				if (mouse_x*sc >= 1235 - Icon_size/2) and (mouse_x*sc <= 1235 + 0*Icon_size*1.1 + Icon_size/2) and (self.model.heroes['wizard'].alive):
					self.actual_hero = self.model.heroes['wizard']
				if (mouse_x*sc >= 1345 - Icon_size/2) and (mouse_x*sc <= 1235 + 1*Icon_size*1.1 + Icon_size/2) and (self.model.heroes['priest'].alive):
					self.actual_hero = self.model.heroes['priest']
				if (mouse_x*sc >= 1455 - Icon_size/2) and (mouse_x*sc <= 1235 + 2*Icon_size*1.1 + Icon_size/2) and (self.model.heroes['warrior'].alive):
					self.actual_hero = self.model.heroes['warrior']					
				if (mouse_x*sc >= 1565 - Icon_size/2) and (mouse_x*sc <= 1235 + 3*Icon_size*1.1 + Icon_size/2) and (self.model.heroes['rogue'].alive):
					self.actual_hero = self.model.heroes['rogue']
	
	def next_hero(self, direction):
		iteration = 0
		while ((self.actual_hero.turnav <= 0) or (self.actual_hero.alive == 0)) and (iteration < 5) and (self.cheat == 0):
			self.hero_number = (self.hero_number + direction) %len(self.model.alive_heroes)
			self.actual_hero = self.model.heroes[self.model.alive_heroes[self.hero_number]]
			iteration = iteration + 1
		if iteration == 5:
			self.parent.next_turn()
			self.parent.curr_player.reload()

			
		
class Message(Layer):

	def __init__(self, text_title):		
		super(Message, self).__init__()
		w, h = director.get_window_size()
		sc = 1920/w
		self.label = Label(text_title, font_name='Times New Roman', font_size=28//sc, anchor_x='center', anchor_y='center', color = (255, 0, 0, 255))
		self.label.position = Quad_side*Tile_size/2//sc + left_space//sc, (h - Quad_side*Tile_size//sc)/4			
	
class Buttons (Layer):
	
	def __init__(self):
		super(Buttons, self).__init__()
		w, h = director.get_window_size()
		sc = 1920/w
		self.img = pyglet.resource.image('next_turn.png')
		w, h = director.get_window_size();
		self.nextturn_button = Sprite(self.img, (w - Button_size/2//sc, Button_size/2//sc), scale = 1/sc)
	
	def draw ( self ):
		self.nextturn_button.draw()

		
class GameOver(ColorLayer):
	
	is_event_handler = True	
	
	def __init__( self, win = False):
		super(GameOver,self).__init__( 32,32,32,64)

		w,h = director.get_window_size()

		label = Label('Game Over', font_name='Edit Undo Line BRK', font_size=54, anchor_y='center', anchor_x='center' )
		label.position =  ( w/2.0, h/2.0 )
		self.add( label )
	
	def on_mouse_release(self, x, y, buttons, modifiers):
		director.pop()
	def on_key_release(self, keys, modifiers):
		director.pop()
	
def get_newgame_DM():
	gamescene = Scene()
	model = GameModel()
	gamescene.add(GameView(model))
	gamescene.add(Background(), z = -2)
	#gamescene.do(ScaleTo(0.5, 0))
	
	return gamescene