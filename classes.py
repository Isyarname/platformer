import pygame as p


class Player:
	def __init__(self, surf, x, y):
		self.x = x
		self.y = y
		self.vx = 4
		self.vy = 0
		self.surface = surf
		self.color = (30, 100, 200)
		self.vyMax = -6
		self.g = 1
		self.motion = 0
		self.jump = False
		self.width = self.height = 5

	def movement(self, collision, s):
		if self.motion == p.K_RIGHT:
			self.x += self.v
		elif self.motion == p.K_LEFT:
			self.x -= self.v
		if collision:
			print("collision")
			if self.jump == True:
				print("jump")
				self.vy = self.vyMax
			else:
				self.vy = 0
		else:
			if self.vy < - self.vyMax and self.vy <= s:
				self.vy += self.g
			else:
				self.vy = s
		self.y += self.vy
			
	def draw(self, collision, s):
		self.movement(collision)
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
	