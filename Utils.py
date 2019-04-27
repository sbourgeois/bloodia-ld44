import pyxen
from pyxen import *


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
	



