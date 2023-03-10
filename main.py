# A global food distribution network model.

# Video Walkthrough Link: https://www.youtube.com/watch?v=tjPaQefornM

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
	is_optimising = False
	city_count = 0
	while True:
		# MANAGING USER INPUT
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				exit()
			if event.type == pygame.MOUSEBUTTONUP:
				is_supplying = not is_supplying
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					is_optimising = not is_optimising

		# RUN SUPPLYING OR OPTIMISING ALGORITHMS
		supplier = None
		if is_supplying:
			supplier = sf.find_city_with_largest_surplus(cities)
			if supplier:
				close_city = sf.select_closest_city_in_need(supplier, cities)
				if close_city:
					sf.transfer_food_to_recipient(supplier, close_city)
				else:
					is_supplying = False

		if is_optimising:
			supplier = sf.find_supplier(cities, city_count)
			if supplier:
				sf.find_and_replace_supplier_to_city(supplier, cities)
			if city_count == len(cities)-1:
				city_count = 0
			else:
				city_count += 1
		

		# DISPLAYING OBJECTS
		screen.blit(bg, (0, 0))

		# Draw lines for supply connections between cities.
		for city in cities:
			for conn in city.connections.keys():
				connection = city.connections[conn]
				color = sf.color_from_supply(connection[1])
				pygame.draw.aaline(screen, color, city.pos, connection[0].pos)

		# Draw and update the cities as circles.
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
