import pygame


screen_dimensions = (400, 400)

class Player():
	def __init__(self, x, y, width, height, color):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.color = color
		self.rect = (x, y, width, height)
		
		self.velocity = 3
		self.going_up = True

	def draw(self, win): 
		pygame.draw.rect(win, self.color, self.rect)

	def move(self):
		keys = pygame.key.get_pressed()
		
		if keys[pygame.K_UP]:
		 	self.going_up = True  
		
		if keys[pygame.K_DOWN]:
		 	self.going_up = False

		self.update()

	def update(self):
		# Update y's
		if self.going_up: 
			self.y = max(0, self.y - self.velocity)
		else:
			self.y = min(screen_dimensions[1] - self.height, self.y + self.velocity)

		self.rect = (self.x, self.y, self.width, self.height)


class Game:
	def __init__(self, players, player_id):
		self.players = players
		self.player_id = player_id

	def get_player(self):
		return self.players[self.player_id]

	def get_enemy_player(self):
		return self.players[(self.player_id + 1) % len(self.players)]