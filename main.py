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
		player.x + player.width >= platform.x - platform.width and platform.type != "ghost"):
		s = (platform.y - platform.height) - (player.y + player.height + 1)
		if s >= 0:
			platformUnderThePlayer = True
			platformAboveThePlayer, s2 = False, False
		else:
			platformUnderThePlayer = False
			s2 = (player.y - player.height - 1) - (platform.y + platform.height)
			if s2 >= 0:
				platformAboveThePlayer = True
			else:
				platformAboveThePlayer = False
	else:
		platformUnderThePlayer, s = False, False
		platformAboveThePlayer, s2 = False, False

	return platformUnderThePlayer, s, platformAboveThePlayer, s2

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
	s, platformUnderThePlayer = Height, False
	s2, platformAboveThePlayer = Height, False
	pType = "ghost"
	for i, platform in enumerate(platforms):
		d = distanceToPlatform(pl, platform)
		if d[0] and platform.type and d[1] < s:
			platformUnderThePlayer = True
			pType = platform.type
			s = d[1]
		elif d[2] and platform.type and d[3] < s2:
			platformAboveThePlayer = True
			s2 = d[3]
		platform.draw()

	pl.draw(platformUnderThePlayer, s, pType, platformAboveThePlayer, s2)

def quit():
	p.quit()
	sys.exit()


x = Width // 2
y = Height - 100
pl = Player(sc, x, 60, Height, Width)
platforms.append(Platform(sc, x, 20, "solid", x))
platforms.append(Platform(sc, x, y-20, "solid", x//2))
platforms.append(Platform(sc, x//4, y-20, "ghost", x//4))
platforms.append(Platform(sc, Width - x//4, y-20, "trampoline", x//4))
platforms.append(Platform(sc, Width*3//4, Height, "solid", x//2))
platforms.append(Platform(sc, Width//4, Height, "trampoline", x//2))

while True:
	sc.fill((100, 50, 50))
	events()
	play()

	clock.tick(120)

	p.display.set_caption(str(clock))
	p.display.update()
	p.display.flip()