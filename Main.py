from pyxen import *

def update(delta):
	if btnp(6):
		quit()

def draw():
	cls(39.0 / 256.0, 39.0 / 255.0, 68.0 / 255.0, 1.0)

	mmap("level1")
	mdraw(0, 0, 0, 0, 16, 16)

	image("spr")
	sprite(160, 160, 0, 0, 16, 16)
	
