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
		self.vyMax = -15
		self.g = 1
		self.motion = 0
		self.jump = False
		self.width = self.height = 10

	def movement(self, collision, platformUnderThePlayer, s):
		if self.motion == p.K_RIGHT:
			self.x += self.vx
		elif self.motion == p.K_LEFT:
			self.x -= self.vx
		if self.x > self.scWidth:
			self.x = 0
		elif self.x < 0:
			self.x = self.scWidth
		if collision:
			if self.jump == True:
				self.vy = self.vyMax
			else:
				self.vy = 0
		else:
			if self.vy < - self.vyMax :
				self.vy += self.g
			if platformUnderThePlayer and s < self.vy:
				self.vy = s
		self.y += self.vy//1
			
	def draw(self, collision, platformUnderThePlayer, s):
		self.movement(collision, platformUnderThePlayer, s)
		form = [(self.x-self.width, self.y-self.height), (self.x-self.width, self.y+self.height), 
		(self.x+self.width, self.y+self.height), (self.x+self.width, self.y-self.height)]
		p.draw.polygon(self.surface, self.color, form)


class Platform:
	def __init__(self, surface, x, y, color, sol, width):
		self.x = x
		self.y = y
		self.surface = surface
		self.color = color
		self.solid = sol
		self.width = width
		self.height = 2

	def draw(self):
		form = [(self.x-self.width, self.y-self.height), (self.x-self.width, self.y+self.height), 
		(self.x+self.width, self.y+self.height), (self.x+self.width, self.y-self.height)]
		p.draw.polygon(self.surface, self.color, form)
	