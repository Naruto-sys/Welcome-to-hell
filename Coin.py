import pygame
from load_image import load_image


class Coin(pygame.sprite.Sprite):
    """Монета - игровая валюта"""
    def __init__(self, pos_x, pos_y, hero):
        super().__init__()
        self.image = pygame.transform.scale(load_image(
            "./tiles/coin.jpg", -1), (50, 50))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos_x * 50, pos_y * 50
        self.hero = hero

    def update(self, *args):
        """"Проверка положения игрока - собрал ли игрок монету"""
        if pygame.sprite.collide_mask(self, self.hero):
            self.hero.coins += 10
            pygame.mixer.Sound('./data/sounds/Coin.wav').play()
            self.kill()
