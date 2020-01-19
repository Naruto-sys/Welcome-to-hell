import pygame
from load_image import load_image


class Coin(pygame.sprite.Sprite):
    def __init__(self, start_pos, all_sprites, hero):
        super().__init__()

        self.image = pygame.transform.scale(load_image("./coin.png", -1),
                                            (50, 50))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = start_pos
        self.hero = hero

    def update(self, *args):
        if pygame.sprite.collide_mask(self, self.hero):
            self.hero.coins += 10
            self.kill()
