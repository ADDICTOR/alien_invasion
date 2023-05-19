"""游戏功能模块"""
import sys
from time import sleep

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

def check_events(settings, screen, stats, play_button, ship, aliens, bullets):
    """响应按键和鼠标事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(settings, screen, stats, play_button, ship, aliens, bullets, mouse_x, mouse_y)

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, settings, screen, ship, bullets)
        
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)

def check_play_button(settings, screen, stats, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    button_clicked =  play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        initialize_dynamic_settings(settings)

        pygame.mouse.set_visible(False)
        stats.reset_stats()
        stats.game_active = True

        aliens.empty()
        bullets.empty()

        create_fleet(settings, screen, ship, aliens)
        ship.center_ship()

def initialize_dynamic_settings(settings):
    settings["ship_speed_factor"] *= settings["ship_speed_factor_dynamic"]
    settings["bullet_speed_factor"] *= settings["bullet_speed_factor_dynamic"]
    settings["alien_speed_factor"] *= settings["alien_speed_factor_dynamic"]

def fire_bullet(settings, screen, ship, bullets):
    if len(bullets) < settings["bullet_allowed"]:
            new_bullet = Bullet(settings, screen, ship)
            bullets.add(new_bullet)

def update_screen(settings, screen, stats, sb, ship, aliens, bullets, play_button):
    """更新屏幕上的图像，并切换到新屏幕"""
    # 每次循环时重绘屏幕
    screen.fill(tuple(settings["background_color"]))
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)

    sb.show_score()

    if not stats.game_active:
        play_button.draw_button()

    # 让最近绘制的屏幕可见
    pygame.display.flip()

def update_bullets(settings, screen, ship, aliens, bullets):
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collision(settings, screen, ship, aliens, bullets)

def check_bullet_alien_collision(settings, screen, ship, aliens, bullets):
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if len(aliens) == 0:
        bullets.empty()
        increase_speed(settings)
        create_fleet(settings, screen, ship, aliens)

def increase_speed(settings):
    settings["ship_speed_factor"] *= settings["speedup_scale"]
    settings["bullet_speed_factor"] *= settings["speedup_scale"]
    settings["alien_speed_factor"] *= settings["speedup_scale"]


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

def check_fleet_edges(settings, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(settings, aliens)
            break

def change_fleet_direction(settings, aliens):
    for alien in aliens.sprites():
        alien.rect.y += settings["fleet_drop_speed"]
    settings["fleet_direction"] *= -1

def ship_hit(settings, stats, screen, ship, aliens, bullets):
    if stats.ships_left > 0:
        stats.ships_left -= 1

        aliens.empty()
        bullets.empty()

        create_fleet(settings, screen, ship, aliens)
        ship.center_ship()

        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_aliens_bottom(settings, stats, screen, ship, aliens, bullets):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(settings, stats, screen, ship, aliens, bullets)
            break

def update_aliens(settings, stats, screen, ship, aliens, bullets):
    check_fleet_edges(settings, aliens)
    aliens.update()

    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(settings, stats, screen, ship, aliens, bullets)

    check_aliens_bottom(settings, stats, screen, ship, aliens, bullets)

