from pyxen import *

class Game:
	def __init__(self):
		self.hero = Hero()

	def draw(self):
		mmap("level1")
		mdraw(0, 0, 0, 0, 16, 16)

		self.hero.draw()


	def update(self, delta):
		mmap("level1")
		self.hero.update(delta)


class Hero:
	def __init__(self):
		self.x = 160.0
		self.y = 160.0
		self.width = 16.0
		self.height = 16.0
		self.vel_x = 0.0
		self.vel_y = 0.0
		self.move_speed = 48.0

	def draw(self):
		image("spr")
		sprite(self.x, self.y, 0, 0, 16, 16)

	def update(self, delta):
		move_x = 0
		move_y = 0
		if btn(0): move_x = -1
		if btn(1): move_x =  1
		if btn(2): move_y = -1
		if btn(3): move_y =  1

		self.vel_x = move_x * self.move_speed
		self.vel_y = move_y * self.move_speed

		dx = self.vel_x * delta
		dy = self.vel_y * delta
		flags = 1
		(nx, ny, col_x, col_y) = mcollide(self.x, self.y, self.width, self.height, dx, dy, flags)

		self.x = nx
		self.y = ny











