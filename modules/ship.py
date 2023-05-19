"""飞船模块"""
import pygame

class Ship():

    def __init__(self, settings, screen):
        self.screen = screen
        self.speed = settings["ship_speed_factor"]

        # 加载飞船图像并获取其外接矩形
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # 定位飞船于屏幕底部中央
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        self.center = float(self.rect.centerx)

        # 移动标志
        self.moving_right = False
        self.moving_left = False

    def blitme(self):
        """指定位置绘制飞船"""
        self.screen.blit(self.image, self.rect)
    
    def update(self):
        """根据移动标志调整飞船位置"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.speed
        if self.moving_left and self.rect.left > 0:
            self.center -= self.speed
        
        self.rect.centerx = self.center

    def center_ship(self):
        self.center = self.screen_rect.centerx