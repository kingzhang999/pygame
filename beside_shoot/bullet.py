import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
	"""管理飞船所发射子弹的类"""
	def __init__(self,ai_game):
		"""在飞船所在的位置创建一个子弹对象"""
		super().__init__()#继承Sprite类
		self.screen = ai_game.screen
		self.settings = ai_game.settings
		self.color = self.settings.bullet_color

		#在(0,0)处创建子弹,再将其移到正确的位置
		self.rect = pygame.Rect(0,0,self.settings.bullet_width,self.settings.bullet_height)
		self.rect.midleft = ai_game.ship.rect.midright

		#用小数表示的子弹位置
		self.x = float(self.rect.x)

	def update(self):
		"""向右移动子弹"""
		#更新表示子弹位置的小数值
		self.x += self.settings.bullet_speed
		#更新子弹的位置
		self.rect.x = self.x

	def draw_bullet(self):
		"""在屏幕上绘制子弹"""
		pygame.draw.rect(self.screen,self.color,self.rect)#draw.rect()在指定的地方用指定的颜色来绘制指定的Rect对象