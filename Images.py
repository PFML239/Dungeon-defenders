from __future__ import division, print_function, unicode_literals

import pyglet

from const import *

class Images(object):
	
	Tile_images = tile_names
	greytile = pyglet.resource.image('tiles/black.png')
	floortile = pyglet.resource.image('tiles/floor.png')
	art_choise = pyglet.resource.image('art_choise.png')
	tile_image = {tile: pyglet.resource.image('tiles/%s.png' %tile) for tile in Tile_images}
	frame_yellow = pyglet.resource.image('frame_yellow.png')
	frame_blue = pyglet.resource.image('frame_blue.png')
	frame_black = pyglet.resource.image('frame_black.png')
	
	heroes = {hero_name: pyglet.resource.image('heroes/%s.png' %hero_name) for hero_name in heroes}
	portraits = {hero_name: pyglet.resource.image('heroes/%s_portrait.png' %hero_name) for hero_name in heroes}
	hero_icons = {hero_name: pyglet.resource.image('heroes/%s_icon.png' %hero_name) for hero_name in heroes}
	hero_icons_black = {hero_name: pyglet.resource.image('heroes/%s_icon_black.png' %hero_name) for hero_name in heroes}
	
	art_image = {art: pyglet.resource.image('artefacts/%s.png' %art) for art in Artefacts}
	skill_image = {skill: pyglet.resource.image('skills/%s.png' %skill) for skill in Skills}
	
	b_types_images = ['trap', 'monster', 'magic', 'wall']
	menu_scroll = pyglet.resource.image('menu_scroll.png')
	building_menu = {b_type_image: pyglet.resource.image('b_menu/b_types/%s.png' %b_type_image) for b_type_image in b_types_images}
	
	Trap_images = {type: pyglet.resource.image('b_menu/Traps/%s.png' %Traps[type]) for type in range(len(Traps))}
	Wall_images = {type: pyglet.resource.image('b_menu/Walls/%s.png' %Walls[type]) for type in range(len(Walls))}
	Monster_images = {type: pyglet.resource.image('b_menu/Monsters/%s.png' %Monsters[type]) for type in range(len(Monsters))}
	Magic_images = {type: pyglet.resource.image('b_menu/Magic/%s.png' %Magic[type]) for type in range(len(Magic))}
	
	
	B_images = {'trap' : Trap_images, 
				'wall' : Wall_images,
				'monster' : Monster_images,
				'magic' : Magic_images}