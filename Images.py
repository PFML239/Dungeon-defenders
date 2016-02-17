from __future__ import division, print_function, unicode_literals

import pyglet

class Images(object):
	
	Tile_images = ['red', 'floor']
	greytile = pyglet.resource.image('tiles/block_black.png')
	floortile = pyglet.resource.image('tiles/block_floor.png')
	image = {tile: pyglet.resource.image('tiles/block_%s.png' %tile) for tile in Tile_images}
	frame_yellow = pyglet.resource.image('frame_yellow.png')
	frame_blue = pyglet.resource.image('frame_blue.png')
	
	Hero_names_images = ['wizard', 'rogue', 'priest', 'warrior']
	heroes = {hero_name: pyglet.resource.image('heroes/%s.png' %hero_name) for hero_name in Hero_names_images}
	portraits = {hero_name: pyglet.resource.image('heroes/%s_portrait.png' %hero_name) for hero_name in Hero_names_images}
	hero_icons = {hero_name: pyglet.resource.image('heroes/%s_icon.png' %hero_name) for hero_name in Hero_names_images}