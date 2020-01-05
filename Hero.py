import pygame
from load_image import load_image
import math


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.step = 10
        self.frames = [load_image("./mainHero/straight.jpg", color_key=-1),
                       load_image("./mainHero/right.jpg", color_key=-1),
                       load_image("./mainHero/straight.jpg", color_key=-1),
                       load_image("./mainHero/left.jpg", color_key=-1)]
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.mask = pygame.mask.from_surface(self.image)

        self.moving = False
        self.motions = []
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

    def update(self, *args):
        if self.moving:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - self.rect.x, mouse_y - self.rect.y
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        self.image = pygame.transform.rotate(self.frames[self.cur_frame], int(angle))
        for elem in self.motions:
            if elem == 119:
                self.rect.y -= self.step
            if elem == 115:
                self.rect.y += self.step
            if elem == 97:
                self.rect.x -= self.step
            if elem == 100:
                self.rect.x += self.step

