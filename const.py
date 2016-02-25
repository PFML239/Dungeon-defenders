from __future__ import division, print_function, unicode_literals

Quad_side = 11
Icon_size = 100
Button_size = 75
Coin_image_number = 12
Tile_size = 75
left_space = 140
screen_scale = 2
B_Menu_size = 120
B_object_size = 100

adject_tiles = [(1, 0), (-1, 0), (0, 1), (0, -1)]
tile_names = ['floor', 'lava', 'wall']
hero_stat = ['health', 'int', 'exp']
heroes = ['wizard', 'priest', 'warrior', 'rogue']
ExpNeed = {1: 10, 2: 30, 3: 60}
maxlvl = 3

Traps = {0: 'lava'}
#Traps = {0: 'lava'}
Monsters = {}
Magic = {0: 'curse'}
Walls = {0: 'wall', 1: 'floor'}

Object_list = {'trap': Traps, 'monster': Monsters, 'magic': Magic, 'wall': Walls}

#B_menu parametrs
m_a = 100
m_b = 20
m_c = 95
#scroll (1175 - 1825); (115 - 645)