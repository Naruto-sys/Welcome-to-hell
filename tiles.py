import pygame
from load_image import load_image

tile_width = tile_height = 50


class Tile(pygame.sprite.Sprite):
    tiles_images = {"#": load_image("./tiles/grey_floor.jpg"),
                    "&": load_image("./tiles/light_grey_floor.jpg"),
                    "$": load_image("./tiles/warning_floor.jpg"),
                    "~": load_image("./tiles/lava.jpg"),
                    "|": load_image("./tiles/grey_floor.jpg"),
                    "\\": load_image("./tiles/brown_rock_wall.jpg"),
                    "/": load_image("./tiles/brown_sugar_rock_wall.jpg")}

    def __init__(self, tile_type, pos_x, pos_y, impassable_tiles_group, tiles_group):
        super().__init__(tiles_group)
        self.image = Tile.tiles_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        self.impassable_tiles_group = impassable_tiles_group
        self.tiles_group = tiles_group
        if tile_type in "\\|/":
            self.impassable_tiles_group.add(self)