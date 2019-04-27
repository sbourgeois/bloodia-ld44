import pyxen
import math

from pyxen import *


def calc_distance(a, b):
	return math.sqrt((b.x - a.x) ** 2 + (b.y - a.y) ** 2)

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


def draw_particles():
	global particles

	image("fx")
	for p in particles:
		i = int(p.t)
		j = 0
		sprite(p.x - 4, p.y - 4, i * 8, j * 8, 8, 8)

def fx_blood(x, y):
	global particles

	p = Particle(1, x, y)
	particles.append(p)
	

def draw_ui_box(x0, y0, nb_repeats):
	image("ui")
	x = x0
	sprite(x, y0, 0, 0, 16, 12)
	x += 16
	for i in range(0,nb_repeats):
		sprite(x, y0, 16, 0, 16, 12)
		x += 16
	sprite(x, y0, 32, 0, 16, 12)



