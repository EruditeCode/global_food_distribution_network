from class_City import City
from map_ref import indices


def create_cities():
	# Initialise all the cities using the City class.
	cities = [City(i[0], i[1], i[2]) for i in indices]
	return cities