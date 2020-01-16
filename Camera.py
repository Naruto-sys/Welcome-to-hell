import pygame


class Camera:
    def __init__(self, width, height, screen, all_sprites):
        self.width = width
        self.height = height
        self.dx = 0
        self.dy = 0
        self.flag_x = False
        self.flag_y = False
        self.flag_x_1 = False
        self.flag_y_1 = False
        self.screen = screen

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        if (target.rect.y + target.rect.h // 2 >= self.height // 2) and not self.flag_y:
            self.dy = -(target.rect.y + target.rect.h // 2 - self.height // 2)
            self.flag_y = True
        elif self.screen.get_at((self.width // 2, 0)) == (0, 0, 0, 255):
            self.flag_y = False
            self.dy = 0
        if (target.rect.y + target.rect.h // 2 <= self.height // 2) and not self.flag_y_1:
            self.dy = -(target.rect.y + target.rect.h // 2 - self.height // 2)
            self.flag_y_1 = True
        elif self.screen.get_at((self.width // 2, self.height - 1)) == (0, 0, 0, 255):
            self.flag_y_1 = False
            self.dy = 0
        self.dy = 0
        if self.flag_y and self.flag_y_1:
            self.dy = -(target.rect.y + target.rect.h // 2 - self.height // 2)

        if (target.rect.x + target.rect.w // 2 >= self.width // 2) and not self.flag_x:
            self.dx = -(target.rect.x + target.rect.w // 2 - self.width // 2)
            self.flag_x = True
        elif self.screen.get_at((0, self.height // 2)) == (0, 0, 0, 255):
            self.flag_x = False
            self.dx = 0
        if (target.rect.x + target.rect.w // 2 <= self.width // 2)and not self.flag_x_1:
            self.dx = -(target.rect.x + target.rect.w // 2 - self.width // 2)
            self.flag_x_1 = True
        elif self.screen.get_at((self.width - 1, self.height // 2)) == (0, 0, 0, 255):
            self.flag_x_1 = False
            self.dx = 0
        self.dx = 0
        if self.flag_x and self.flag_x_1:
            self.dx = -(target.rect.x + target.rect.w // 2 - self.width // 2)
