import pygame
class Ship:
	"""管理飞船的类"""
	def __init__(self,ai_game):#ai_game这个参数可以让Ship类访问Beside_Shoot类中定义的资源
		"""初始化飞船设置"""
		self.screen = ai_game.screen
		self.settings = ai_game.settings
		self.screen_rect = self.screen.get_rect()#获得屏幕外接矩形数据
		#加载飞船图像并获得外接矩形的信息
		self.image = pygame.image.load('images/ship.bmp')#加载飞船图像
		self.rect = self.image.get_rect()#获得飞船外接矩形数据
		#将飞船生成到屏幕的左中间
		self.rect.midleft = self.screen_rect.midleft#使飞船的midleft属性和屏幕的midleft属性所代表的内容一致
		#在飞船的属性y中存储小数值
		self.y = float(self.rect.y)
		#移动标志
		self.moving_down = False
		self.moving_up = False

	def move(self):
		"""通过移动标志来控制飞船位置"""
		if self.moving_down and self.rect.y < (self.screen_rect.bottom - 56):#限制飞船的活动范围
			self.y += self.settings.ship_speed
		if self.moving_up and self.rect.y > self.screen_rect.top:#限制飞船的活动范围
			self.y -= self.settings.ship_speed
		#根据self.y更新rect对象
		self.rect.y = self.y
#因为self.rect.y才是控制飞船位置的,self.y只是为了小数的计算而设立的,所以要将计算完的self.y的值赋给self.rect.y才能实现飞船的移动
	def center_ship(self):
		self.rect.midleft = self.screen_rect.midleft
		self.y = float(self.rect.y)#将坐标信息重新归零

	def blitme(self):
		"""在指定位置画飞船"""
		self.screen.blit(self.image,self.rect)#blit方法需要输入要画什么和在哪里画