

from __future__ import division, print_function, unicode_literals
import six

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from cocos.director import director
from cocos.layer import *
from cocos.scene import Scene
from cocos.scenes.transitions import *
from cocos.actions import *
from cocos.sprite import *
from cocos.menu import *
from cocos.text import *
from HUD import Background

import pyglet
from pyglet import gl, font
from pyglet.window import key

from const import *
				
class MainMenu( Menu ):

	def __init__(self):
		super( MainMenu, self).__init__('Dungeon Master') 
		
		# you can override the font that will be used for the title and the items
		# you can also override the font size and the colors. see menu.py for
		# more info
		self.font_title['font_name'] = 'Edit Undo Line BRK'
		self.font_title['font_size'] = 72//screen_scale
		self.font_title['color'] = (245,184,16,255)

		self.font_item['font_name'] = 'Courier New',
		self.font_item['color'] = (32,16,32,255)
		self.font_item['font_size'] = 40//screen_scale
		self.font_item_selected['font_name'] = 'Courier New'
		self.font_item_selected['color'] = (255, 0, 255,255)
		self.font_item_selected['font_size'] = 54//screen_scale


		# example: menus can be vertical aligned and horizontal aligned
		self.menu_anchor_y = CENTER
		self.menu_anchor_x = CENTER

		items = []

		items.append( MenuItem('New Game', self.on_newgame) )
		items.append( MenuItem('Quit', self.on_quit) )
		
		self.create_menu( items, shake(), shake_back() )

	def on_newgame(self):
		import game_view
		director.push( FadeTransition(
			game_view.get_newgame_DM(), 1.5 ) )
		
	def on_quit(self):
		pyglet.app.exit()
		
if __name__ == "__main__":	
	
	sc = screen_scale
	director.init(width=1920//sc, height=1080//sc, caption="Dungeon master", fullscreen=(sc == 1))
	main_scene = Scene()
	color_layer = Background()
	main_scene.add(MainMenu(), z = 1)
	main_scene.add(color_layer, z = 0)
	director.run(main_scene)
