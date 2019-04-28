from pyxen import *

import pyxen
import math
import Utils

from Utils import calc_distance, calc_man_distance, calc_orientation

sfx_volume = 0.30

PROP_GENERATOR = 1
PROP_POTION = 2


class Game:
	def __init__(self):
		self.next_id = 1
		self.game_over = False
		self.level_name = "level1"
		self.fade_in_time = 0.0
		self.fade_out_time = 0.0
		self.fade_in = True			# fade in entering the level
		self.fade_out = False		# fade out to next level

		self.scroll_x = 0.0
		self.scroll_y = 0.0

		self.map_cols = 40
		self.map_rows = 30

		self.hero = Hero()
		self.hero.id = self.next_id
		self.next_id += 1

		self.monsters = []
		self.props = []

		self.exit_loc = None

	def enter_level(self, level_name):
		self.level_name = level_name
		log("entering level " + level_name)
		self.monsters = []
		self.props = []

		self.setup_level()
		reset_colliders()
		start_music("LD44")

		self.hero.x = 160.0
		self.hero.y = 160.0

		self.fade_in = True
		self.fade_in_time = 0.0
		self.fade_out = False

		(numcols, numrows) = msize()
		self.map_cols = numcols
		self.map_rows = numrows

		self.focus_on_hero()

	def enter_next_level(self):
		if self.level_name == "level1":
			self.enter_level("shop")
		else:
			self.enter_level("level1")

	def setup_level(self):
		mreset(self.level_name)
		mmap(self.level_name)
		stair_tiles = mfind(8)
		self.exit_loc = stair_tiles[rand(len(stair_tiles))]
		for tile in stair_tiles:
			(col, row) = tile
			if col != self.exit_loc[0] or row != self.exit_loc[1]:
				mset(col, row, 0)

		prop_tiles = mfind(16)
		for tile in prop_tiles:
			(col, row) = tile
			mset(col, row, 0)

		# spawn generators
		nb_generators = len(prop_tiles) // 2
		if self.level_name == "shop":
			nb_generators = 0

		for i in range(0, nb_generators):
			tile = prop_tiles[rand(len(prop_tiles))]
			(col, row) = tile
			self.spawn_prop(PROP_GENERATOR, col * 16, row * 16)
			prop_tiles.remove(tile)

		# spawn potions
		nb_potions = len(prop_tiles) // 2
		if self.level_name == "shop":
			nb_potions = 0

		for i in range(0, nb_potions):
			tile = prop_tiles[rand(len(prop_tiles))]
			(col, row) = tile
			self.spawn_prop(PROP_POTION, col * 16, row * 16)
			prop_tiles.remove(tile)

			
		self.focus_on_hero()

	def draw(self):
		self.draw_map()

		self.hero.draw(self.scroll_x, self.scroll_y)
		for m in self.monsters:
			m.draw(self.scroll_x, self.scroll_y)
		for prop in self.props:
			prop.draw(self.scroll_x, self.scroll_y)

		# Particles
		Utils.draw_particles(self.scroll_x, self.scroll_y)

		if self.game_over:
			self.draw_game_over()
		else:
			self.draw_ui()

		if self.fade_in:
			self.draw_fade_in()
		if self.fade_out:
			self.draw_fade_out()

	def draw_map(self):
		mmap(self.level_name)
		first_col = int(self.scroll_x) // 16
		first_row = int(self.scroll_y) // 16
		mdraw(-self.scroll_x, -self.scroll_y, first_col, first_row, 16+1, 15+1)
		
	def update(self, delta):
		if self.fade_in:
			self.fade_in_time += delta
			if self.fade_in_time >= 2.50:
				self.start_gameplay()

		if self.fade_out:
			self.fade_out_time += delta
			if self.fade_out_time >= 2.50:
				self.enter_next_level()

		if not self.fade_in and not self.fade_out:
			self.update_loop(delta)

	def start_gameplay(self):
		self.fade_in = False
		self.fade_in_time = 0.0

	def update_loop(self, delta):
		if not pyxen.is_playing_music():
			start_music("LD44")	

		mmap(self.level_name)
		self.hero.read_inputs(delta)
		self.hero.update(delta)

		pyxen.reset_colliders()	
		for m in self.monsters:
			m.enable_collider()
		for p in self.props:
			p.enable_collider()

		self.hero.move(delta)

		# did the hero reach exit stairs ?
		exit_hb = (self.exit_loc[0] * 16, self.exit_loc[1] * 16, 16, 16)
		if Utils.rect_intersect(self.hero.hitbox, exit_hb):
			self.hero_reach_exit()

		# after hero move, enable his collider
		self.hero.enable_collider()

		# did the hero walk on a prop
		loots = self.loots_in_rect(self.hero.hitbox)
		for loot in loots:
			self.hero_pickup_loot(loot)

		if btnp(4) and not self.hero.attacking:
			self.hero_attack()

		# move and update monsters
		self.move_monsters(delta)

		# update props
		for prop in self.props:
			prop.update(delta)

		Utils.update_particles(delta)

		self.focus_on_hero()

	def focus_on_hero(self):
		# Update scroll to keep hero on screen
		x_in_screen = self.hero.x - self.scroll_x
		y_in_screen = self.hero.y - self.scroll_y
		if x_in_screen >= 192.0:
			self.scroll_x = self.hero.x - 192.0
		if x_in_screen <= 64.0:
			self.scroll_x = self.hero.x - 64.0
		if y_in_screen >= 176.0:
			self.scroll_y = self.hero.y - 176.0
		if y_in_screen <= 64.0:
			self.scroll_y = self.hero.y - 64.0

		if self.scroll_x < 0.0: 
			self.scroll_x = 0.0
		if self.scroll_x > (self.map_cols * 16 - 256): 
			self.scroll_x = self.map_cols * 16 - 256
		if self.scroll_y < 0.0: 
			self.scroll_y = 0.0
		if self.scroll_y > (self.map_rows * 16 - 240): 
			self.scroll_y = self.map_rows * 16 - 240

	def draw_ui(self):
		x0 = (256 - 5 * 16) // 2
		y0 = 0
		Utils.draw_ui_box(x0, y0, 3)
		Utils.draw_text("LIFE: {0}".format(self.hero.life), x0 + 3, y0 + 3)		
	def draw_fade_in(self):
		txt = "Entering Level"
		w = len(txt) * 8
		x0 = (256 - w) // 2
		y0 = 100
		Utils.draw_ui_box(x0, y0, 1 + (w - 32) // 16)
		Utils.draw_text(txt, x0 + 3, y0 + 3)

	def draw_fade_out(self):
		txt = "Level Finished!"
		w = len(txt) * 8
		x0 = (256 - w) // 2
		y0 = 100
		Utils.draw_ui_box(x0, y0, 1 + (w - 32) // 16)
		Utils.draw_text(txt, x0 + 3, y0 + 3)

	def draw_game_over(self):
		w = 21 * 8
		x0 = (256 - w) // 2
		y0 = 100
		Utils.draw_ui_box(x0, y0, 1 + (w - 32) // 16)
		Utils.draw_text("Your life is consumed", x0 + 3, y0 + 3)

	def hero_killed(self):
		self.game_over = True

	def hero_attack(self):
		self.hero.attacking = True
		self.hero.attack_time = 0.0

		monsters_hit = self.monsters_in_rect(self.hero.attack_hitbox)

		for m in monsters_hit:
			self.hero_hit_monster(m)

		props_hit = self.props_in_rect(self.hero.attack_hitbox)
		log("found {0} props in hitbox".format(len(props_hit)))

		for p in props_hit:
			self.hero_hit_prop(p)
			
		sounds = ["shoot 1", "shoot 2", "expl 2", "expl 3"]
		sfx(sounds[rand(len(sounds))], sfx_volume)

	def hero_reach_exit(self):
		self.fade_out = True
		self.fade_out_time = 0.0
		sfx("rand 10", sfx_volume)

	def hero_pickup_loot(self, loot):
		self.destroy_prop(loot)
		self.hero.life += 20
		sfx("pickup 4", sfx_volume)
		

	def spawn_monster(self, t, x, y):
		m = Monster()
		m.x = x
		m.y = y
		m.id = self.next_id
		m.game = self
		self.next_id += 1
		self.monsters.append(m)

	def spawn_prop(self, t, x, y):
		m = None
		if t == PROP_POTION:
			m = Loot()
		else:
			m = Generator(self)
		m.x = x
		m.y = y
		m.id = self.next_id
		self.next_id += 1
		self.props.append(m)

	def hero_hit_prop(self, prop):
		h = self.hero
		if isinstance(prop, Generator):
			prop.life -= h.force
			if prop.life <= 0:
				self.destroy_prop(prop)

	def hero_hit_monster(self, monster):
		h = self.hero
		monster.life -= h.force
		if monster.life <= 0:
			self.destroy_monster(monster)

	def monster_hit_hero(self, monster, hero):
		hero.life -= monster.force
		if hero.life <= 0:
			self.hero_killed()
	
	def destroy_prop(self, prop):
		self.props.remove(prop)

	def destroy_monster(self, monster):
		self.monsters.remove(monster)
		

	def move_monsters(self, delta):
		h = self.hero

		# move monsters toward hero
		for m in self.monsters:
			d = calc_man_distance(h, m)
			tres = 17.0
			if d > 17.0:
				if h.x > (m.x + tres):
					m.move_x = 1
				elif h.x < (m.x - tres):
					m.move_x = -1
				else:
					m.move_x = 0

				if h.y > (m.y + tres):
					m.move_y = 1
				elif h.y < (m.y - tres):
					m.move_y = -1
				else:
					m.move_y = 0
			else:
				m.move_x = 0
				m.move_y = 0

			ori = calc_orientation(m.move_x, m.move_y)
			if ori != -1:
				m.orientation = ori

			m.disable_collider()
			m.move(delta)
			m.enable_collider()
			m.think(delta, h)

	def monsters_in_rect(self, rect):
		return [m for m in self.monsters if Utils.rect_intersect(rect,m.hitbox)]

	def props_in_rect(self, rect):
		return [p for p in self.props if Utils.rect_intersect(rect, p.hitbox)]

	def loots_in_rect(self, rect):
		return [p for p in self.props if isinstance(p,Loot) and Utils.rect_intersect(rect, p.hitbox)]

class Actor:
	def __init__(self):
		self.x = 160.0
		self.y = 160.0
		self.width = 16.0
		self.height = 16.0
		self.vel_x = 0.0
		self.vel_y = 0.0
		self.move_speed = 48.0
		self.move_x = 0
		self.move_y = 0
		self.orientation = 0
		self.force = 0
		self.life = 100
		self.id = 0
		self.collider_flag = 1

	def move(self, delta):
		self.vel_x = self.move_x * self.move_speed
		self.vel_y = self.move_y * self.move_speed

		dx = self.vel_x * delta
		dy = self.vel_y * delta
		flags = 1
		(nx, ny, col_x, col_y) = mcollide(self.x, self.y, self.width, self.height, dx, dy, flags)

		self.x = nx
		self.y = ny

	@property
	def hitbox(self):
		return (self.x, self.y, self.width, self.height)

	@property
	def attack_hitbox(self):
		vec = Utils.vector_with_orientation(self.orientation)
		dx = 16 * vec[0]
		dy = 16 * vec[1]

		return (self.x + dx, self.y + dy, 16, 16)

	def enable_collider(self):
		hb = self.hitbox
		pyxen.set_collider(self.id, hb[0], hb[1], hb[2], hb[3], self.collider_flag)

	def disable_collider(self):
		pyxen.unset_collider(self.id)


class Hero(Actor):
	def __init__(self):
		super().__init__()
		self.attacking = False
		self.attack_time = 0.0
		self.force = 10
		self.life = 100

	def draw(self, scroll_x, scroll_y):
		image("spr")
		sprite(self.x - scroll_x, self.y - scroll_y, 0, 0, 16, 16)

		if self.attacking:
			vec = Utils.vector_with_orientation(self.orientation)
			dx = 8 + 5 * vec[0]
			dy = 8 + 5 * vec[1]
			pivot(3,8)
			rotate(Utils.angle_with_orientation(self.orientation))
			sprite(self.x + dx - scroll_x, self.y + dy - scroll_y, 0, 16*2, 16, 16)

			rotate(0)
			pivot(0,0)


	def read_inputs(self, delta):
		self.move_x = 0
		self.move_y = 0
		if btn(0): self.move_x = -1
		if btn(1): self.move_x =  1
		if btn(2): self.move_y = -1
		if btn(3): self.move_y =  1
		
		ori = calc_orientation(self.move_x, self.move_y)
		if ori != -1:
			self.orientation = ori

	def update(self, delta):
		if self.attacking:
			self.attack_time += delta
			if self.attack_time >= 0.20:
				self.attacking = False


class Monster(Actor):
	def __init__(self):
		super().__init__()
		self.move_speed = 12.0
		self.hit_delay = 1.0
		self.force = 4
		self.life = 20
		self.game = None

	def draw(self, scroll_x, scroll_y):
		image("spr")
		sprite(self.x - scroll_x, self.y - scroll_y, 0, 16, 16, 16)


	def think(self, delta, hero):
		d = calc_distance(hero, self)		
		(x,y,w,h) = self.hitbox
		x -= 2.0
		y -= 2.0
		w += 4.0
		h += 4.0
		hit = Utils.rect_intersect((x,y,w,h), hero.hitbox)

		if hit:
			self.hit_delay -= delta

		if hit and self.hit_delay <= 0.0:
			self.hit_delay = (rand(10)) / 5
			self.attack_hero(hero)

	def attack_hero(self, hero):
		hit_x = 8.0 + self.x + 0.75 * (hero.x - self.x)
		hit_y = 8.0 + self.y + 0.75 * (hero.y - self.y)
		Utils.fx_blood(hit_x, hit_y)

		sounds = ["hit 1", "hit 3", "hit 4"]
		sfx(sounds[rand(len(sounds))], sfx_volume)

		self.game.monster_hit_hero(self, hero)


class Generator(Actor):
	def __init__(self, game):
		super().__init__()
		self.move_speed = 0.0
		self.force = 0
		self.life = 40
		self.game = game
		self.gen_delay = 4.0

	def draw(self, scroll_x, scroll_y):
		image("spr")
		sprite(self.x - scroll_x, self.y - scroll_y, 16, 32, 16, 16)

	def update(self, delta):
		sx = self.game.scroll_x
		sy = self.game.scroll_y
		view_rect = (sx - 16, sy - 16, sx+256 + 32, sy+240 + 32)
		if not Utils.rect_intersect(view_rect, self.hitbox):
			return

		self.gen_delay -= delta
		if self.gen_delay <= 0.0:
			self.generate()
			self.gen_delay = 4.0 + 0.5 * rand(8)

	def generate(self):
		ori = rand(8)

		for i in range(0, 8):
			vec = Utils.vector_with_orientation((ori + i) % 8)
			dx = 16 * vec[0]
			dy = 16 * vec[1]

			hb = (self.x + dx, self.y + dy, 16, 16)

			hit_something = mhit(hb[0], hb[1], hb[2], hb[3], 1)
			if not hit_something:
				self.game.spawn_monster(1, hb[0], hb[1])
				break


class Loot(Actor):
	def __init__(self):
		super().__init__()
		self.move_speed = 0.0
		self.force = 0
		self.life = 5
		self.gen_delay = 4.0

	def draw(self, scroll_x, scroll_y):
		image("spr")
		sprite(self.x - scroll_x, self.y - scroll_y, 32, 32, 16, 16)

	def update(self,delta):
		pass

	def enable_collider(self):
		# no collider for loot
		return

	def disable_collider(self):
		# no collider for loot
		return








