import pygame.font

class Button:
	"""绘制开始按钮的类"""
	def __init__(self,ai_game,msg):
		"""初始化按钮属性"""
		self.screen = ai_game.screen
		self.screen_rect = self.screen.get_rect()

		#初始化按钮尺寸和其他属性
		self.width,self.height = 200,50
		self.color = (40,180,210)
		self.text_color = (255,255,255)
		self.text = pygame.font.SysFont(None,48)#使用默认字体和48号字体大小

		#绘制按钮的rect对象并居中
		self.rect = pygame.Rect(0,0,self.width,self.height)
		self.rect.center = self.screen_rect.center

		#创建按钮标签
		self.prep_msg(msg)

	def prep_msg(self,msg):
		"""将msg图像化,并使其在按钮上居中"""
		self.msg_image = self.text.render(msg,True,self.text_color,self.color)
		self.msg_rect = self.msg_image.get_rect()
		self.msg_rect.center = self.rect.center

	def draw_msg(self):
		"""绘制按钮和文本"""
		self.screen.fill(self.color,self.rect)
		self.screen.blit(self.msg_image,self.msg_rect)