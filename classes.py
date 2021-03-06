import pygame as p

font = "pixelFont.otf"

class Player:
	def __init__(self, surf, x, y, height, width):
		self.x = x
		self.y = y
		self.vx = 3
		self.vy = 0
		self.scHeight = height
		self.scWidth = width
		self.surface = surf
		self.color = (30, 100, 200)
		self.g = 0.5
		self.vyMax = self.g * 16
		self.motion = 0
		self.jump = False
		self.width = 10
		self.height = 10
		self.level = 1
		self.attempt = 1
		self.editing = True

		self.pfMotion = 0
		self.pfIndex = 0
		self.sxl = 0
		self.sxr = 0
		self.sy1 = 0
		self.sy2 = 0
		self.pfType = 0
		self.backgroundColor = (62,62,62)
		self.pfColors = [(253,150,34), (165,165,100), (255,50,0), (40,41,35), (69,180,0)]

	def movement(self):
		if self.motion == p.K_RIGHT:
			if self.sxr < self.vx:
				self.x += self.sxr
			else:
				self.x += self.vx
		elif self.motion == p.K_LEFT:
			if self.sxl < self.vx:
				self.x -= self.sxl
			else:
				self.x -= self.vx
		if self.x > self.scWidth:
			self.x = 0
		elif self.x < 0:
			self.x = self.scWidth
		
		if self.sy1 != 0:								# gravitation
			self.vy += self.g

		if self.sy2 <= 0 and self.vy < 0:
			self.vy = 0
		elif self.sy1 > 0 and self.sy2 < -self.vy:
			self.vy = -self.sy2
		if self.pfType == 1 or self.pfType > 3:
			if self.sy1 < self.vy:
				self.vy = self.sy1
			if self.sy1 == 0:
				if self.jump:
					self.vy = -self.vyMax
				else:
					self.vy = 0
		elif self.pfType == 3:							#trampoline
			if self.sy1 < self.vy or self.sy1 == 0:
				if self.vy > 1.5:
					self.vy = -self.vy * 0.8 + 1
				else:
					self.vy = 0
					self.y += self.sy1
				if self.jump:
					self.vy -= self.vyMax
			if self.sy1 < self.vy and self.sy1 != 0:
				self.y += (self.sy1 * 2 - self.vy)
					
		self.y += self.vy

	def getPoints(self):
		return (self.x - self.width, self.y - self.height, 
			self.x + self.width, self.y + self.height)
			
	def draw(self):
		self.movement()
		x = round(self.x)
		y = round(self.y)
		form = [(x-self.width, y-self.height), (x-self.width, y+self.height), 
		(x+self.width, y+self.height), (x+self.width, y-self.height)]
		p.draw.polygon(self.surface, self.color, form)

class Platform:
	def __init__(self, points, surface, _type, color):
		self.x1, self.y1, self.x2, self.y2 = points
		self.surface = surface
		self.type = _type
		self.color = color
		self.form = [(self.x1, self.y1), (self.x1, self.y2),
		(self.x2, self.y2), (self.x2, self.y1)]

	def getPoints(self):
		return (self.x1, self.y1, self.x2, self.y2)

	def formUpdate(self):
		self.form = [(self.x1, self.y1), (self.x1, self.y2),
		(self.x2, self.y2), (self.x2, self.y1)]

	def draw(self):
		p.draw.polygon(self.surface, self.color, self.form)
		if self.type == 4:		# spikes
			w, h = 4, 9
			for x in range(self.x1+w, self.x2, w*2):
				form = [(x-w, self.y1), (x, self.y1-h), (x+w, self.y1)]
				p.draw.polygon(self.surface, self.color, form)

class Table:
	def __init__(self, x, y, surf, size, color):
		self.pressure = False
		self.surface = surf
		self.color = color
		self.textColor = (0,0,0)
		self.size = size
		self.f = p.font.Font(font, self.size)
		self.x = x
		self.y = y

	def draw(self, txt, height, lenght):
		h = height * self.size / 2
		w = lenght * self.size / 3
		indent = 8
		fh = round(h + indent)
		fw = round(w + indent)
		form = [(self.x-fw, self.y-fh), (self.x+fw, self.y-fh), 
		(self.x+fw, self.y+fh), (self.x-fw, self.y+fh)]
		p.draw.polygon(self.surface, self.color, form)
		tx = self.x - w
		dy = h * 2 / height
		for i, line in enumerate(txt):
			text = self.f.render(line, 1, self.textColor)
			ty = round(self.y - h + dy * i)
			place = text.get_rect(topleft=(tx, ty))
			self.surface.blit(text, place)
		