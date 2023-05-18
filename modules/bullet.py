import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """子弹类"""

    def __init__(self, settings, screen, ship):
        super.__init__()
        self.settings = settings
        self.screen = screen
        self.ship = ship

        self.init()

    def init(self):
        self.rect = pygame.Rect(0, 0, self.settings["bullet_width"],
            self.settings["bullet_height"])
        self.rect.centerx = self.ship.rect.cente.rindex()
        self.rect.top = self.rect.top
        self.y = float(self.rect.y)

        self.color = self.settings["bullet_color"]
        self.speed_factor = self.settings["bullet_speed_factor"]

    def update(self):
        self.y -= self.speed_factor
        self.rect.y = self.y

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)