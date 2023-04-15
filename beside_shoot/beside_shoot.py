import pygame
import sys
from settings import Settings
from game_stats import Game_Stats
from ship import Ship
from bullet import Bullet
from armour_piercer import Armour_Piercer
from high_explosive import High_Explosive
from fanwei import Fan_Wei
from aliens import Alien
import random
from time import sleep
class Beside_Shoot:
	"""控制游戏所有资源的类"""
	def __init__(self):
		"""初始化游戏并创建游戏资源"""
		pygame.init()#初始化pygame
		self.settings = Settings()#创建Setting实例
		self.screen = pygame.display.set_mode((
			self.settings.screen_width,self.settings.screen_height))#创建屏幕
		self.screen_rect = self.screen.get_rect()
		self.game = Game_Stats(self)
		pygame.display.set_caption("Beside_Shoot")#创建标题
		pygame.display.set_icon(self.settings.biaoti)#创建图标
		self.yuanlai = True#控制子弹种类
		self.xinzidan = False#控制子弹种类
		self.gaobao = False
		self.chuanjia = True
		self.ship = Ship(self)#创建Ship实例ps:一定要在屏幕创建以后再创建这个实例
		self.bullets = pygame.sprite.Group()#这里创建了一个编组
		self.aliens = pygame.sprite.Group()#这里创建了一个编组
		self.fanweis = pygame.sprite.Group()
		self.create_fleet()

	def run_game(self):
		"""开始游戏的主循环"""
		while True:
			self.check_event()
			self.ship.move()
			self.update_bullet()
			self.update_aliens()
			self.update_screen()

	def check_event(self):
		"""检测和响应鼠标和键盘事件"""
		for event in pygame.event.get():#通过pygame.event.get()方法来获取事件
			if event.type == pygame.QUIT:
				sys.exit()#sys模块里的退出一个进程的方法
			elif event.type == pygame.KEYDOWN:
				self.check_keydown_event(event)
			elif event.type == pygame.KEYUP:
				self.check_keyup_event(event)
				
	def check_keydown_event(self,event):
		"""响应按键"""
		if event.key == pygame.K_q:
			sys.exit()
		elif event.key == pygame.K_DOWN:
			self.ship.moving_down = True
		elif event.key == pygame.K_UP:
			self.ship.moving_up = True
		elif event.key == pygame.K_1:
			self.yuanlai = True
			self.xinzidan = False
			self.gaobao = False
			self.chuanjia = True
		elif event.key == pygame.K_2:
			self.yuanlai = False
			self.xinzidan = True
			self.gaobao = False
			self.chuanjia = False
		elif event.key == pygame.K_3:
			self.yuanlai = False
			self.xinzidan = False
			self.gaobao = True
			self.chuanjia = True
		elif event.key == pygame.K_SPACE:
			self.fire_bullet()#每按一次空格键都会创建一个新的Bullet实例

	def check_keyup_event(self,event):
		"""响应松开"""
		if event.key == pygame.K_DOWN:
			self.ship.moving_down = False
		elif event.key == pygame.K_UP:
			self.ship.moving_up = False

	def fire_bullet(self):
		"""创建一颗子弹,确定子弹种类后再将其加到编组bullets里"""
		if self.yuanlai:
			if len(self.bullets) < self.settings.bullet_allowed:
				new_bullet = Bullet(self)
				self.bullets.add(new_bullet)
		elif self.xinzidan:
			if len(self.bullets) < self.settings.armour_piercer_allowed:
				new_bullet = Armour_Piercer(self)
				self.bullets.add(new_bullet)
		elif self.gaobao:
			if len(self.bullets) < self.settings.high_explosive_allowed:
				new_bullet = High_Explosive(self)
				self.bullets.add(new_bullet)

	def update_bullet(self):
		"""更新子弹的位置并删除消失的子弹"""
		#更新子弹的位置
		self.bullets.update()
		#删除消失的子弹
		for bullete in self.bullets.copy():#遍历编组的副本
			if bullete.rect.x >= self.screen_rect.right:
				self.bullets.remove(bullete)
		self.check_bullet_alien_collisions()
		
	def check_bullet_alien_collisions(self):
		#检查是否有子弹击中外星人
		#如果有,就删除对应的目标
		collision = pygame.sprite.groupcollide(self.bullets,self.aliens,
			self.chuanjia,True)#接受两个编组,检测其中的元素是否碰撞,并能决定是否删除碰撞的元素
		if collision and self.gaobao:
			for weizhi in collision.values():
				zuobiao = weizhi[0]
				fanweiss = Fan_Wei(self,zuobiao.rect.x,zuobiao.rect.y)
				self.fanweis.add(fanweiss)
			collisions = pygame.sprite.groupcollide(self.fanweis,self.aliens,True,True)
		if not self.aliens:#如果外星人的编组为空,则删除以下编组里的内容并创建新的外星人群
			self.bullets.empty()
			self.fanweis.empty()
			self.create_fleet()

	def update_aliens(self):
		"""更新外星人群中所有外星人的位置"""
		self.check_fleet_edges()
		self.aliens.update()
		#如果外星人与飞船发生碰撞就执行ship_hit方法
		if pygame.sprite.spritecollideany(self.ship,self.aliens):
			self.ship_hit()
		#如果外星人与边界发生碰撞就执行check_aliens_bottom()方法
		self.check_aliens_bottom()

	def create_fleet(self):
		"""创建外星人"""
		alien = Alien(self)
		alien_width,alien_height = alien.rect.size
		zhanyong_space_y = (self.settings.screen_height - 65) - (2 * alien_height)
		number_aliens_x = zhanyong_space_y // alien_height
		#计算可容纳的外星人列数
		ship_width = self.ship.rect.width
		zhanyong_space_x = (self.settings.screen_width - (3 * alien_width) - ship_width)
		number_row = zhanyong_space_x // (2*alien_width)
		#创建外星人群
		for row_number in range(random.randint(1,number_row)):
			for alien_number in range(random.randint(1,number_aliens_x - 4)):
				self.create_alien(alien_number,row_number)

	def create_alien(self,alien_number,row_number):
		"""创建外星人并放在当前列"""
		alien = Alien(self)
		alien_width,alien_height = alien.rect.size
		alien.y = alien_height + 2 * alien_height * alien_number
		alien.rect.y = alien.y
		alien.rect.x = 14 * alien.rect.height + 2 * alien.rect.height * (row_number - 2)
		self.aliens.add(alien)

	def ship_hit(self):
		"""响应飞船被撞击"""
		#飞船个数减一
		self.game.ships_left -= 1
		#清空剩余的外星人和子弹
		self.aliens.empty()
		self.bullets.empty()
		#创造新的外星人并居中飞船
		self.create_fleet()
		self.ship.center_ship()
		#暂停1秒
		sleep(1)

	def check_fleet_edges(self):
		"""有外星人到达边界时采取的措施"""
		for alien in self.aliens.sprites():
			if alien.check_edges():
				self.change_fleet_direction()
				break#break是因为方向只需改变一次

	def change_fleet_direction(self):
		"""将外星人群左移并改变其方向"""
		for alien in self.aliens.sprites():
			alien.rect.x -= self.settings.alien_go_spend
		self.settings.fleet_direction *= -1

	def check_aliens_bottom(self):
		"""如果外星人人到达边界时所采取的措施"""
		screen_rect = self.screen_rect
		for aliens in self.aliens.sprites():
			if aliens.rect.left < 0:
				self.ship_hit()
				break

	def update_screen(self):
		"""刷新屏幕,显示最新内容"""
		self.screen.fill(self.settings.bg_color)#fill方法:用某一种颜色填充屏幕
		self.ship.blitme()#调用Ship类里的blitme方法
		for bullet in self.bullets.sprites():#方法sprites()返回一个列表,包含编组内所有元素
			bullet.draw_bullet()#对编组里的每个元素调用方法draw_bullet()
		self.aliens.draw(self.screen)
		pygame.display.flip()#刷新屏幕

if __name__ == '__main__':
	bs = Beside_Shoot()
	bs.run_game()