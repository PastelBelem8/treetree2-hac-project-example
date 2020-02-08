import pygame

screen_dimensions = (400, 300)
offset_y = 15

class Player():
	def __init__(self, x, y, width, height, color):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.color = color
		self.rect = (x, y, width, height)
		self.hitbox = self.rect
		
		self.velocity = 3
		self.y_direction = 0

	def draw(self, win): 
		pygame.draw.rect(win, self.color, self.rect)

	def move(self):
		keys = pygame.key.get_pressed()
		
		if keys[pygame.K_UP]:
		 	self.y_direction = -1  
		
		if keys[pygame.K_DOWN]:
		 	self.y_direction = 1

		self.update()

	def update(self):
		self.y = self.y + self.y_direction * self.velocity

		if self.y_direction == -1 and self.y <= offset_y: 
			self.y = offset_y
			self.y_direction = 0

		elif self.y_direction == 1 and self.y > screen_dimensions[1] - self.height - offset_y:
			self.y = screen_dimensions[1] - self.height - offset_y
			self.y_direction = 0

		self.rect = (self.x, self.y, self.width, self.height)
		self.hitbox = self.rect


class Game:
	def __init__(self, players, player_id):
		self.players = players
		self.player_id = player_id

	def get_player(self):
		return self.players[self.player_id]

	def get_other_player(self):
		return self.players[(self.player_id + 1) % len(self.players)]

	def update(self):
		self.players[self.player_id].move()

	def draw(self, win):
		for p in self.players:
			p.draw(win)
