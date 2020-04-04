import pygame as p
import sys
from math import *
from classes import *
#from screeninfo import get_monitors

p.mixer.init()
clock = p.time.Clock()
p.init()

Width = 900
Height = 500
sc = p.display.set_mode((Width, Height))
platforms = []

def collision(player, platform):
	if (player.x - player.width <= platform.x + platform.width and
		player.x + player.width >= platform.x - platform.width):
		p = True
		s = (platform.y - platform.height) - (player.y + player.height)
		if s <= 0 and platform.solid:
			col = True
		else col = False
	else:
		p, s, col = False, 0, False

	return col, p, s

def events():
	for event in p.event.get():
		if event.type == p.QUIT:
			quit()
		elif event.type == p.KEYDOWN:
			if event.key == p.K_ESCAPE:
				quit()
			elif event.key in [p.K_LEFT, p.K_RIGHT]:
				pl.motion = event.key
			elif event.key == p.K_SPACE:
				pl.jump = True
		elif event.type == p.KEYUP:
			if event.key == p.K_SPACE:
				pl.jump = False
			elif event.key == pl.motion:
				pl.motion = 0

def play():
	col = False
	s = Height
	p
	for i, platform in enumerate(platforms):
		c = collision(pl, p)
		if c[0]:
			col = True
		elif c[1] and platform.solid and c[2] < s:
			s = c[2]
		p.draw()

	pl.draw(col,s)

def quit():
	p.quit()
	sys.exit()


x = Width // 2
y = Height - 100
color = (253,150,34)
pl = Player(sc, x, 60)
platforms.append(Platform(sc, x, y-50, color, True, x))

while True:
	sc.fill((100, 50, 50))
	events()
	play()

	clock.tick(60)

	p.display.set_caption(str(clock))
	p.display.update()
	p.display.flip()