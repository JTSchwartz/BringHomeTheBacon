import cocos
from cocos.scenes.transitions import FadeTRTransition

import game
import layers
import pyglet


class GameBuilder(object):
	title = "Bring Home The Bacon"
	window_width, window_height = 800, 600
	
	def __init__(self):
		super(GameBuilder, self).__init__()
		
		# Defines a newly created window of the default dimensions
		director_width = GameBuilder.window_width
		director_height = GameBuilder.window_height
		self.window = cocos.director.director.init(director_width, director_height, caption=GameBuilder.title, fullscreen=False)
		
		# Builds the Gameplay layer and anchors it in the center of the Director
		game_layer = layers.OfficeLayer()
		game_layer.anchor_x = director_width * 0.5
		game_layer.anchor_y = director_height * 0.5
		
		# Initializes the Menu
		intro_menu = IntroMenu(self)
		game_layer.add(intro_menu)
		
		self.intro_scene = cocos.scene.Scene(game_layer)
	
	def run(self):
		cocos.director.director.run(self.intro_scene)
	
	def start_game(self):  # Starts the game and hides the cursor so as to not block the view of bacon
		game_instance = game.Game()
		cocos.director.director.replace(FadeTRTransition(
			game_instance.get_scene(), 2))
		self.window.set_mouse_visible(False)
	
	@staticmethod
	def on_quit():
		pyglet.app.exit()


class IntroMenu(cocos.menu.Menu):
	
	def __init__(self, game):
		super(IntroMenu, self).__init__()
		self.game = game
		self.font_item = {
			'font_name': 'Arial',
			'font_size': 32,
			'bold': True,
			'color': (205, 97, 85, 220),
		}
		self.font_item_selected = {
			'font_name': 'Arial',
			'font_size': 42,
			'bold': True,
			'color': (123, 36, 28, 255),
		}
		
		l = [cocos.menu.MenuItem('Bring Home The Bacon', self.game.start_game),
			 cocos.menu.MenuItem('Quit', self.game.on_quit)]
		
		self.create_menu(l)


if __name__ == "__main__":
	game_builder = GameBuilder()
	game_builder.run()
