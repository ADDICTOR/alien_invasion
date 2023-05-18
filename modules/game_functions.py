"""游戏功能模块"""
import sys

import pygame

from .bullet import Bullet
from .alien import Alien

def check_keydown_events(event, settings, screen, ship, bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()

def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_events(settings, screen, ship, bullets):
    """响应按键和鼠标事件"""
    for event in pygame.event.get():
        if event == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, settings, screen, ship, bullets)
        
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)

def fire_bullet(settings, screen, ship, bullets):
    if len(bullets) < settings["bullet_allowed"]:
            new_bullet = Bullet(settings, screen, ship)
            bullets.add(new_bullet)

def update_screen(settings, screen, ship, aliens, bullets):
    """更新屏幕上的图像，并切换到新屏幕"""
    # 每次循环时重绘屏幕
    screen.fill(tuple(settings["background_color"]))
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)

    # 让最近绘制的屏幕可见
    pygame.display.flip()

def update_bullets(bullets):
    bullets.update()
        
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

def create_fleet(settings, screen, ship, aliens):
    alien = Alien(settings, screen)
    alien_width = alien.rect.width
    number_aliens_x = get_number_aliens_x(settings, alien_width)
    number_row = get_number_rows(settings, ship.rect.height, alien.rect.height)

    for row_number in range(number_row):
        for alien_number in range(number_aliens_x):
            create_aliens(settings, screen, aliens, alien_width, alien_number, row_number)

def get_number_aliens_x(settings, alien_width):
    available_space_x = settings["screen_width"] - alien_width * 2
    number_aliens_x = int(available_space_x / (alien_width * 2))
    return number_aliens_x

def get_number_rows(settings, ship_height, alien_height):
    available_space_y = settings["screen_height"] - alien_height * 3 - ship_height
    number_rows = int(available_space_y / (alien_height * 2))
    return number_rows

def create_aliens(settings, screen, aliens, alien_width, alien_number, row_number):
        alien = Alien(settings, screen)
        alien.x = alien_width + alien_width * alien_number * 2
        alien.rect.y = alien.rect.height + alien.rect.height * row_number * 2
        alien.rect.x = alien.x
        aliens.add(alien)
    