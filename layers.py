import math
import random
import time

import cocos
import pyglet

click_coords: list
ui: None
timer: time
game_timer = lambda: 20 + float(timer - time.time())  # Functional programming is a beautiful thing


class HUDLayer(cocos.layer.Layer):
	bacon_label = 'Bacon:'
	bacon_coords: list
	
	def __init__(self):
		global ui
		super(HUDLayer, self).__init__()
		
		width, height = cocos.director.director.get_window_size()
		
		# Initializes and places the Bacon Score
		score_pos = (width * 0.1, height * 0.95)
		self.bacon_score = cocos.text.Label(f"{HUDLayer.bacon_label} 0",
											font_name='Arial', font_size=20,
											anchor_x='center', anchor_y='center',
											color=(255, 255, 255, 255))
		self.bacon_score.position = score_pos
		self.add(self.bacon_score, z=10)

		# Initializes and places the Timer
		timer_pos = (width * 0.95, height * 0.05)
		self.timer_label = cocos.text.Label("20.00",
											font_name='Arial', font_size=16,
											anchor_x='center', anchor_y='center',
											color=(255, 255, 255, 255))
		self.timer_label.position = timer_pos
		self.add(self.timer_label, z=10)
		
		# Starts the score at 0 and passes the conception to the global storage for the game start
		self.bacon_count = 0
		ui = self
	
	def _step(self, dt):
		global game_timer
		
		if game_timer() <= 0: # Checks if the game is over and places the Final Score label
			width, height = cocos.director.director.get_window_size()
			score_pos = (width / 2, height / 2)
			self.score_label = cocos.text.Label(f"Final Score: {self.bacon_count}",
												font_name='Arial', font_size=42,
												anchor_x='center', anchor_y='center',
												color=(0, 0, 0, 255))
			self.score_label.position = score_pos
			self.add(self.score_label, z=10)
			
			# Move the timer and score out of view, rather than destroying them, so they can be reused in a future update to the game
			self.timer_label.position = (-10, -10)
			self.bacon_score.position = (-10, -10)
		else:  # If the game isn't over, update the timer in view
			self.timer_label.element.text = "{:2.2f}".format(game_timer())
	
	def update_bacon_score(self):  # Increase the stored bacon score and show it through the label
		self.bacon_count += 1
		self.bacon_score.element.text = f"{HUDLayer.bacon_label} {self.bacon_count}"


class InputLayer(cocos.layer.Layer):  # Wrapper for user input in layers
	is_event_handler = True
	
	def __init__(self):
		global click_coords
		click_coords = []
		super(InputLayer, self).__init__()
	
	def on_mouse_press(self, x, y, buttons, modifiers):  # Stores left mouse clicks in a list to be checked by children objects
		x, y = cocos.director.director.get_virtual_coordinates(x, y)
		
		if buttons == pyglet.window.mouse.LEFT:
			global click_coords
			click_coords.append((x, y))


class OfficeLayer(InputLayer):
	bg_image_path = 'img/office.jpg'  # Yes if's a picture of the NBC's The Office set
	bg_image = pyglet.resource.image(bg_image_path)
	
	def __init__(self):
		super(OfficeLayer, self).__init__()
		
		# Initializes the location of the current bacon in a tuple of coordinates and sets the background of the game
		self.bacon_coords = tuple()
		width, height = cocos.director.director.get_window_size()
		bg = cocos.sprite.Sprite(OfficeLayer.bg_image_path, position=(width * 0.5, height * 0.5))
		bg.scale_x = width / bg.width
		bg.scale_y = height / bg.height
		self.add(bg, z=-1)
		
		self.current_bacon = None
		self.shadow = None
	
	def _step(self, dt):
		global click_coords, ui, game_timer, timer
		
		try:  # Checks if game is in a pre- or post-gameplay state
			if game_timer() <= 0 and self.shadow:
				self.shadow.position = (-2000, -2000)
				self.current_bacon.position = (-20, -20)
		except NameError:
			timer = time.time()
		
		for c_coords in click_coords:  # Check if any clicks have occurred within a 25 pixel radius of a bacon
			if not len(self.bacon_coords) == 0 and abs(math.sqrt((c_coords[0] - self.bacon_coords[0]) ** 2 + (
					c_coords[1] - self.bacon_coords[1]) ** 2)) <= 25:  # Distance formula
				ui.update_bacon_score()
				self.current_bacon.kill()
				timer = time.time()
				self.place_bacon()
		
		click_coords = []  # Clear out any click coordinates
	
	def on_mouse_motion(self, x, y, dx, dy):  # Capture cursor movement to move the shadow mask along with it
		if self.shadow is not None:
			self.shadow.x = x
			self.shadow.y = y
	
	def place_bacon(self):  # Place a piece of bacon randomly within a 25 pixel margin of the window edges
		margin = 25
		width, height = cocos.director.director.get_window_size()
		x, y, = random.randrange(margin, width - margin), random.randrange(margin, height - margin)
		self.bacon_coords = (x, y)
		new_bacon = Bacon(self.bacon_coords)
		self.add(new_bacon, z=-1)
		self.current_bacon = new_bacon
	
	def start(self):  # Initializes the timer, sets in the shadow mask, places the first piece of bacon to start the game
		global timer
		
		self.shadow = Shadow()
		self.add(self.shadow, z=2)
		self.place_bacon()
		timer = time.time()


class Bacon(cocos.sprite.Sprite):
	def __init__(self, position):
		super(Bacon, self).__init__(pyglet.resource.image('img/bacon.png'), position, 0, 0.05, 255, (255, 255, 255))


class Shadow(cocos.sprite.Sprite):
	def __init__(self):
		super(Shadow, self).__init__(pyglet.resource.image('img/mask.png'), (400, 300), 0, 1, 255, (255, 255, 255))

if __name__ == '__main__':
	assert False