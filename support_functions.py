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

def find_city_with_largest_surplus(cities):
	max_city, surplus = None, 0
	for city in cities:
		if city.live_surplus > surplus:
			max_city, surplus = city, city.live_surplus
	return max_city

def select_closest_city_in_need(supplier, cities):
	recipient, min_dist = None, 10_000_000
	for city in cities:
		if city.live_surplus < 0 and euclidean_distance(supplier.pos, city.pos) < min_dist:
			recipient, min_dist = city, euclidean_distance(supplier.pos, city.pos)
	return recipient

def transfer_food_to_recipient(supplier, close_city):
	if abs(close_city.live_surplus) <= supplier.live_surplus:
		stock = abs(close_city.live_surplus)
	else:
		stock = supplier.live_surplus
	move_food(supplier, close_city, stock)

def move_food(supplier, recipient, stock):
	supplier.live_surplus -= stock
	recipient.live_surplus += stock
	if supplier.name in recipient.connections.keys():
		supplier.connections[recipient.name][1] += stock
		recipient.connections[supplier.name][1] += stock
	else:
		supplier.connections[recipient.name] = [recipient, stock]
		recipient.connections[supplier.name] = [supplier, stock]
