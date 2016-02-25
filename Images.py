from __future__ import division, print_function, unicode_literals

import pyglet

from const import *

class Images(object):
	
	Tile_images = tile_names
	greytile = pyglet.resource.image('tiles/block_black.png')
	floortile = pyglet.resource.image('tiles/block_floor.png')
	tile_image = {tile: pyglet.resource.image('tiles/block_%s.png' %tile) for tile in Tile_images}
	frame_yellow = pyglet.resource.image('frame_yellow.png')
	frame_blue = pyglet.resource.image('frame_blue.png')
	frame_red = pyglet.resource.image('frame_red.png')
	
	Hero_names_images = ['wizard', 'rogue', 'priest', 'warrior']
	heroes = {hero_name: pyglet.resource.image('heroes/%s.png' %hero_name) for hero_name in Hero_names_images}
	portraits = {hero_name: pyglet.resource.image('heroes/%s_portrait.png' %hero_name) for hero_name in Hero_names_images}
	hero_icons = {hero_name: pyglet.resource.image('heroes/%s_icon.png' %hero_name) for hero_name in Hero_names_images}
	hero_icons_black = {hero_name: pyglet.resource.image('heroes/%s_icon_black.png' %hero_name) for hero_name in Hero_names_images}
	
	b_types_images = ['trap', 'monster', 'magic', 'wall']
	menu_scroll = pyglet.resource.image('menu_scroll.png')
	building_menu = {b_type_image: pyglet.resource.image('b_menu/b_types/%s.png' %b_type_image) for b_type_image in b_types_images}
	
	Trap_images = {type: pyglet.resource.image('b_menu/Traps/%s.png' %Traps[type]) for type in Traps}
	Wall_images = {type: pyglet.resource.image('b_menu/Walls/%s.png' %Walls[type]) for type in Walls}
	Monster_images = {type: pyglet.resource.image('b_menu/Monsters/%s.png' %Monsters[type]) for type in Monsters}
	Magic_images = {type: pyglet.resource.image('b_menu/Magic/%s.png' %Magic[type]) for type in Magic}
	
	
	B_images = {'trap' : Trap_images, 
				'wall' : Wall_images,
				'monster' : Monster_images,
				'magic' : Magic_images}