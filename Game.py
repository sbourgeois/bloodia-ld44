from pyxen import *

import math

def calc_distance(a, b):
	return math.sqrt((b.x - a.x) ** 2 + (b.y - a.y) ** 2)

class Game:
	def __init__(self):
		self.hero = Hero()
		self.monsters = []
		self.spawn_monster(1, 120.0, 120.0)
		self.spawn_monster(1, 160.0, 120.0)

	def draw(self):
		mmap("level1")
		mdraw(0, 0, 0, 0, 16, 16)

		self.hero.draw()
		for m in self.monsters:
			m.draw()


	def update(self, delta):
		mmap("level1")
		self.hero.read_inputs(delta)
		self.hero.move(delta)

		# move monsters toward hero
		for m in self.monsters:
			h = self.hero
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
			m.move(delta)
		

	def spawn_monster(self, t, x, y):
		m = Monster()
		m.x = x
		m.y = y
		self.monsters.append(m)

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

	def move(self, delta):
		self.vel_x = self.move_x * self.move_speed
		self.vel_y = self.move_y * self.move_speed

		dx = self.vel_x * delta
		dy = self.vel_y * delta
		flags = 1
		(nx, ny, col_x, col_y) = mcollide(self.x, self.y, self.width, self.height, dx, dy, flags)

		self.x = nx
		self.y = ny


class Hero(Actor):
	def __init__(self):
		super().__init__()

	def draw(self):
		image("spr")
		sprite(self.x, self.y, 0, 0, 16, 16)

	def read_inputs(self, delta):
		self.move_x = 0
		self.move_y = 0
		if btn(0): self.move_x = -1
		if btn(1): self.move_x =  1
		if btn(2): self.move_y = -1
		if btn(3): self.move_y =  1


class Monster(Actor):
	def __init__(self):
		super().__init__()
		self.move_speed = 12.0

	def draw(self):
		image("spr")
		sprite(self.x, self.y, 0, 16, 16, 16)






