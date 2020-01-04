import pygame
from load_image import load_image
import math


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_image("./mainHero/straight.jpg", color_key=-1)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

    def update(self, *args):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - self.rect.x, mouse_y - self.rect.y
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        self.image = pygame.transform.rotate(load_image("./mainHero/straight.jpg", color_key=-1), int(angle))
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 100
