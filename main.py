import pygame as p
import sys, json
from classes import *

p.mixer.init()
clock = p.time.Clock()
p.init()

Width = 900
Height = 500
sc = p.display.set_mode((Width, Height))
platforms = []

fileName = "data.json"
buttonColor = (140, 140, 140)
eButton = Button(Width//2, Height//2, sc, Width//15, buttonColor)	# конец

x = Width // 2
y = Height // 2														# Height - 100
pl = Player(sc, x, 60, Height, Width)
pfMotion = 0
pf = 0

def read():
	with open(fileName, "r", encoding = "UTF-8") as file:
		return json.load(file)

def write():
	with open(fileName, "w", encoding = "UTF-8") as file:
		json.dump(data, file)

def distanceToPlatform(platform):
	if (pl.x - pl.width <= platform.x2 and 
		pl.x + pl.width >= platform.x1 and platform.type != 2):
		s = (platform.y1) - (pl.y + pl.height + 1)
		if pl.y - pl.height <= platform.y2:
			if pl.y + pl.height >= platform.y1 - 9 and platform.type == 4:
				pl.hp = 0
			elif pl.y + pl.height >= platform.y1 - 1 and platform.type == 5:
				nextLevel()
		if s >= 0:
			platformUnderThePlayer = True
			platformAboveThePlayer, s2 = False, False
		else:
			platformUnderThePlayer = False
			s2 = (pl.y - pl.height - 1) - (platform.y2)
			if s2 >= 0:
				platformAboveThePlayer = True
			else:
				platformAboveThePlayer = False
	else:
		platformUnderThePlayer, s = False, False
		platformAboveThePlayer, s2 = False, False

	return (platformUnderThePlayer, s, platformAboveThePlayer, s2)

def events():
	for event in p.event.get():
		if event.type == p.MOUSEBUTTONDOWN:
			pos = event.pos
			for i, o in enumerate(platforms):
				if (o.x1 <= pos[0] <= o.x2 and o.y1 <= pos[1] <= o.y2):
					pl.pfIndex = i
					if event.button == 1:
						pl.pfMotion = 1
					elif event.button == 3:
						pl.pfMotion = 2

		elif event.type == p.MOUSEBUTTONUP:
			pl.pfMotion = 0

		elif event.type == p.MOUSEMOTION:
			pos = event.pos
			x1, y1, x2, y2 = platforms[pl.pfIndex].getPoints()
			if pl.pfMotion == 1:							# измененте платформы
				if pos[0]-x1 < x2-pos[0]:
					platforms[pl.pfIndex].x1 += event.rel[0]
				else:
					platforms[pl.pfIndex].x2 += event.rel[0]
				if pos[1]-y1 < y2-pos[1]:
					platforms[pl.pfIndex].y1 += event.rel[1]
					if pl.standsOnThePlatform == pl.pfIndex and event.rel[1] < 0:
						pl.y += event.rel[1]
						pl.vy -= 2
				else:
					platforms[pl.pfIndex].y2 += event.rel[1]
			elif pl.pfMotion == 2:							# передвижение платформы
				platforms[pl.pfIndex].x1 += event.rel[0]
				platforms[pl.pfIndex].y1 += event.rel[1]
				platforms[pl.pfIndex].x2 += event.rel[0]
				platforms[pl.pfIndex].y2 += event.rel[1]
				if pl.standsOnThePlatform != 0 and event.rel[1] < 0:
					pl.y += event.rel[1]
					pl.vy -= 2

		if event.type == p.QUIT:
			_quit()

		elif event.type == p.KEYDOWN:
			if event.key == p.K_ESCAPE:
				_quit()
			elif event.key in [p.K_LEFT, p.K_RIGHT]:
				pl.motion = event.key
			elif event.key == p.K_SPACE:
				pl.jump = True
			elif event.key == p.K_t:
				platforms[pl.pfIndex].type += 1
				if platforms[pl.pfIndex].type > 5:
					platforms[pl.pfIndex].type = 1
				platforms[pl.pfIndex].colorSel()
			elif event.key == p.K_d:
				platforms.pop(pl.pfIndex)
				pl.pfIndex -= 1
				pl.pfMotion = 0
			elif event.key == p.K_p:
				savePoint()
			elif event.key == p.K_l:
				saveLevel()
			elif event.key == p.K_r:
				restart()
			elif event.key == p.K_n:
				nextLevel()
			elif event.key == p.K_c:
				pts = (x-20, y-20, x+20, y+20)
				platforms.append(Platform(pts, sc))

		elif event.type == p.KEYUP:
			if event.key == p.K_SPACE:
				pl.jump = False
			elif event.key == pl.motion:
				pl.motion = 0

def play():
	s, pl.platformUnder = Height, False
	s2, pl.platformAbove = Height, False
	pfType = 0
	for i, platform in enumerate(platforms):
		d = distanceToPlatform(platform)
		if d[0] and d[1] < s:
			pl.platformUnder = True
			pfType = platform.type
			s = d[1]
		elif d[2] and d[3] < s2:
			pl.platformAbove = True
			s2 = d[3]
		platform.draw()

	pl.draw(s, pfType, s2)

def saveLevel(ls=[]):
	lvl = str(pl.level)
	if ls == []:
		for i in platforms:
			ls.append({"points":i.getPoints(), "type":i.type})
	if lvl in data.keys():
		data[lvl]["platforms"] = ls
	else:
		data.update({lvl:{"player":{"point":[x,300]},"platforms":ls}})

def savePoint():
	point = [pl.x, pl.y]
	lvl = str(pl.level)
	if lvl in data.keys():
		data[lvl]["player"]["point"] = point
	else:
		data.update({lvl:{"player":{"point":point},"platforms":[]}})

def restart():
	lvl = str(pl.level)
	point = data[lvl]["player"]["point"]
	pl.x, pl.y = point
	pl.vy = 0
	pl.hp += 1

def nextLevel():
	if pl.level < 5:
		pl.level += 1
		lvl = str(pl.level)
		platforms.clear()
		pl.vy = 0
		if lvl in data.keys():
			point = data[lvl]["player"]["point"]
			pl.x, pl.y = point
			for i in data[lvl]["platforms"]:
				platforms.append(Platform(i["points"], sc, i["type"]))
			pl.pfIndex = len(platforms) - 1
		else:
			platforms.append(Platform([1, 475, 918, 506], sc, 1))
			pl.x, pl.y = x, 200
			pl.pfIndex = 0
			saveLevel()
	else:
		print("капец, куда тебе столько уровней?")

def _quit():
	saveLevel()
	write()
	p.quit()
	sys.exit()


data = read()
for i in data[str(pl.level)]["platforms"]:
	platforms.append(Platform(i["points"], sc, i["type"]))

while True:
	sc.fill((100, 50, 50))
	events()
	if pl.hp <= 0:
		eButton.draw("конец", Width)
	else:
		play()

	clock.tick(120)

	p.display.set_caption("level = "+str(pl.level))
	p.display.update()
	p.display.flip()