from pyxen import *

from Game import *

import Utils

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

	if game.game_end:
		draw_game_end()
	else:
		game.draw()

def draw_game_end():
	txt = "Congratulations!"
	w = len(txt) * 8
	x0 = (256 - w) // 2
	y0 = 100
	Utils.draw_ui_box(x0, y0, 1 + (w - 32) // 16)
	Utils.draw_text(txt, x0 + 3, y0 + 3)

	txt = "Thanks for Playing!"
	w = len(txt) * 8
	x0 = (256 - w) // 2
	y0 = 160

	Utils.draw_text(txt, x0 + 3, y0 + 3)