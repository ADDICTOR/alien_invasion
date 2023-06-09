# Created on iPad.
import json
import pygame

from pygame.sprite import Group

from modules.ship import Ship
from modules.alien import Alien
from modules.button import Button
from modules.game_stats import GameStats
from modules.scoreborad import Scoreboard
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
    stats = GameStats(settings)
    sb = Scoreboard(settings, screen, stats)
    ship = Ship(settings, screen)
    play_button = Button(settings, screen, "Play")
    bullets = Group()
    aliens = Group()

    gf.create_fleet(settings, screen, ship, aliens)

    # 开始游戏主循环
    while True:
        # 监视键盘和鼠标事件
        gf.check_events(settings, screen, stats, play_button, ship, aliens, bullets)
        if stats.game_active:
            ship.update()
            gf.update_bullets(settings, screen, ship, aliens, bullets)
            gf.update_aliens(settings, stats, screen, ship, aliens, bullets)
        
        # 更新屏幕
        gf.update_screen(settings, screen, stats, sb, ship, aliens, bullets, play_button)

if __name__ == "__main__":
    main()