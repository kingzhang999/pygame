import pygame
class Settings:
	"""管理设置的类"""
	def __init__(self):
		#屏幕设置
		self.screen_width = 1450
		self.screen_height = 750
		self.bg_color = (230,230,230)
		self.biaoti = pygame.image.load('images/tubiao.ico')

		#飞船设置
		self.ship_speed = 1.5
		self.ships_limit = 3
		
		#子弹设置
		self.bullet_color = (60,60,60)
		self.bullet_speed = 1.5
		self.bullet_width = 15
		self.bullet_height = 3
		self.bullet_allowed = 9

		#穿甲弹设置
		self.armour_piercer_color = (47,99,254)
		self.armour_piercer_speed = 2.0
		self.armour_piercer_width = 15
		self.armour_piercer_height = 3
		self.armour_piercer_allowed = 4

		#高爆弹设置
		self.high_explosive_color = (255,55,5)
		self.high_explosive_speed = 1.0
		self.high_explosive_width = 15
		self.high_explosive_height = 3
		self.high_explosive_allowed = 4

		#外星人设置
		self.alien_spend = 2
		self.alien_go_spend = 20
		self.fleet_direction = 1#self.direction等于1时往右走,等于-1时往左走