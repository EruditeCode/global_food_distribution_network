import support_functions as sf

class City:
	def __init__(self, name, x, y):
		self.name = name
		self.pos = (x, y)
		self.color = (255,255,255)
		self.rad = 2

	def update(self, mouse_pos, screen, font):
		self.show_label_on_hover(mouse_pos, screen, font)

	def show_label_on_hover(self, mouse_pos, screen, font):
		if sf.euclidean_distance(mouse_pos, self.pos) < self.rad:
			sf.draw_label(self.name, self.pos, screen, font)
