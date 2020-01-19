from Bullet import Bullet
from load_image import load_image
from coin import Coin
from rotate import rotate
import pygame
import math


class Turel(pygame.sprite.Sprite):
    def __init__(self, start_pos, frame, walls, hero, all_sprites,
                 bullets_group, enemies_group):
        super().__init__()
        self.all_sprites = all_sprites
        self.walls = walls
        self.hero = hero

        self.frame = frame
        self.image = frame
        self.mask = pygame.mask.from_surface(self.image)
        self.enemies_group = enemies_group

        self.start_pos = start_pos
        self.rect = self.image.get_rect()

        self.rect.x = start_pos[0]
        self.rect.y = start_pos[1]
        self.bullets_group = bullets_group

        self.hp = 2000

    def shooting(self, hero, s_x, s_y):
        flag = True
        self.distance = ((hero.rect.x - s_x) ** 2 +
                         (hero.rect.y - s_y) ** 2) ** 0.5
        self.x = self.start_pos[0] - hero.rect.x
        self.y = self.start_pos[1] - hero.rect.y
        x1 = self.hero.rect.x - self.start_pos[0]
        y1 = self.hero.rect.y - self.start_pos[1]
        if (x1 ** 2 + y1 ** 2) ** 0.5 < self.distance:
            while (x1 ** 2 + y1 ** 2) ** 0.5 < self.distance:
                x1 += self.x / 30
                y1 += self.y / 30

            self.x = int(x1)
            self.y = int(y1)

        else:
            while (x1 ** 2 + y1 ** 2) ** 0.5 < self.distance:
                x1 += self.x / 30
                y1 += self.y / 30
            self.x = -int(x1)
            self.y = -int(y1)

        if (x1 ** 2 + y1 ** 2) ** 0.5 < self.distance:
            while (x1 ** 2 + y1 ** 2) ** 0.5 < self.distance:
                x1 += self.x / 30
                y1 += self.y / 30

            self.x = int(x1)
            self.y = int(y1)

        else:
            while (x1 ** 2 + y1 ** 2) ** 0.5 < self.distance:
                x1 += self.x / 30
                y1 += self.y / 30
            self.x = -int(x1)
            self.y = -int(y1)

        self.passed_distance = 0

        while True:
            self.rect.x -= self.x // 30
            self.rect.y -= self.y // 30
            self.passed_distance += ((self.x // 30) ** 2 +
                                     (self.y // 30) ** 2) ** 0.5
            if self.passed_distance > self.distance:
                break
            if self.x < 0:
                if self.rect.x < self.x + self.start_pos[0]:
                    flag = False
                    break
            if self.x > 0:
                if self.rect.x > self.x + self.start_pos[0]:
                    flag = False
                    break
            for elem in self.walls:
                if pygame.sprite.collide_mask(self, elem) and \
                        elem not in self.enemies_group:
                    flag = False
                    break
        self.rect.x = s_x
        self.rect.y = s_y
        if flag:
            self.all_sprites.add(Bullet(load_image("./bullets/bullet.png", -1),
                                        20, 20, (self.rect.x + self.rect.w //
                                                 2,
                                                 self.rect.y + self.rect.h //
                                                 2),
                                        (self.hero.rect.x + self.hero.rect.w //
                                         2,
                                         self.hero.rect.y + self.hero.rect.h //
                                         2),
                                        1000, self.walls, self.hero,
                                        self.enemies_group))

    def update(self, *args):
        if self.hp <= 0:
            self.all_sprites.add(Coin((self.rect.x, self.rect.y),
                                      self.all_sprites, self.hero))
            self.kill()
            self.hero.kills += 1
            return
        self.shooting(self.hero, self.rect.x, self.rect.y)
        mouse_x, mouse_y = self.hero.rect.x + self.hero.rect.w // 2, \
                           self.hero.rect.y + + self.hero.rect.h // 2
        rel_x, rel_y = mouse_x - self.rect.x, mouse_y - self.rect.y
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        self.image, self.rect = rotate(self.frame, self.rect, int(angle))
