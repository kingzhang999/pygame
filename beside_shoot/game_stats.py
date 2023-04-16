
class Game_Stats:
	"""跟综游戏的统计信息"""
	def __init__(self,ai_game):
		"""初始化统计信息"""
		self.settings = ai_game.settings
		self.reset_ststs()

	def reset_ststs(self):
		"""初始化在游戏期间可能变化的值"""
		self.ships_left = self.settings.ships_limit