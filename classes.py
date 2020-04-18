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
		self.g = 0.5
		self.vyMax = self.g * 16
		self.motion = 0
		self.jump = False
		self.width = self.height = 10
		self.hp = 1

	def movement(self, platformUnderThePlayer, s, pType, platformAboveThePlayer, s2):
		if self.motion == p.K_RIGHT:
			self.x += self.vx
		elif self.motion == p.K_LEFT:
			self.x -= self.vx
		if self.x > self.scWidth:
			self.x = 0
		elif self.x < 0:
			self.x = self.scWidth

		if s != 0: #гравитация
			self.vy += self.g

		if platformAboveThePlayer:
			if s2 <= 0 and self.vy < 0:
				self.vy = 0
			elif s > 0 and s2 < -self.vy:
				self.vy = -s2
		
		if platformUnderThePlayer:
			if pType == ("solid" or "spikes"):
				if s < self.vy:
					self.vy = s
				if s == 0:
					if self.jump:
						self.vy -= self.vyMax
					else:
						self.vy = 0
			elif pType == "trampoline":
				if s < self.vy or s == 0:
					if self.vy > 8:
						self.vy = -(self.vy * 3 / 4)
					elif self.vy > 3:
						self.vy = -(self.vy - 3)
					else:
						self.vy = 0
						self.y += s
					if self.jump:
						self.vy -= self.vyMax
				if s < self.vy and s != 0:
					self.y += (s * 2 - self.vy)
			elif pType == "spikes":
				if s == 0:
					self.hp = 0
					
		self.y += self.vy
			
	def draw(self, platformUnderThePlayer, s, pType, platformAboveThePlayer, s2):
		self.movement(platformUnderThePlayer, s, pType, platformAboveThePlayer, s2)
		print("hp =", self.hp)
		x = round(self.x)
		y = round(self.y)
		form = [(x-self.width, y-self.height), (x-self.width, y+self.height), 
		(x+self.width, y+self.height), (x+self.width, y-self.height)]
		p.draw.polygon(self.surface, self.color, form)


class Platform:
	def __init__(self, surface, x, y, type, width):
		self.x = x
		self.y = y
		self.surface = surface
		if type == "solid":
			self.color = (253,150,34)
		elif type == "ghost":
			self.color = (165,165,100)
		elif type == "trampoline":
			self.color = (255,50,0)
		elif type == "spikes":
			self.color = (40,41,35)
		self.type = type
		self.width = width
		self.height = 2

	def draw(self):
		form = [(self.x-self.width, self.y-self.height), (self.x-self.width, self.y+self.height), 
		(self.x+self.width, self.y+self.height), (self.x+self.width, self.y-self.height)]
		p.draw.polygon(self.surface, self.color, form)
		if self.type == "spikes":
			y = self.y - self.height
			w = 4
			h = 9
			for x in range(self.x-self.width+w, self.x+self.width, w*2):
				form = [(x-w, y), (x, y-h), (x+w, y)]
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
		self.h = size * 10 // 19 + 7
		self.w = 10

	def draw(self, txt, Width):
		text = self.f.render(txt, 1, self.textColor)
		self.w = len(txt) * self.size // 3 + 10
		if self.x - self.w < 5:
			self.x -= (self.x - self.w) - 5
		elif self.x + self.w > Width - 5:
			self.x -= (self.x + self.w) - (Width - 5)
		place = text.get_rect(center=(self.x,self.y))
		form = [(self.x - self.w, self.y - self.h), (self.x + self.w, self.y - self.h),
		(self.x + self.w, self.y + self.h), (self.x - self.w, self.y + self.h)]
		p.draw.polygon(self.surface, self.color, form)
		self.surface.blit(text, place)

