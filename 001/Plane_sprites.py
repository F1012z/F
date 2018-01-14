import random # 系统模块 
import pygame # 第三方模块

# 游戏屏幕的大小
SCREEN_RECT = pygame.Rect(0,0,480,700)
#敌机的定时器事件 常量
CREATE_ENEMY_EVENT = pygame.USEREVENT
#定义一个子弹的常量
HERO_FIRE_EVENT = pygame.USEREVENT + 1

class GameSprite(pygame.sprite.Sprite):
	'''游戏精灵的基类'''
	def __init__(self,image_name,speed = 1):

		#调用父类的初始化方法
		super().__init__()

		#加载图像
		self.image = pygame.image.load(image_name)

		#设置尺寸 self.image.get_rect() 返回图片的宽和高
		self.rect = self.image.get_rect()

		#记录速度
		self.speed = speed

	def update(self):

		#默认在垂直方向移动
		self.rect.y += self.speed


class Backgroup(GameSprite):
	'''背景精灵组'''
	def update(self):
		#1.调用父类的方法
		super().update()

		#判断是否移除屏幕 如果移除屏幕 将图片移动到上方
		if self.rect.y >= SCREEN_RECT.height:
			self.rect.y = -self.rect.height


class Enemy(GameSprite):
	'''敌机精灵组'''
	def __init__(self):
		#1.调用父类方法,创建敌机精灵,并且指定敌机图像
		super().__init__('/home/f/图片/feiji/enemy0.png')

		#2.设置敌机的随机初始速度
		self.speed = random.randint(1,3)

		#3.设置敌机的随机初始位置
		self.rect.bottom = 0

		max_x = SCREEN_RECT.width - self.rect.width
		self.rect.x = random.randint(0,max_x)


	def update(self):
		#1.调用父类方法 让敌机在垂直方向运动
		super().update()

		#2.判断是否飞出屏幕 如果是 需要将敌机从精灵组 删除
		if self.rect.y >= SCREEN_RECT.height:
			self.kill()


class Hero(GameSprite):
	'''英雄的精灵'''

	def __init__(self):
		super().__init__('/home/f/图片/feiji/hero1.png',0)

		#给英雄设置一个初始位置
		self.rect.centerx = SCREEN_RECT.centerx 
		self.rect.bottom = SCREEN_RECT.bottom - 120

		#创建一个子弹的精灵
		self.bullets = pygame.sprite.Group()

	def update(self):

		#super().update()
		#飞机水平移动
		self.rect.x += self.speed

		#判断飞机屏幕边界
		if self.rect.left < 0:
			self.rect.left = 0

		if self.rect.right > SCREEN_RECT.right:
			self.rect.right = SCREEN_RECT.right

	def fire(self):
		for i in (1,2,3):
			#1.创建子弹
			bullet = Bullet()
			#2.设置子弹的位置
			bullet.rect.bottom = self.rect.y - 20*i
			bullet.rect.centerx = self.rect.centerx
			#3.将子弹添加到精灵组
			self.bullets.add(bullet)


class Bullet(GameSprite):
	'''子弹精灵类'''

	def __init__(self):
		#调用父类的方法
		super().__init__('/home/f/图片/feiji/bullet1.png',-2)

	def update(self):

		super().update()

		#判断子弹是否超出屏幕 如果是 我们要让子弹从精灵组删除
		if self.rect.bottom < 0:
			self.kill()
