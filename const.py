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
tile_names = ['floor', 'lava', 'wall', 'treasure', 'orc_weak', 'orc_strong', 'smoke']
hero_stat = ['health', 'int', 'exp']
heroes = ['wizard', 'priest', 'warrior', 'rogue']
ExpNeed = [0, 30, 80, 180]
maxlvl = 3

Tech_stat = {
			'wizard': {'speed': 1, 'maxhp': 100, 'attack': 30, 'armor': 30},
			'priest': {'speed': 1, 'maxhp': 100, 'attack': 30, 'armor': 30},
			'warrior': {'speed': 1, 'maxhp': 140, 'attack': 30, 'armor': 30},
			'rogue': {'speed': 2, 'maxhp': 80, 'attack': 30, 'armor': 30}
			}

Artefacts = ['mage_wand', 'aqua_shield', 'bandit_sword',
			'black_mask', 'crystal_dagger', 'frost_staff', 
			'glory_cloak', 'katana_sword', 'mage_hat',
			'priest_robe', 'redking_amulet', 'redking_belt',
			'redking_hat', 'rogue_knife', 'royal_ring',
			'sharp_ring', 'speed_boots', 'holy_wand',
			'redking_boots', 'flame_sword']

Skills = ['warrior_1', 'wizard_1', 'priest_1', 'rogue_1']
			
			
Wizard_skills = [('wizard_1', 0)]			
Priest_skills = [('priest_1', 0)]
Warrior_skills = [('warrior_1', 0)]
Rogue_skills = [('rogue_1', 0)]

Hero_skills = {'wizard': Wizard_skills, 'priest' : Priest_skills, 'warrior': Warrior_skills, 'rogue': Rogue_skills}

art_pos = [94 + 75/2, 174 + 75/2, 253 + 75/2, 331 + 75/2, 410 + 75/2]
skill_pos = [95 + 75/2, 174 + 75/2, 252 + 75/2, 331 + 75/2, 410 + 75/2]

Traps = ['lava']
#Monsters = []
Monsters = ['orc']
Magic = ['curse']
Walls = ['wall', 'floor']

Object_list = {'trap': Traps, 'monster': Monsters, 'magic': Magic, 'wall': Walls}
Cost_list = {'lava': 100, 'orc': 200, 'wall': 100, 'floor': 0,'curse': 500,}

#B_menu parametrs
m_a = 100
m_b = 20
m_c = 95
#scroll (1175 - 1825); (115 - 645)

luck_per_tile = 50
lava_damage = 20