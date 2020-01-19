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

        self.tile_width = 50
        self.tile_height = 50

        self.frame = frame
        self.image = frame
        self.mask = pygame.mask.from_surface(self.image)
        
        self.enemies_group = enemies_group
        self.start_pos = [self.tile_width * pos_x, self.tile_height * pos_y]
        self.rect = self.image.get_rect().move(self.tile_width * pos_x, self.tile_height * pos_y)

        self.bullets_group = bullets_group

        self.hp = 2000

    def shooting(self, hero, s_x, s_y):
        flag = True
        
        self.distance = ((hero.rect.x - s_x) ** 2 + (hero.rect.y - s_y) ** 2) ** 0.5
        if self.distance > 300:
            flag = False
        if flag:
            self.all_sprites.add(Bullet(load_image("./bullets/enemy_bullet.png", -1),
                                        20, 20, (self.rect.x + self.rect.w // 2, 
                                                 self.rect.y + self.rect.h // 2),
                                        (self.hero.rect.x + self.hero.rect.w // 2,
                                         self.hero.rect.y + self.hero.rect.h // 2),
                                        300, self.walls, self.hero, self.enemies_group))

    def update(self, *args):
        if self.hp <= 0:
            self.all_sprites.add(Coin(self.rect.x / 50, self.rect.y / 50, self.hero))

            self.kill()
            self.hero.kills += 1
            return
          
        self.shooting(self.hero, self.rect.x, self.rect.y)

        mouse_x, mouse_y = self.hero.rect.x + self.hero.rect.w // 2, \
                           self.hero.rect.y + + self.hero.rect.h // 2
        rel_x, rel_y = mouse_x - self.rect.x, mouse_y - self.rect.y
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        self.image, self.rect = rotate(self.frame, self.rect, int(angle))

