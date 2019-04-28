from pyxen import *

from Game import *

game = Game()

def load():
	game.enter_level("final")

def update(delta):
	if btnp(6):
		quit()

	sfxbank("main")
	if not game.game_over:
		game.update(delta)

def draw():
	cls(39.0 / 256.0, 39.0 / 255.0, 68.0 / 255.0, 1.0)

	game.draw()
