import pygame
import random

obstacle_dimensions = (40, 37)
screen_dimensions = (400, 300)
offset_y = 15

class Player:
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


class Obstacle:
	"""Represents an obstacle."""
	images = [
		pygame.transform.scale(pygame.image.load("../resources/images/bird0.png"), obstacle_dimensions),
		pygame.transform.scale(pygame.image.load("../resources/images/bird1.png"), obstacle_dimensions),
		pygame.transform.scale(pygame.image.load("../resources/images/bird2.png"), obstacle_dimensions),
		pygame.transform.scale(pygame.image.load("../resources/images/bird3.png"), obstacle_dimensions),
		pygame.transform.scale(pygame.image.load("../resources/images/bird4.PNG"), obstacle_dimensions),
	]
	def __init__(self, x, y):
		self.width, self.height = obstacle_dimensions
		self.x = x - self.width
		self.y = max(0, y - self.height)

		self.count = -1
		self.max_count = len(Obstacle.images)

	def update(self):
		self.count = (self.count + 1) % self.max_count * 2

	def draw(self, win):
		# Defines the accurate hitbox for our character 
		self.hitbox = (self.x + 10, self.y + 5, self.width - 20, self.height - 5)
		pygame.draw.rect(win, (255,0,0), self.hitbox, 2)

		# This is what will allow us to animate the saw
		self.update()
		win.blit(self.images[self.count], (self.x, self.y))  

	def move(self, vel):
		self.x -= vel

	def is_off_screen(self):
		return self.x < self.width / 3
 

class Game:
	def __init__(self, players, player_id, obstacles=[]):
		"""Initialize the game, and create resources."""
		self.players = players
		self.player_id = player_id
		self.obstacles = obstacles

	def get_player(self):
		return self.players[self.player_id]

	def get_obstacles(self):
		return self.obstacles

	def get_other_player(self):
		return self.players[(self.player_id + 1) % len(self.players)]

	def generate_obstacle(self):
		screen_width, screen_height = screen_dimensions
		# Generate obstacle on
		obstacle_y = random.randint(0, screen_height)
		self.obstacles.append(Obstacle(screen_width, obstacle_y))

	def update(self):
		self.players[self.player_id].move()
		for obstacle in self.obstacles:
			obstacle.move(vel=1.5)
			# If the obstacle no longer appears in the screen,
			# remove it!
			if obstacle.is_off_screen():
				self.obstacles.pop(self.obstacles.index(obstacle))

	def draw(self, win):
		for p in self.players:
			p.draw(win)

		for o in self.obstacles:
			o.draw(win)


