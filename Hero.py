import pygame
from load_image import load_image
import math


clock = pygame.time.Clock()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.step = 10
        self.frames = [load_image("./mainHero/straight.jpg", color_key=-1),
                       load_image("./mainHero/right_3.jpg", color_key=-1),
                       load_image("./mainHero/right_2.jpg", color_key=-1),
                       load_image("./mainHero/right_1.jpg", color_key=-1),
                       load_image("./mainHero/straight.jpg", color_key=-1),
                       load_image("./mainHero/left_3.jpg", color_key=-1),
                       load_image("./mainHero/left_2.jpg", color_key=-1),
                       load_image("./mainHero/left_1.jpg", color_key=-1)]
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.mask = pygame.mask.from_surface(self.image)

        self.moving = False
        self.motions = []
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

    def update(self):
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
            elif elem == 115:
                self.rect.y += self.step
            elif elem == 97:
                self.rect.x -= self.step
            elif elem == 100:
                self.rect.x += self.step
        clock.tick(10)