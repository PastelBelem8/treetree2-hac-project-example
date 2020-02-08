import pygame
from network import Network
from player import screen_dimensions, Player

# Must do it in the beginning of your program
pygame.init()

# Window size
win = pygame.display.set_mode(screen_dimensions)
pygame.display.set_caption("Hac-2020 Games")


def redrawWindow(win, player, player2):
	win.fill((255, 255, 255))
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
	while run:
		clock.tick(60)

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