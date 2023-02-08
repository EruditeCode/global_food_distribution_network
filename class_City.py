import support_functions as sf

class City:
	def __init__(self, name, x, y):
		self.name = name
		self.pos = (x, y)
		self.color = (255,255,255)
		self.rad = 2

		self.population = None
		self.production = None
		self.surplus = None

	def update(self, mouse_pos, screen, font):
		self.update_color()
		self.update_radius()
		self.show_label_on_hover(mouse_pos, screen, font)

	def update_color(self):
		pass

	def update_radius(self):
		if self.production // 15_000_000 < 2:
			self.rad = 2
		else:
			self.rad = self.production // 15_000_000

	def show_label_on_hover(self, mouse_pos, screen, font):
		if sf.euclidean_distance(mouse_pos, self.pos) < self.rad:
			sf.draw_label(self.name, self.pos, screen, font)
