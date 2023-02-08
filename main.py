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

	is_supplying = False
	while True:
		# MANAGING USER INPUT
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				exit()
			if event.type == pygame.MOUSEBUTTONUP:
				is_supplying = not is_supplying

		# RUN SUPPLYING ALGORITHM
		supplier = None
		if is_supplying:
			supplier = sf.find_city_with_largest_surplus(cities)
			if supplier:
				close_city = sf.select_closest_city_in_need(supplier, cities)
				if close_city:
					sf.transfer_food_to_recipient(supplier, close_city)
				else:
					is_supplying = False
		

		# DISPLAYING OBJECTS
		screen.blit(bg, (0, 0))

		# Draw lines for supply connections between cities.
		for city in cities:
			for conn in city.connections.keys():
				connection = city.connections[conn]
				pygame.draw.aaline(screen, (255,0,0), city.pos, connection[0].pos)

		# Draw the cities as circles.
		mouse_pos = pygame.mouse.get_pos()
		for city in cities:
			pygame.draw.circle(screen, city.color, city.pos, city.rad)
			city.update(mouse_pos, screen, font_name)

		# Place a yellow circle around the present supplier city.
		if supplier:
			pygame.draw.circle(screen, (230,230,0), supplier.pos, supplier.rad+4, 1)

		pygame.display.update()
		clock.tick(30)


if __name__ == "__main__":
	main()
