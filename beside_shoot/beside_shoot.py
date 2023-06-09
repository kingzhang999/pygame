import pygame
import sys
from settings import Settings
from game_stats import Game_Stats
from scoreboard import ScoreBoard
from ship import Ship
from bullet import Bullet
from button import Button
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
		self.sb = ScoreBoard(self)
		pygame.display.set_caption("Beside_Shoot")#创建标题
		pygame.display.set_icon(self.settings.biaoti)#创建图标
		self.play_button = Button(self,"Play")
		self.yuanlai = True#控制子弹种类
		self.xinzidan = False#控制子弹种类
		self.gaobao = False#控制子弹种类
		self.chuanjia = True#控制子弹种类
		self.ship = Ship(self)#创建Ship实例ps:一定要在屏幕创建以后再创建这个实例
		self.bullets_common = pygame.sprite.Group()#这里创建了一个编组
		self.bullets_armour = pygame.sprite.Group()#这里创建了一个编组
		self.bullets_explosive = pygame.sprite.Group()#这里创建了一个编组
		self.aliens = pygame.sprite.Group()#这里创建了一个编组
		self.fanweis = pygame.sprite.Group()
		self.create_fleet()

	def run_game(self):
		"""开始游戏的主循环"""
		while True:
			self.check_event()#游戏在非运行时也要执行按键检测
			if self.game.game_active:
				self.ship.move()
				self.update_bullet()
				self.update_aliens()
			self.update_screen()#游戏在非运行时也要执行屏幕刷新

	def check_event(self):
		"""检测和响应鼠标和键盘事件"""
		for event in pygame.event.get():#通过pygame.event.get()方法来获取事件
			if event.type == pygame.QUIT:
				sys.exit()#sys模块里的退出一个进程的方法
			elif event.type == pygame.KEYDOWN:
				self.check_keydown_event(event)
			elif event.type == pygame.KEYUP:
				self.check_keyup_event(event)
			elif event.type == pygame.MOUSEBUTTONDOWN:
				mouse_pos = pygame.mouse.get_pos()
				self.check_play_button(mouse_pos)
				
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
		elif event.key == pygame.K_p:
			if not self.game.game_active:
				self.game.reset_ststs()
				self.game.game_active = True
				pygame.mouse.set_visible(False)#把光标隐藏

				#清空剩余的外星人和子弹
				self.aliens.empty()
				self.bullets_common.empty()
				self.bullets_armour.empty()
				self.bullets_explosive.empty()

				#创造新的外星人并居中飞船
				self.create_fleet()
				self.aliens_num_1 = len(self.aliens.sprites())
				self.ship.center_ship()

	def check_keyup_event(self,event):
		"""响应松开"""
		if event.key == pygame.K_DOWN:
			self.ship.moving_down = False
		elif event.key == pygame.K_UP:
			self.ship.moving_up = False

	def check_play_button(self,mouse_pos):
		"""玩家单击play按钮时开始游戏"""
		button_click = self.play_button.rect.collidepoint(mouse_pos)
		if button_click and not self.game.game_active:
			self.game.reset_ststs()
			self.game.game_active = True
			pygame.mouse.set_visible(False)#把光标隐藏

			#清空剩余的外星人和子弹
			self.aliens.empty()
			self.bullets_common.empty()
			self.bullets_armour.empty()
			self.bullets_explosive.empty()

			#创造新的外星人并居中飞船
			self.create_fleet()
			self.ship.center_ship()
			self.settings.reset_settings()

	def fire_bullet(self):
		"""创建一颗子弹,确定子弹种类后再将其加到对应的编组里"""
		if self.yuanlai:
			if len(self.bullets_common) < self.settings.bullet_allowed:
				new_bullet = Bullet(self)
				self.bullets_common.add(new_bullet)
		elif self.xinzidan:
			if len(self.bullets_armour) < self.settings.armour_piercer_allowed:
				new_bullet = Armour_Piercer(self)
				self.bullets_armour.add(new_bullet)
		elif self.gaobao:
			if len(self.bullets_explosive) < self.settings.high_explosive_allowed:
				new_bullet = High_Explosive(self)
				self.bullets_explosive.add(new_bullet)

	def update_bullet(self):
		"""更新子弹的位置并删除消失的子弹"""
		#更新子弹的位置
		self.bullets_common.update()
		self.bullets_armour.update()
		self.bullets_explosive.update()
		#删除消失的子弹
		for bullete in self.bullets_common.copy():#遍历编组的副本
			if bullete.rect.x >= self.screen_rect.right:
				self.bullets_common.remove(bullete)

		for bullete in self.bullets_armour.copy():#遍历编组的副本
			if bullete.rect.x >= self.screen_rect.right:
				self.bullets_armour.remove(bullete)

		for bullete in self.bullets_explosive.copy():#遍历编组的副本
			if bullete.rect.x >= self.screen_rect.right:
				self.bullets_explosive.remove(bullete)

		self.check_bullet_alien_collisions()
		
	def check_bullet_alien_collisions(self):
		#检查是否有子弹击中外星人
		#如果有,就删除对应的目标
		collision_1 = pygame.sprite.groupcollide(self.bullets_common,self.aliens,
			self.chuanjia,True,)#接受两个编组,检测其中的元素是否碰撞,并能决定是否删除碰撞的元素
		#self.chuanjia是一个bool值,用来控制是否穿甲

		collision_2 = pygame.sprite.groupcollide(self.bullets_armour,self.aliens,
			self.chuanjia,True)#接受两个编组,检测其中的元素是否碰撞,并能决定是否删除碰撞的元素

		collision_3 = pygame.sprite.groupcollide(self.bullets_explosive,self.aliens,
			self.chuanjia,True)#接受两个编组,检测其中的元素是否碰撞,并能决定是否删除碰撞的元素

		if collision_3 and self.gaobao:
			for weizhi in collision_3.values():
				zuobiao = weizhi[0]
				fanweiss = Fan_Wei(self,zuobiao.rect.x,zuobiao.rect.y)
				self.fanweis.add(fanweiss)
			collisions = pygame.sprite.groupcollide(self.fanweis,self.aliens,True,True)
			if not collisions:
				self.game.score += self.settings.alien_point * 1
				self.sb.prep_score()
			else:
				for aliens in collisions.values():
					self.game.score += self.settings.alien_point * (len(aliens) + 1)
					self.sb.prep_score()
		if collision_1:
			for aliens in collision_1.values():
				self.game.score += self.settings.alien_point * len(aliens)
				self.sb.prep_score()
		if collision_2:
			for aliens in collision_2.values():
				self.game.score += self.settings.alien_point * len(aliens)
				self.sb.prep_score()
		if not self.aliens:#如果外星人的编组为空,则删除以下编组里的内容并创建新的外星人群
			self.bullets_common.empty()
			self.bullets_armour.empty()
			self.bullets_explosive.empty()
			self.fanweis.empty()
			self.create_fleet()
			self.settings.change_speed()

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
		if self.game.ships_left > 0:
			#飞船个数减一
			self.game.ships_left -= 1

			#清空剩余的外星人和子弹
			self.aliens.empty()
			self.bullets_common.empty()
			self.bullets_armour.empty()
			self.bullets_explosive.empty()

			#创造新的外星人并居中飞船
			self.create_fleet()
			self.ship.center_ship()

			#暂停一秒
			sleep(1)
		else:
			self.game.game_active = False
			pygame.mouse.set_visible(True)

	def check_fleet_edges(self):
		"""有外星人到达边界时采取的措施"""
		for alien in self.aliens.sprites():
			if alien.check_edges():
				self.change_fleet_direction()
				break#break是因为方向只需改变一次

	def change_fleet_direction(self):
		"""将外星人群左移并改变其方向"""
		for alien in self.aliens.sprites():#方法sprites()返回一个列表,包含编组内所有元素
			alien.rect.x -= self.settings.alien_go_spend
		self.settings.fleet_direction *= -1

	def check_aliens_bottom(self):
		"""如果外星人人到达边界时所采取的措施"""
		screen_rect = self.screen_rect
		for aliens in self.aliens.sprites():#方法sprites()返回一个列表,包含编组内所有元素
			if aliens.rect.left < 0:
				self.ship_hit()
				break#只要有一个外星人到达边界就可以停止检查了

	def update_screen(self):
		"""刷新屏幕,显示最新内容"""
		self.screen.fill(self.settings.bg_color)#fill方法:用某一种颜色填充屏幕
		self.ship.blitme()#调用Ship类里的blitme方法
		if not self.game.game_active:
			self.play_button.draw_msg()
		for bullet in self.bullets_common.sprites():#方法sprites()返回一个列表,包含编组内所有元素
			bullet.draw_bullet()#对编组里的每个元素调用方法draw_bullet()
		for bullet in self.bullets_armour.sprites():#方法sprites()返回一个列表,包含编组内所有元素
			bullet.draw_bullet()#对编组里的每个元素调用方法draw_bullet()
		for bullet in self.bullets_explosive.sprites():#方法sprites()返回一个列表,包含编组内所有元素
			bullet.draw_bullet()#对编组里的每个元素调用方法draw_bullet()
		self.aliens.draw(self.screen)
		self.sb.draw_score()
		pygame.display.flip()#刷新屏幕

if __name__ == '__main__':#当本程序直接运行的时候,运行以下代码
	bs = Beside_Shoot()
	bs.run_game()