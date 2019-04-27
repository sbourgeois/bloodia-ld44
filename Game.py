from pyxen import *

import math
import Utils

from Utils import calc_distance, calc_orientation

class Game:
	def __init__(self):
		self.hero = Hero()
		self.monsters = []
		self.props = []
		self.spawn_monster(1, 120.0, 120.0)
		self.spawn_monster(1, 160.0, 120.0)
		self.spawn_prop(1, 100, 100)

	def draw(self):
		mmap("level1")
		mdraw(0, 0, 0, 0, 16, 16)

		self.hero.draw()
		for m in self.monsters:
			m.draw()
		for prop in self.props:
			prop.draw()

		# Particles
		Utils.draw_particles()

		# draw HUD
		image("ui")
		x0 = (256 - 5 * 16) // 2
		x = x0
		y0 = 0
		sprite(x, y0, 0, 0, 16, 12)
		x += 16
		for i in range(1,4):
			sprite(x, y0, 16, 0, 16, 12)
			x += 16
		sprite(x, y0, 32, 0, 16, 12)
		Utils.draw_text("LIFE: {0}".format(self.hero.life), x0 + 3, y0 + 3)


	def update(self, delta):
		mmap("level1")
		self.hero.read_inputs(delta)
		self.hero.update(delta)
		self.hero.move(delta)

		if btnp(4) and not self.hero.attacking:
			self.hero_attack()

		# move and update monsters
		self.move_monsters(delta)

		# update props
		for prop in self.props:
			prop.update(delta)

		Utils.update_particles(delta)
		
	def hero_attack(self):
		self.hero.attacking = True
		self.hero.attack_time = 0.0

		monsters_hit = self.monsters_in_rect(self.hero.attack_hitbox)

		for m in monsters_hit:
			self.hero_hit_monster(m)
			
		sounds = ["shoot 1", "shoot 2", "expl 2", "expl 3"]
		sfx(sounds[rand(len(sounds))])

	def spawn_monster(self, t, x, y):
		m = Monster()
		m.x = x
		m.y = y
		self.monsters.append(m)

	def spawn_prop(self, t, x, y):
		m = Generator(self)
		m.x = x
		m.y = y
		self.props.append(m)


	def hero_hit_monster(self, monster):
		h = self.hero
		monster.life -= h.force
		if monster.life <= 0:
			self.destroy_monster(monster)


	def destroy_monster(self, monster):
		self.monsters.remove(monster)
		

	def move_monsters(self, delta):
		h = self.hero

		# move monsters toward hero
		for m in self.monsters:
			d = calc_distance(h, m)
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

			m.move(delta)
			m.think(delta, h)

	def monsters_in_rect(self, rect):
		return [m for m in self.monsters if Utils.rect_intersect(rect,m.hitbox)]


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


class Hero(Actor):
	def __init__(self):
		super().__init__()
		self.attacking = False
		self.attack_time = 0.0
		self.force = 10
		self.life = 100

	def draw(self):
		image("spr")
		sprite(self.x, self.y, 0, 0, 16, 16)

		if self.attacking:
			vec = Utils.vector_with_orientation(self.orientation)
			dx = 8 + 5 * vec[0]
			dy = 8 + 5 * vec[1]
			pivot(3,8)
			rotate(Utils.angle_with_orientation(self.orientation))
			sprite(self.x + dx, self.y + dy, 0, 16*2, 16, 16)

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
		self.force = 2
		self.life = 20

	def draw(self):
		image("spr")
		sprite(self.x, self.y, 0, 16, 16, 16)


	def think(self, delta, hero):
		d = calc_distance(hero, self)		
		if d <= 19.0:
			self.hit_delay -= delta

		if d <= 18.0 and self.hit_delay <= 0.0:
			self.hit_delay = (rand(10)) / 5
			self.attack_hero(hero)

	def attack_hero(self, hero):
		global game

		hit_x = 8.0 + self.x + 0.75 * (hero.x - self.x)
		hit_y = 8.0 + self.y + 0.75 * (hero.y - self.y)
		Utils.fx_blood(hit_x, hit_y)

		sounds = ["hit 1", "hit 3", "hit 4"]
		sfx(sounds[rand(len(sounds))])



class Generator(Actor):
	def __init__(self, game):
		super().__init__()
		self.move_speed = 0.0
		self.force = 0
		self.life = 50
		self.game = game
		self.gen_delay = 4.0

	def draw(self):
		image("spr")
		sprite(self.x, self.y, 16, 32, 16, 16)

	def update(self, delta):
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

			monsters = self.game.monsters_in_rect(hb)
			if len(monsters) == 0:
				self.game.spawn_monster(1, hb[0], hb[1])
				break









