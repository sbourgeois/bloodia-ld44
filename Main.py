from pyxen import *

from Game import *

import Utils

game = None

def update(delta):
	global game, title_blink

	title_blink += delta
	if title_blink >= 1.2:
		title_blink -= 1.2

	sfxbank("main")

	just_started = False

	if game is None:
		if btnp(6) or btnp(4):
			game = Game()
			game.enter_level(0)
			just_started = True

	if game is not None:
		if game.game_end:
			if btnp(6):
				game = None
		elif not game.game_over:
			if btnp(6) and not just_started:
				game.paused = not game.paused
			if not game.paused:
				game.update(delta)
		elif game.game_over:
			if btnp(6):
				game = None

def draw():
	cls(39.0 / 256.0, 39.0 / 255.0, 68.0 / 255.0, 1.0)

	if game is None:
		draw_game_title()
	elif game.game_end:
		draw_game_end()
	else:
		game.draw()
		if game.paused:
			draw_pause()

title_blink = 0.0

def draw_pause():
	txt = "PAUSED"
	w = len(txt) * 8
	x0 = (256 - w) // 2
	y0 = 100
	Utils.draw_ui_box(x0, y0, 1 + (w - 32) // 16)
	Utils.draw_text(txt, x0 + 10, y0 + 3)

def draw_game_title():
	txt = "BLOODIA"
	w = len(txt) * 8
	x0 = (256 - w) // 2
	y0 = 50
	Utils.draw_ui_box(x0, y0, 1 + (w - 32) // 16)
	Utils.draw_text(txt, x0 + 3, y0 + 3)

	txt = "Press Start or Return key"
	w = len(txt) * 8
	x0 = (256 - w) // 2
	y0 = 140
	if title_blink < 0.95:
		Utils.draw_text(txt, x0 + 3, y0 + 3)

	txt = "Game by Sebastien Bourgeois"
	w = len(txt) * 8
	x0 = (256 - w) // 2
	y0 = 220
	Utils.draw_ui_box(x0, y0, 1 + (w - 32) // 16)
	Utils.draw_text(txt, x0 + 3, y0 + 3)

	txt = "Ludum Dare #44 Compo"
	w = len(txt) * 8
	x0 = (256 - w) // 2
	y0 = 200
	#Utils.draw_ui_box(x0, y0, 1 + (w - 32) // 16)
	Utils.draw_text(txt, x0 + 3, y0 + 3)

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