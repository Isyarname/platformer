import pygame as p


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
			if pType == "solid":
				if s < self.vy:
					self.vy = s
				if s == 0:
					if self.jump:
						self.vy -= self.vyMax
					else:
						self.vy = 0
			elif pType == "trampoline":
				if s < self.vy or s == 0:
					print("vy =", self.vy)
					if self.vy > 8:
						self.vy = -(self.vy * 3 / 4)
					elif self.vy > 3:
						self.vy = -(self.vy - 3)
					else:
						self.vy = 0
						self.y += s
					print("vy2 =", self.vy)
					if self.jump:
						print("jump")
						self.vy -= self.vyMax
				if s < self.vy and s != 0:
					self.y += (s * 2 - self.vy)
					print("y =", self.y)
					
		self.y += self.vy
			
	def draw(self, platformUnderThePlayer, s, pType, platformAboveThePlayer, s2):
		self.movement(platformUnderThePlayer, s, pType, platformAboveThePlayer, s2)
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
		self.type = type
		self.width = width
		self.height = 2

	def draw(self):
		form = [(self.x-self.width, self.y-self.height), (self.x-self.width, self.y+self.height), 
		(self.x+self.width, self.y+self.height), (self.x+self.width, self.y-self.height)]
		p.draw.polygon(self.surface, self.color, form)
	