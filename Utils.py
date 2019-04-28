import pyxen
import math

from pyxen import *


def calc_distance(a, b):
	return math.sqrt((b.x - a.x) ** 2 + (b.y - a.y) ** 2)

def calc_man_distance(a, b):
	return math.fabs(b.x - a.x) + math.fabs(b.y - a.y)

# a and b : (x,y,w,h)
def rect_intersect(a, b):
	ax0 = a[0]
	ax1 = ax0 + a[2]
	ay0 = a[1]
	ay1 = ay0 + a[3]
	bx0 = b[0]
	bx1 = bx0 + b[2]
	by0 = b[1]
	by1 = by0 + b[3]
	return ax0 < bx1 and ax1 > bx0 and ay0 < by1 and ay1 > by0


def calc_orientation(move_x, move_y):
	if move_x == 1 and move_y == 0:
		return 0
	elif move_x == 1 and move_y == 1:
		return 1
	elif move_x == 0 and move_y == 1:
		return 2
	elif move_x == -1 and move_y == 1:
		return 3
	elif move_x == -1 and move_y == 0:
		return 4
	elif move_x == -1 and move_y == -1:
		return 5
	elif move_x == 0 and move_y == -1:
		return 6
	elif move_x == 1 and move_y == -1:
		return 7
	return -1		

_angles = [0, 315, 270, 225, 180, 135, 90, 45]
def angle_with_orientation(orient):
	return _angles[orient]

_vectors = [(1,0), (1,1), (0,1), (-1,1), (-1,0), (-1,-1), (0,-1), (1,-1)]
def vector_with_orientation(orient):
	return _vectors[orient]

def draw_text(s, x, y):
	dx = 0
	for character in s:
		val = ord(character)
		col = val % 16
		row = val // 16
		s = pyxen.Sprite("font", col*8, row*8, 8, 8)
		#s.color = pyxen.Color(1, 0, 0, 1)
		s.draw(x + dx, y)
		dx += 8


class Particle:
	def __init__(self, kind, x, y):
		self.kind = kind
		self.x = x
		self.y = y
		self.t = 0.0
		self.speed = 8.0
		self.ttl = 3.0
		self.image_name = "fx"

particles = []

def update_particles(delta):
	global particles
	
	dead_particles = []
	for p in particles:
		p.t += delta * p.speed
		if p.t >= p.ttl:
			dead_particles.append(p)
	for p in dead_particles:
		particles.remove(p)


def draw_particles(scroll_x, scroll_y):
	global particles

	for p in particles:
		image(p.image_name)
		i = int(p.t)
		j = 0
		sprite(p.x - 4 - scroll_x, p.y - 4 - scroll_y, i * 8, j * 8, 8, 8)

def fx_blood(x, y):
	global particles

	p = Particle(1, x, y)
	particles.append(p)




class InstantSprite:
	def __init__(self, kind, x, y):
		self.kind = kind
		self.x0 = x
		self.y0 = y
		self.x1 = x
		self.y1 = y - 16.0
		self.t = 0.0
		self.speed = 5.0
		self.ttl = 4.0
		self.image_name = "spr"
		self.col = 2
		self.row = 2

isprites = []

def update_isprites(delta):
	global isprites
	
	dead_particles = []
	for p in isprites:
		p.t += delta * p.speed
		if p.t >= p.ttl:
			dead_particles.append(p)
	for p in dead_particles:
		isprites.remove(p)


def draw_isprites(scroll_x, scroll_y):
	global isprites

	for p in isprites:
		image(p.image_name)
		i = p.col
		j = p.row
		t = p.t
		if t > 1.0:
			t = 1.0
		x = (1.0 - t) * p.x0 + t * p.x1
		y = (1.0 - t) * p.y0 + t * p.y1

		blink_time = int(p.t * 100.0) % 10
		if p.t >= 1.6 and blink_time >= 7:
			return

		sprite(x - scroll_x, y - scroll_y, i * 16, j * 16, 16, 16)


def fx_raise_sprite(x, y, col, row):
	global isprites

	p = InstantSprite(1, x, y)
	p.col = col
	p.row = row
	isprites.append(p)
	

def draw_ui_box(x0, y0, nb_repeats):
	image("ui")
	x = x0
	sprite(x, y0, 0, 0, 16, 12)
	x += 16
	for i in range(0,nb_repeats):
		sprite(x, y0, 16, 0, 16, 12)
		x += 16
	sprite(x, y0, 32, 0, 16, 12)



