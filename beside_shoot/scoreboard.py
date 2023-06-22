import pygame.font

class ScoreBoard:
	def __init__(self,ai_game):
		#屏幕基础属性
		self.screen = ai_game.screen
		self.screen_rect = self.screen.get_rect()
		self.settings = ai_game.settings
		self.game = ai_game.game
		#字体属性
		self.text_color = (30,30,30)
		self.font = pygame.font.SysFont(None,48)
		#准备图像
		self.prep_score()
	def prep_score(self):
		"""将得分渲染为图像"""
		score_str = str(self.game.score)
		self.score_image = self.font.render(score_str,True,self.text_color,self.settings.bg_color)
		self.score_rect = self.score_image.get_rect()
		self.score_rect.right = self.screen_rect.right - 10
		self.score_rect.top = self.screen_rect.top + 10
		
	def draw_score(self):
		"""将得分图像画在屏幕上"""
		self.screen.blit(self.score_image,self.score_rect)