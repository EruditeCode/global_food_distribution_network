import pygame
import support_functions as sf
from sys import exit


def main():
	pygame.init()
	WIDTH, HEIGHT = 1280, 650
	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	pygame.display.set_caption("Food Distribution Network")
	clock = pygame.time.Clock()
	font_name = "LCD-U___.ttf"

	# Create the background surface.
	bg = pygame.image.load('bg.png').convert_alpha()
	bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

	cities = sf.create_cities()

	while True:
		# MANAGING USER INPUT
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				exit()

		# DISPLAYING OBJECTS
		screen.blit(bg, (0, 0))

		# Draw the cities as circles.
		mouse_pos = pygame.mouse.get_pos()
		for city in cities:
			pygame.draw.circle(screen, city.color, city.pos, city.rad)
			city.update(mouse_pos, screen, font_name)

		pygame.display.update()
		clock.tick(30)


if __name__ == "__main__":
	main()
