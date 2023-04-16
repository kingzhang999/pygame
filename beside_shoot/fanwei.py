import pygame
from pygame.sprite import Sprite

class Fan_Wei(Sprite):
	"""管理飞船所发射子弹的类"""
	def __init__(self,ai_game,x,y):
		"""在飞船所在的位置创建一个子弹对象"""
		super().__init__()#继承Sprite类
		self.screen = ai_game.screen
		self.settings = ai_game.settings
		self.color = self.settings.high_explosive_color
		self.x_zhou = x
		self.y_zhou = y

		#在(0,0)处创建子弹,再将其移到正确的位置
		self.rect = pygame.Rect(self.x_zhou,self.y_zhou,165,
			165)

		#用小数表示的子弹位置
		self.x = float(self.rect.x)

	def draw_fanwei(self):
		"""在屏幕上绘制子弹"""
		pygame.draw.rect(self.screen,self.color,self.rect)#draw.rect()在指定的地方用指定的颜色来绘制指定的Rect对象