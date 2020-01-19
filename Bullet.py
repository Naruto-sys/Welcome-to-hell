import pygame


class Bullet(pygame.sprite.Sprite):
    """Класс пули"""
    def __init__(self, image, damage, speed, start_pos, final_pos,
                 distance, walls, hero, enemies, bull_group=-1):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()

        self.rect.x = start_pos[0]
        self.rect.y = start_pos[1]

        self.hero = hero
        self.walls = walls
        self.bull_group = bull_group
        self.enemies = enemies

        self.damage = damage
        self.speed = speed
        self.distance = distance

        self.mask = pygame.mask.from_surface(self.image)

        # рассчёт траектории полёта пули
        self.start_pos = start_pos
        self.x = self.start_pos[0] - final_pos[0]
        self.y = self.start_pos[1] - final_pos[1]

        self.final_pos = final_pos
        x1 = self.final_pos[0] - self.start_pos[0]
        y1 = self.final_pos[1] - self.start_pos[1]

        if (x1 ** 2 + y1 ** 2) ** 0.5 < self.distance:
            while (x1 ** 2 + y1 ** 2) ** 0.5 < self.distance:
                x1 += self.x / self.speed
                y1 += self.y / self.speed

            self.x = int(x1)
            self.y = int(y1)

        else:
            while (x1 ** 2 + y1 ** 2) ** 0.5 < self.distance:
                x1 += self.x / self.speed
                y1 += self.y / self.speed
            self.x = -int(x1)
            self.y = -int(y1)

        self.passed_distance = 0

    def update(self, *args):
        """Изменение положения пули при полёте"""
        self.rect.x -= self.x // self.speed
        self.rect.y -= self.y // self.speed
        self.passed_distance += ((self.x // self.speed) ** 2 +
                                 (self.y // self.speed) ** 2) ** 0.5
        if self.passed_distance > self.distance:
            self.kill()

        # проверка, вылетела ли пуля за грань экрана
        if self.x < 0:
            if self.rect.x < self.x + self.start_pos[0]:
                self.kill()

        if self.x > 0:
            if self.rect.x > self.x + self.start_pos[0]:
                self.kill()

        # проверка, не столкнулась ли пуля с объектами
        if self.bull_group == -1:
            if pygame.sprite.collide_mask(self, self.hero):
                pygame.mixer.Sound('./data/sounds/Hit.wav').play()
                self.hero.hp -= 100
                self.kill()

        for elem in self.walls:
            if pygame.sprite.collide_mask(self, elem):
                if self.bull_group != -1:
                    if elem in self.bull_group:
                        pygame.mixer.Sound('./data/sounds/Hit.wav').play()
                        elem.hp -= self.hero.damage
                    self.kill()
                else:
                    if elem not in self.enemies:
                        self.kill()
