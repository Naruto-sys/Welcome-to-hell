import pygame

tile_width = tile_height = 50


class Tile(pygame.sprite.Sprite):
    """Класс тайлов - объектов текстур"""
    def __init__(self, image, pos_x, pos_y, *args):
        super().__init__(*list(args))
        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(tile_width * pos_x,
                                               tile_height * pos_y)
