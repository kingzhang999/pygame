import pygame
from pygame.sprite import Sprite
import random

class Alien(Sprite):
	"""表示外星人的类"""	
	def __init__(self,ai_game):
		super().__init__()
		self.screen = ai_game.screen
		self.settings = ai_game.settings
		self.screen_rect = self.screen.get_rect()
		#加载图像并设置其rect属性
		self.image = pygame.image.load('images/alien.bmp')
		self.rect = self.image.get_rect()
		#每个外星人的最初位置
		self.rect.x = (self.rect.width)*((self.screen_rect.width//self.rect.width)-1)
		self.rect.y = random.randint(0,694)
		#存储外星人的精确竖直位置
		self.y = float(self.rect.y)

	def update(self):
		self.y += (self.settings.alien_spend * self.settings.fleet_direction)
		self.rect.y = self.y

	def check_edges(self):
		if self.rect.bottom >= (self.screen_rect.bottom - 0) or self.rect.top <=0:
			return True