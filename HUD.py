

from __future__ import division, print_function, unicode_literals
import six

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pyglet
from pyglet.gl import *
from pyglet import image

from cocos.director import *
from cocos.layer import *
from cocos.sprite import Sprite

from const import *

import random
				
class Background( Sprite ):
	def __init__(self):
		w, h = director.get_window_size()
		sc = 1920/w
		super( Background, self ).__init__(pyglet.resource.image('Background.png'), (w/2, h/2), scale = 1/sc)


class Coin (Layer):
	def __init__(self):
		super(Coin, self).__init__()
		w, h = director.get_window_size()
		sc = 1920/w
		self.coins = [pyglet.resource.image('coins/coin%s.png' %  coin_image) for coin_image in range(Coin_image_number)]
		self.coin_anim  = pyglet.image.Animation.from_image_sequence(self.coins, 0.1, True)
		self.coin = Sprite(self.coin_anim, (w - 300//sc, h - 50//sc), scale = 1/sc)
	def draw(self):
		self.coin.draw()		
	
class HUD_DM(Layer):
	def __init__(self):
		
		super( HUD_DM, self).__init__()
		#self.add( Background(), z = 0 )
		self.add( Coin(), z = 2 )
		
class HUD_P(Layer):
	def __init__(self):
		
		super( HUD_P, self).__init__()
		#self.add( Background(), z = 0 )