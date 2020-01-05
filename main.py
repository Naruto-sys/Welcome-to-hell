import os
import sys
import pygame
from Button import Button
from AnimatedSprite import AnimatedSprite
from Hero import Player
from load_image import load_image

pygame.init()
FPS = 100
WIDTH = 1080
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
player = None
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()

LEVELS = ["level1.txt",
          "level2.txt",
          "level3.txt",
          "level4.txt",
          "level5.txt"]


def terminate():
    pygame.quit()
    sys.exit()


def load_level(filename):
    fullname = os.path.join('data', filename)
    if not os.path.exists(fullname):
        print("Файла не существует!")
        terminate()
        return 0, 0, 0
    with open(fullname, 'r') as f:
        level_map = [i.strip() for i in f]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    new_player, x, y = None, None, None
    return new_player, x, y


def start_screen():
    screen.fill((0, 0, 0))
    fon = pygame.transform.scale(load_image('fon.jpeg'), (WIDTH, HEIGHT))
    fon2 = pygame.transform.scale(load_image('fon2.jpg'), (WIDTH, HEIGHT))
    fon_x1 = 0
    fon_x2 = fon.get_width()
    while True:
        clock.tick(100)
        fon_x1 -= 1.4
        fon_x2 -= 1.4
        if fon_x1 < fon.get_width() * -1:
            fon_x1 = fon.get_width()

        if fon_x2 < fon.get_width() * -1:
            fon_x2 = fon.get_width()

        screen.blit(fon, (fon_x1, 0))
        screen.blit(fon2, (fon_x2, 0))
        play_btn = Button()
        play_btn.create_button(screen, (10, 10, 10), WIDTH // 2 - 100, HEIGHT // 2 - 75, 200, 50, 1, "Play",
                               (255, 0, 0))
        rules_btn = Button()
        rules_btn.create_button(screen, (10, 10, 10), WIDTH // 2 - 100, HEIGHT // 2, 200, 50, 1, "Rules",
                                (255, 0, 0))
        exit_btn = Button()
        exit_btn.create_button(screen, (10, 10, 10), WIDTH // 2 - 100, HEIGHT // 2 + 75, 200, 50, 1, "Exit",
                               (255, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if rules_btn.pressed(event.pos):
                    rule_screen()
                if exit_btn.pressed(event.pos):
                    terminate()
                if play_btn.pressed(event.pos):
                    return
        pygame.display.flip()
        clock.tick(FPS)


def rule_screen():
    screen.fill((0, 0, 0))
    rules = ["ЛКМ - Огонь",
             "W - Вперёд",
             "A - Влево",
             "S - Назад",
             "D - Вправо",
             "E - Взаимодейтсвовать"]
    fon = pygame.transform.scale(load_image('rule_fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    back_btn = Button()
    back_btn.create_button(screen, (10, 10, 10), WIDTH // 12, HEIGHT // 2 - 50, 200, 50, 1, "Back", (255, 0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = HEIGHT // 2
    for line in rules:
        string_rendered = font.render(line, 1, pygame.Color(255, 100, 100))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = WIDTH // 12
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_btn.pressed(event.pos):
                    return
        pygame.display.flip()
        clock.tick(FPS)


def play():
    screen.fill((0, 0, 0))
    hero = Player()
    all_sprites.add(hero)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pass
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w or\
                        event.key == pygame.K_a or\
                        event.key == pygame.K_s or\
                        event.key == pygame.K_d:
                    hero.moving = True
                    hero.motions.append(event.key)
                    print(event.key)
            elif event.type == pygame.KEYUP:
                if event.key in hero.motions:
                    del hero.motions[hero.motions.index(event.key)]
                    if len(hero.motions) == 0:
                        hero.moving = False
                        hero.cur_frame = 0

        all_sprites.update()
        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(10)


if __name__ == '__main__':
    pygame.mixer.music.load('.\data\Crystals.mp3')
    pygame.mixer.music.play(loops=-1)
    start_screen()
    pygame.mixer.music.stop()
    play()
