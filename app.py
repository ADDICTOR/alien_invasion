# Created on iPad.
import sys
import json
import pygame

from pygame.sprite import Group

from modules.ship import Ship
import modules.game_functions as gf

def main():
    pygame.init()
    # 读取全局设置
    with open("./config/settings.json","r",encoding="utf-8") as f:
        settings = json.load(f)

    # 屏幕大小
    screen = pygame.display.set_mode((settings["screen_width"], settings["screen_height"]))
    pygame.display.set_caption("Alien Invasion")

    # 创建飞船对象
    ship = Ship(settings, screen)
    bullets = Group()

    # 开始游戏主循环
    while True:
        # 监视键盘和鼠标事件
        gf.check_events(settings, screen, ship, bullets)
        ship.update()
        gf.update_bullets(bullets)
        
        # 更新屏幕
        gf.update_screen(settings, screen, ship, bullets)

if __name__ == "__main__":
    main()