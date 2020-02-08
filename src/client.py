import pygame
import pygame.time

from network import Network
from player import screen_dimensions, Player


pygame.init()
# ------------------------------------------------------------
# Screen Configurations
# ------------------------------------------------------------
win = pygame.display.set_mode(screen_dimensions)
pygame.display.set_caption("Hac-2020 Games")

# ------------------------------------------------------------
## Background Configurations
# -------------------------------------------------------------
bg = pygame.image.load("../resources/images/bg1.png").convert()
bgX = 0
bgX2 = bg.get_width()

# ------------------------------------------------------------
## Game Configurations
# -------------------------------------------------------------
game_speed = 60


def update_background():
	"""Update the background to implement scrolling bockground."""
	global bgX
	global bgX2

	bgX -= 1.4  # Move both background images back
	bgX2 -= 1.4

	if bgX < bg.get_width() * -1:  # If our bg is at the -width then reset its position
		bgX = bg.get_width()

	if bgX2 < bg.get_width() * -1:
		bgX2 = bg.get_width()


def redrawWindow(win, player, player2):
	# Render backgrounds / also called blit
	win.blit(bg, (bgX, 0)) 
	win.blit(bg, (bgX2, 0))
	
	# Update obstacles 
	player.draw(win)
	player2.draw(win)

	pygame.display.update()


def main(): 
	# Game Configurations
	music = pygame.mixer.music.load('../resources/music.mp3')
	pygame.mixer.music.play(-1)

	# Game Variables
	run = True
	network = Network()
	p = network.getP()

	clock = pygame.time.Clock()
	pygame.time.set_timer(pygame.USEREVENT+1, 500) # Sets the timer for 0.5 seconds
	while run:
		clock.tick(game_speed)
		update_background()

		# Send the player, get the updated version of the game
		p2 = network.send(p)
		
		# Let's check for events (e.g., something that happens from the user)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False # Stop program

		p.move()
		redrawWindow(win, p, p2)
	pygame.quit()



main()