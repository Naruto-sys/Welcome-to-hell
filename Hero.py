import pygame
from rotate import rotate
from load_image import load_image
import math

clock = pygame.time.Clock()


class Player(pygame.sprite.Sprite):
    def __init__(self, impassable_tiles_group):
        super().__init__()
        self.step = 10
        self.frames = [load_image("./mainHero/straight.png", color_key=-1),
                       load_image("./mainHero/right3.png", color_key=-1),
                       load_image("./mainHero/right2.png", color_key=-1),
                       load_image("./mainHero/right1.png", color_key=-1),
                       load_image("./mainHero/straight.png", color_key=-1),
                       load_image("./mainHero/left3.png", color_key=-1),
                       load_image("./mainHero/left2.png", color_key=-1),
                       load_image("./mainHero/left1.png", color_key=-1)]
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.mask = pygame.mask.from_surface(self.image)
        self.impassable_tiles_group = impassable_tiles_group
        self.moving = False
        self.motions = []
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 100

        self.hp = 100000

        self.coins = 0

    def update(self):
        if self.moving:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]

        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - self.rect.x, mouse_y - self.rect.y
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        self.image, self.rect = rotate(self.frames[self.cur_frame], self.rect, int(angle))

        for elem in self.motions:
            if elem == 119:
                self.rect.y -= self.step
                for elem in self.impassable_tiles_group:
                    if pygame.sprite.collide_mask(self, elem):
                        self.rect.y += self.step
                        break
            elif elem == 115:
                self.rect.y += self.step
                for elem in self.impassable_tiles_group:
                    if pygame.sprite.collide_mask(self, elem):
                        self.rect.y -= self.step
                        break
            elif elem == 97:
                self.rect.x -= self.step
                for elem in self.impassable_tiles_group:
                    if pygame.sprite.collide_mask(self, elem):
                        self.rect.x += self.step
                        break
            elif elem == 100:
                self.rect.x += self.step
                for elem in self.impassable_tiles_group:
                    if pygame.sprite.collide_mask(self, elem):
                        self.rect.x -= self.step
                        break
        clock.tick(10)
