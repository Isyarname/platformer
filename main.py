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

def distanceToPlatform(player, platform):
	if (player.x - player.width <= platform.x + platform.width and
		player.x + player.width >= platform.x - platform.width):
		s = (platform.y - platform.height) - (player.y + player.height + 1)
		if s >= 0:
			platformUnderThePlayer = True
		else:
			platformUnderThePlayer = False
	else:
		platformUnderThePlayer, s = False, False

	return platformUnderThePlayer, s

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
	s = Height
	platformUnderThePlayer = False
	pType = "ghost"
	for i, platform in enumerate(platforms):
		d = distanceToPlatform(pl, platform)
		if d[0] and platform.type != "ghost" and d[1] < s:
			platformUnderThePlayer = True
			pType = platform.type
			s = d[1]
		platform.draw()

	pl.draw(platformUnderThePlayer, s, pType)

def quit():
	p.quit()
	sys.exit()


x = Width // 2
y = Height - 100
color = (253,150,34)
pl = Player(sc, x, 60, Height, Width)
platforms.append(Platform(sc, x, y-20, color, "solid", x//2))
platforms.append(Platform(sc, x//4, y-20, (150,150,34), "ghost", x//4))
platforms.append(Platform(sc, Width - x//4, y-20, (255,100,0), "trampoline", x//4))
platforms.append(Platform(sc, Width*3//4, Height, color, "solid", x//2))
platforms.append(Platform(sc, Width//4, Height, (255,100,0), "trampoline", x//2))

while True:
	sc.fill((100, 50, 50))
	events()
	play()

	clock.tick(60)

	p.display.set_caption(str(clock))
	p.display.update()
	p.display.flip()