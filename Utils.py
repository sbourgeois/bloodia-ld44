import pyxen
from pyxen import *

def load():
	pass

def update(delta):
	pass

def draw():
	cls(0.0, 0.0, 0.0, 1.0)
	color(1, 0, 0, 1)
	draw_text("A: 12324!(%hopUbH", 16, 16)

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
