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
		s = (platform.y - platform.height) - (player.y + player.height + 1)
		if s >= 0:
			platformUnderThePlayer = True
			if s == 0 and platform.solid:
				col = True
			else:
				col = False
		else:
			platformUnderThePlayer = False
			col = False
	else:
		platformUnderThePlayer, s, col = False, 0, False

	return col, platformUnderThePlayer, s

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
	platformUnderThePlayer = False
	for i, platform in enumerate(platforms):
		c = collision(pl, platform)
		if c[0]:
			col = True
		elif c[1] and platform.solid and c[2] < s:
			platformUnderThePlayer = True
			s = c[2]
		platform.draw()

	pl.draw(col, platformUnderThePlayer, s)

def quit():
	p.quit()
	sys.exit()


x = Width // 2
y = Height - 100
color = (253,150,34)
pl = Player(sc, x, 60, Height, Width)
platforms.append(Platform(sc, x, y-20, color, True, x//2))
platforms.append(Platform(sc, x//4, y-20, (150,150,34), False, x//4))
platforms.append(Platform(sc, x, Height, color, True, x))

while True:
	sc.fill((100, 50, 50))
	events()
	play()

	clock.tick(60)

	p.display.set_caption(str(clock))
	p.display.update()
	p.display.flip()