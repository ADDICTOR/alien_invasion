"""游戏功能模块"""
import sys

import pygame

def check_events(ship):
    """响应按键和鼠标事件"""
    for event in pygame.event.get():
        if event == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                ship.moving_right = True
            elif event.key == pygame.K_LFET:
                ship.moving_left = True
        
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                ship.moving_right = False
            elif event.key == pygame.K_LFET:
                ship.moving_left = False


def update_screen(color, screen, ship):
    """更新屏幕上的图像，并切换到新屏幕"""
    # 每次循环时重绘屏幕
    screen.fill(color)
    ship.blitme()

    # 让最近绘制的屏幕可见
    pygame.display.flip()