from __future__ import division, print_function, unicode_literals

Quad_side = 11
Icon_size = 100
Button_size = 75
Coin_image_number = 12
Tile_size = 75
left_space = 140
screen_scale = 1
B_Menu_size = 120
B_object_size = 100

adject_tiles = [(1, 0), (-1, 0), (0, 1), (0, -1)]
tile_names = ['floor', 'lava', 'wall', 'orc', 'treasure']
hero_stat = ['health', 'int', 'exp']
heroes = ['wizard', 'priest', 'warrior', 'rogue']
ExpNeed = [0, 30, 80, 180]
maxlvl = 3

Tech_stat = {
			'wizard': {'speed': 1, 'maxhp': 100},
			'priest': {'speed': 1, 'maxhp': 100},
			'warrior': {'speed': 1, 'maxhp': 140},
			'rogue': {'speed': 2, 'maxhp': 80}
			}

Artefacts = ['mage_wand', 'aqua_shield', 'bandit_sword',
			'black_mask', 'crystal_dagger', 'frost_staff', 
			'glory_cloak', 'katana_sword', 'mage_hat',
			'priest_robe', 'redking_amulet', 'redking_belt',
			'redking_hat', 'rogue_knife', 'royal_ring',
			'sharp_ring', 'speed_boots', 'holy_wand',
			'redking_boots', 'flame_sword']
art_pos = [94 + 75/2, 174 + 75/2, 253 + 75/2, 331 + 75/2, 410 + 75/2]


Traps = ['lava']
Monsters = []
#Monsters = ['orc', 'orc']
Magic = ['curse']
Walls = ['wall', 'floor']

Object_list = {'trap': Traps, 'monster': Monsters, 'magic': Magic, 'wall': Walls}

#B_menu parametrs
m_a = 100
m_b = 20
m_c = 95
#scroll (1175 - 1825); (115 - 645)

luck_per_tile = 50
lava_damage = 20