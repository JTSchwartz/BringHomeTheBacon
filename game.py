import cocos, layers

class Game:
	
	def __init__(self):
		super(Game, self).__init__()
		
		# Creates and begins the game
		self.game_layer = layers.OfficeLayer()
		self.game_layer.start()
		
		# Creates the Heads Up Display and places it in the window
		self.ui_layer = layers.HUDLayer()
		self.ui_layer.add(self.game_layer)
		
		self.game_scene = cocos.scene.Scene(self.ui_layer)
	
	def get_scene(self):
		return self.game_scene
	
if __name__ == '__main__':
	assert False