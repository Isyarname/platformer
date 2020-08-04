import pygame as p

font = "pixelFont.otf"
textColor = (0,0,0)

class Player:
	def __init__(self, surf, x, y, height, width):
		self.x = x
		self.y = y
		self.vx = 4
		self.vy = 0
		self.scHeight = height
		self.scWidth = width
		self.surface = surf
		self.color = (30, 100, 200)
		self.g = 0.5							# 0.5
		self.vyMax = self.g * 16
		self.motion = 0
		self.jump = False
		self.width = self.height = 10
		self.restart = False
		self.level = 1
		self.attempt = 1
		self.editing = True
		self.levelIsNew = False

		self.standsOnThePlatform = 0
		self.pfMotion = 0
		self.pfIndex = 0
		self.Sxl = 0
		self.Sxr = 0
		self.Sy1 = 0
		self.Sy2 = 0
		self.pfType = 0

	def movement(self):
		if self.motion == p.K_RIGHT:
			if self.Sxr < self.vx:
				self.x += self.Sxr
			else:
				self.x += self.vx
		elif self.motion == p.K_LEFT:
			if self.Sxl < self.vx:
				self.x -= self.Sxl
			else:
				self.x -= self.vx
		if self.x > self.scWidth:
			self.x = 0
		elif self.x < 0:
			self.x = self.scWidth
		
		if self.Sy1 != 0:								# притяжение
			self.standsOnThePlatform = 0
			self.vy += self.g
		else:
			self.standsOnThePlatform = self.pfType

		if self.Sy2 <= 0 and self.vy < 0:
			self.vy = 0
		elif self.Sy1 > 0 and self.Sy2 < -self.vy:
			self.vy = -self.Sy2
		if self.pfType == 1 or self.pfType > 3:
			if self.Sy1 < self.vy:
				self.vy = self.Sy1
			if self.Sy1 == 0:
				if self.jump:
					self.vy = -self.vyMax
				else:
					self.vy = 0
		elif self.pfType == 3:
			if self.Sy1 < self.vy or self.Sy1 == 0:
				if self.vy > 8:
					self.vy = -(self.vy * 3 / 4)
				elif self.vy > 3:
					self.vy = -(self.vy - 3)
				else:
					self.vy = 0
					self.y += self.Sy1
				if self.jump:
					self.vy -= self.vyMax
			if self.Sy1 < self.vy and self.Sy1 != 0:
				self.y += (self.Sy1 * 2 - self.vy)
					
		self.y += self.vy
			
	def draw(self):
		self.movement()
		x = round(self.x)
		y = round(self.y)
		form = [(x-self.width, y-self.height), (x-self.width, y+self.height), 
		(x+self.width, y+self.height), (x+self.width, y-self.height)]
		p.draw.polygon(self.surface, self.color, form)


class Platform:
	def __init__(self, points, surface, _type=3):
		self.x1, self.y1, self.x2, self.y2 = points
		self.surface = surface
		self.type = _type
		self.colorSel()

	def colorSel(self):
		if self.type == 1:				# solid
			self.color = (253,150,34)
		elif self.type == 2:			# ghost
			self.color = (165,165,100)
		elif self.type == 3:			# trampoline
			self.color = (255,50,0)
		elif self.type == 4:			# spikes
			self.color = (40,41,35)
		elif self.type == 5:			# passage
			self.color = (69,180,0)

	def getPoints(self):
		return (self.x1, self.y1, self.x2, self.y2)

	def draw(self):
		form = [(self.x1, self.y1), (self.x1, self.y2),
		(self.x2, self.y2), (self.x2, self.y1)]
		p.draw.polygon(self.surface, self.color, form)
		if self.type == 4:		# spikes
			w, h = 4, 9
			for x in range(self.x1+w, self.x2, w*2):
				form = [(x-w, self.y1), (x, self.y1-h), (x+w, self.y1)]
				p.draw.polygon(self.surface, self.color, form)
	

class Button:
	def __init__(self, x, y, surf, size, color):
		self.pressure = False
		self.surface = surf
		self.color = color
		self.textColor = textColor
		self.size = size
		self.f = p.font.Font(font, self.size)
		self.x = x
		self.y = y
		self.w = 10

	def draw(self, txt, Width):
		indent = 10
		x, y = self.x, self.y
		h = len(txt) * self.size / 2.5
		w = 0
		for i in txt:
			if len(i) > w:
				w = len(i) * self.size / 2.5
		fh = round(h + indent)
		fw = round(w + indent)
		form = [(x-fw, y-fh), (x+fw, y-fh), (x+fw, y+fh), (x-fw, y+fh)]
		p.draw.polygon(self.surface, self.color, form)
		tx = x - w
		dy = h * 2 / len(txt)
		for i, line in enumerate(txt):
			text = self.f.render(line, 1, self.textColor)
			ty = round(y - h + dy * i)
			place = text.get_rect(topleft=(tx, ty))
			self.surface.blit(text, place)
		