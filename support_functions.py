# Functions to support the global food distribution program.

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

def color_from_supply(supply):
	rgb = int((supply / 5_000_000) * 255)
	if rgb > 240:
		rgb = 240
	elif rgb < 40:
		rgb = 40
	return (rgb,rgb,rgb)

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

def find_supplier(cities, city_count):
	for city in cities[city_count:]:
		if city.surplus > 0 and city.live_surplus > 1_000_000:
			return city

def find_and_replace_supplier_to_city(supplier, cities):
	checked_list = []
	for i in range(0, len(cities)):
		city = optimise_closest_city_in_need(supplier, cities, checked_list)
		if city:
			furthest_city = find_furthest_connection(city)
			if euclidean_distance(supplier.pos, city.pos) < euclidean_distance(furthest_city.pos, city.pos):
				replace_supplier(supplier, city, furthest_city, city.connections[furthest_city.name][1])
				return #continue
		checked_list.append(city)

def optimise_closest_city_in_need(supplier, cities, checked_list):
	recipient, min_dist = None, 10_000_000
	for city in cities:
		if city not in checked_list and city.surplus < 0 and euclidean_distance(supplier.pos, city.pos) < min_dist:
			recipient, min_dist = city, euclidean_distance(supplier.pos, city.pos)
	return recipient

def find_furthest_connection(city):
	max_city, max_distance = None, 0
	for conn in city.connections:
		if euclidean_distance(city.pos, city.connections[conn][0].pos) > max_distance:
			max_distance = euclidean_distance(city.pos, city.connections[conn][0].pos)
			max_city = city.connections[conn][0]
	return max_city

def replace_supplier(supplier, city, furthest_city, stock):
	if stock <= supplier.live_surplus:
		move_food(supplier, city, stock)
		move_food(furthest_city, city, -stock)
		del furthest_city.connections[city.name]
		del city.connections[furthest_city.name]
	else:
		stock = supplier.live_surplus
		move_food(supplier, city, stock)
		move_food(furthest_city, city, -stock)
