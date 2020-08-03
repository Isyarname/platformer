import pygame as p
import sys
import json
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
y = 300
pl = Player(sc, x, 60, Height, Width)

def read():
	with open(fileName, "r", encoding = "UTF-8") as file:
		return json.load(file)

def write():
	with open(fileName, "w", encoding = "UTF-8") as file:
		json.dump(data, file)

def distanceToPlatform(platform):
	if (pl.x - pl.width <= platform.x2 and 
		pl.x + pl.width >= platform.x1):
		sy1 = platform.y1 - (pl.y + pl.height) - 1
		sy2 = pl.y - pl.height - platform.y2 - 1
		if pl.y - pl.height <= platform.y2:
			if sy1 < 9 and platform.type == 4:
				end()
			elif sy1 <= 0 and platform.type == 5:
				nextLevel()
		if 0 <= sy1 < pl.Sy1:
			pl.Sy1 = sy1
			pl.pfType = platform.type
		if 0 <= sy2 < pl.Sy2:
			pl.Sy2 = sy2
	if (pl.y - pl.height <= platform.y2 and 
		pl.y + pl.height >= platform.y1):
		sxl = pl.x - pl.width - platform.x2 - 1
		if 0 <= sxl < pl.Sxl:
			pl.Sxl = sxl
		sxr = platform.x1 - (pl.x + pl.width) - 1
		if 0 <= sxr < pl.Sxr:
			pl.Sxr = sxr

def mouseMotion(event):
	pos = event.pos
	x1, y1, x2, y2 = platforms[pl.pfIndex].getPoints()
	if pl.pfMotion == 1:								# измененте платформы
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
	elif pl.pfMotion == 2:								# передвижение платформы
		platforms[pl.pfIndex].x1 += event.rel[0]
		platforms[pl.pfIndex].y1 += event.rel[1]
		platforms[pl.pfIndex].x2 += event.rel[0]
		platforms[pl.pfIndex].y2 += event.rel[1]
		if pl.standsOnThePlatform == pl.pfIndex and event.rel[1] < 0:
			pl.y += event.rel[1]
			pl.vy -= 2

def editingWithTheKeyboard(event):
	if event.key == p.K_t:
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
		if pl.pause:
			pl.pause = False
	elif event.key == p.K_n:
		nextLevel()
	elif event.key == p.K_c:
		pts = (x-20, y-20, x+20, y+20)
		platforms.append(Platform(pts, sc))

def events():
	for event in p.event.get():
		if event.type == p.MOUSEBUTTONDOWN:
			if pl.editing:
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

		elif event.type == p.MOUSEMOTION and pl.editing:
			mouseMotion(event)

		if event.type == p.QUIT:
			_quit()

		elif event.type == p.KEYDOWN:
			if event.key == p.K_ESCAPE:
				_quit()
			elif event.key in [p.K_LEFT, p.K_RIGHT]:
				pl.motion = event.key
			elif event.key == p.K_SPACE:
				pl.jump = True
			elif pl.editing:
				editingWithTheKeyboard(event)

		elif event.type == p.KEYUP:
			if event.key == p.K_SPACE:
				pl.jump = False
			elif event.key == pl.motion:
				pl.motion = 0

def play():
	pl.Sxr = 9999
	pl.Sxl = 9999
	pl.Sy1 = 9999
	pl.Sy2 = 9999
	pl.pfType = 0
	for i, platform in enumerate(platforms):
		if platform.type != 2 and not pl.pause:
			distanceToPlatform(platform)
		platform.draw()
	pl.draw()
	if pl.hp <= 0:
		eButton.draw("конец", Width)

def end():
	pl.hp = 0
	pl.pause = True

def saveLevel(ls=[]):
	lvl = str(pl.level)
	if ls == []:
		for i in platforms:
			ls.append({"points":i.getPoints(), "type":i.type})
	if lvl in data.keys():
		data[lvl]["platforms"] = ls
	else:
		data.update({lvl:{"player":{"point":[x,y]},"platforms":ls}})

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
			pl.x, pl.y = x, y
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
	play()

	clock.tick(120)

	p.display.set_caption("level = "+str(pl.level))
	p.display.update()
	p.display.flip()
