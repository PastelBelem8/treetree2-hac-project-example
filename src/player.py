import pygame
import random

obstacle_dimensions = (39, 48)
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
		
        # The elements in the hitbox are (top left x, top left y, width, height)
		self.hitbox = pygame.Rect(self.rect)
		
		self.velocity = 3
		self.y_direction = 0

		self.score = 0
		self.has_lost = False

	def draw(self, win): 
		pygame.draw.rect(win, self.color, self.rect)

	def move(self):
		if self.has_lost: return;

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
		self.hitbox = pygame.Rect(self.rect)

	def increase_score(self):
		if self.has_lost: return;
		self.score += 1

	def hit(self):
		self.has_lost = True


class Obstacle:
	"""Represents an obstacle."""
	images = [
		pygame.transform.scale(pygame.image.load("../resources/images/bird0.png"), obstacle_dimensions),
		pygame.transform.scale(pygame.image.load("../resources/images/bird1.png"), obstacle_dimensions),
		pygame.transform.scale(pygame.image.load("../resources/images/bird2.png"), obstacle_dimensions),
		pygame.transform.scale(pygame.image.load("../resources/images/bird3.png"), obstacle_dimensions),
		pygame.transform.scale(pygame.image.load("../resources/images/bird2.PNG"), obstacle_dimensions),
		pygame.transform.scale(pygame.image.load("../resources/images/bird1.PNG"), obstacle_dimensions),
	]
	def __init__(self, x, y, vel):
		self.width, self.height = obstacle_dimensions
		self.x = x - self.width
		self.y = max(0, y - self.height)
		self.hitbox = pygame.Rect(self.x + 6, self.y + 5, self.width - 12, self.height - 10)
		self.count = -1
		self.max_count = len(Obstacle.images)
		self.vel = vel

	def update(self):
		self.count = (self.count + 1) % (self.max_count * 3) 

	def draw(self, win):
		# Defines the accurate hitbox for our character
		self.hitbox = pygame.Rect(self.x + 6, self.y + 5, self.width - 12, self.height - 10)
		# pygame.draw.rect(win, (255,0,0), self.hitbox, 2)

		# This is what will allow us to animate the saw
		self.update()
		win.blit(self.images[self.count // 3], (self.x, self.y))  

	def move(self):
		self.x -= self.vel

	def is_off_screen(self):
		return self.x < self.width // 5
        
	def hit(self):
		print("Hit!")


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

	def generate_obstacle(self, velocity=1):
		screen_width, screen_height = screen_dimensions
		# Generate obstacle on
		obstacle_y = random.randint(0, screen_height)
		self.obstacles.append(Obstacle(screen_width, obstacle_y, velocity))

	def check_collision(self, player):
		obstacles = map(lambda o: o.hitbox, self.obstacles)
		obstacle_index = player.hitbox.collidelist(list(obstacles))

		if obstacle_index != -1:
			player.hit() 
			self.obstacles[obstacle_index].hit() 
		return obstacle_index != -1

	def update(self):
		player = self.get_player()
		player.move()
		
		if self.check_collision(player):
			print(f"Player {self.player_id} has lost...")


		for obstacle in self.obstacles:
			obstacle.move()
			# If the obstacle no longer appears in the screen, remove it!
			if obstacle.is_off_screen():
				self.obstacles.pop(self.obstacles.index(obstacle))
				player.increase_score()

	def draw(self, win):
		for p in self.players:
			p.draw(win)

		for o in self.obstacles:
			o.draw(win)

	def draw_score(self, win, font):
		player = self.get_player()
		screen_width, screen_height = screen_dimensions
		# Arguments are: text, anti-aliasing, color
		score_text = font.render(f"Score: {player.score}", 1, (0,0,0)) 
		win.blit(score_text, (screen_width-40, 5))


