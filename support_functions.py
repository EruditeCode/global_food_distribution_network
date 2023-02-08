import pygame
import json
from class_City import City
from map_ref import indices

# Basic Geometry Functions.
def euclidean_distance(point_1, point_2):
	s = 0.0
	for i in range(len(point_1)):
		s += ((point_1[i] - point_2[i]) ** 2)
	return s ** 0.5

# Basic Pygame and Display Helper Functions.
def draw_text(screen, font_name, text, size, x, y, color):
	font = pygame.font.Font(font_name, size)
	text_surface = font.render(text, True, color)
	text_rect = text_surface.get_rect()
	text_rect.topleft = (x, y)
	screen.blit(text_surface, text_rect)

def draw_label(name, pos, screen, font):
	width = len(name)*6.5 + 18
	text_surface = pygame.Surface((width, 30))
	text_surface.fill((70, 70, 70))
	text_surface.set_alpha(150)
	screen.blit(text_surface, pos)
	draw_text(screen, font, name, 14, pos[0]+7, pos[1]+8, (255,255,255))

# City Functions.
def create_cities():
	# Initialise all the cities using the City class.
	cities = [City(i[0], i[1], i[2]) for i in indices]

	# Load the population and production data.
	with open('country_populations_main.json', 'r') as file:
		populations = json.load(file)
	with open('country_production_main.json', 'r') as file:
		production = json.load(file)

	# Update each city with the loaded information.
	for city in cities:
		if city.name in populations.keys():
			city.population = int(populations[city.name])
			city.production = int(production[city.name])
			city.surplus = city.production - int(city.population * 0.55)
			city.live_surplus = city.surplus
		else:
			city.population = 100_000
			city.production = 0
			city.surplus = -55000
			city.live_surplus = city.surplus

	return cities