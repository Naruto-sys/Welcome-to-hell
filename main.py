import os
import sys
import pygame
import random
from Button import Button
from Hero import Player
from load_image import load_image
from tiles import Tile
from Camera import Camera
from Bullet import Bullet

pygame.init()
FPS = 100
WIDTH = 1200
HEIGHT = 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()

player = None
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
impassable_tiles_group = pygame.sprite.Group()

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


tile_images = {"#": load_image("./tiles/grey_floor.jpg"),
               "&": load_image("./tiles/light_grey_floor.jpg"),
               "$": load_image("./tiles/warning_floor.jpg"),
               "~": load_image("./tiles/lava.jpg"),
               "|": load_image("./tiles/grey_rock_wall.jpg"),
               "\\": load_image("./tiles/brown_rock_wall.jpg"),
               "/": load_image("./tiles/brown_sugar_rock_wall.jpg")}


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] in "\\|/":
                Tile(tile_images[level[y][x]], x, y, impassable_tiles_group, tiles_group, all_sprites)
            else:
                Tile(tile_images[level[y][x]], x, y, tiles_group, all_sprites)

    return new_player, x, y


def start_screen():
    pygame.mixer.music.load('./data/Crystals.mp3')
    pygame.mixer.music.play(loops=-1)
    pygame.mixer.music.set_volume(0.9)
    screen.fill((0, 0, 0))
    fon = pygame.transform.scale(load_image('fons/menu/fon.jpeg'), (WIDTH, HEIGHT))
    fon_x1 = 0

    fons = [fon, fon, fon, fon, fon]
    fons.extend([pygame.transform.scale(load_image(f'fons/menu/fon{_}.jpg'), (WIDTH, HEIGHT)) for _ in range(2, 6)])

    while True:
        clock.tick(100)

        screen.blit(random.choice(fons), (fon_x1, 0))

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

    fon = pygame.transform.scale(load_image('fons/rule_fon.jpg'), (WIDTH, HEIGHT))
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

    pygame.mixer.music.load("./data/Paris.mp3")
    pygame.mixer.music.play(loops=-1)
    pygame.mixer.music.set_volume(0.9)
    hero = Player(impassable_tiles_group)
    a = load_level("./levels/level1.txt")
    camera = Camera(WIDTH, HEIGHT, screen, all_sprites)
    generate_level(a)
    all_sprites.add(hero)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    all_sprites.add(Bullet(load_image("bullet.png", -1), 10,
                                    20, (hero.rect.x + hero.rect.w // 2, hero.rect.y + hero.rect.h // 2),
                                    event.pos, 600, impassable_tiles_group))
                if event.button == 3:
                    pass
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w or \
                        event.key == pygame.K_a or \
                        event.key == pygame.K_s or \
                        event.key == pygame.K_d:
                    hero.moving = True
                    hero.motions.append(event.key)
                if event.key == pygame.K_ESCAPE:
                    hero.motions = []
                    hero.moving = False
                    hero.cur_frame = 0
                    flag = pause()
                    if flag == 1:
                        for elem in all_sprites:
                            elem.kill()
                        return
                    else:
                        pygame.mixer.music.set_volume(0.9)
            elif event.type == pygame.KEYUP:
                if event.key in hero.motions:
                    del hero.motions[hero.motions.index(event.key)]
                    if len(hero.motions) == 0:
                        hero.moving = False
                        hero.cur_frame = 0
        camera.update(hero)
        for sprite in all_sprites:
            camera.apply(sprite)
        all_sprites.update()
        screen.fill((0, 0, 0))
        tiles_group.draw(screen)
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(20)


def pause():
    pygame.mixer.music.set_volume(0.2)
    running = True
    while running:
        screen.fill((0, 0, 0))
        fon = pygame.transform.scale(load_image('fons/hell.jpg'), (WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))

        back_btn = Button()
        back_btn.create_button(screen, (10, 10, 10), WIDTH // 3, HEIGHT // 4 - 50, 200, 50, 1, "Resume", (255, 0, 0))

        menu_btn = Button()
        menu_btn.create_button(screen, (10, 10, 10), WIDTH // 3, HEIGHT // 4 * 2 - 50, 200, 50, 1, "Menu", (255, 0, 0))

        exit_btn = Button()
        exit_btn.create_button(screen, (10, 10, 10), WIDTH // 3, HEIGHT // 4 * 3 - 50, 200, 50, 1, "Exit", (255, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_btn.pressed(event.pos):
                    return
                elif menu_btn.pressed(event.pos):
                    anchor = warning_screen()
                    if anchor == 1:
                        return 1
                    else:
                        pygame.mixer.music.set_volume(0.2)
                elif exit_btn.pressed(event.pos):
                    terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

        pygame.display.flip()
        clock.tick(FPS)


def warning_screen():
    pygame.mixer.music.set_volume(0)
    running = True
    while running:
        fon = pygame.transform.scale(load_image('fons/warning_picture.png'), (WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))

        font = pygame.font.SysFont('Calibri', 72)
        text = font.render("Are you sure you want to get out?", 0, (255, 255, 10))
        screen.blit(text, (WIDTH // 10, HEIGHT // 4))

        back_btn = Button()
        back_btn.create_button(screen, (10, 10, 10), WIDTH // 4, HEIGHT // 2 + 150, 200, 75, 1, "BACK", (255, 0, 0))
        exit_btn = Button()
        exit_btn.create_button(screen, (10, 10, 10), WIDTH // 2, HEIGHT // 2 + 150, 200, 75, 1, "EXIT", (255, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_btn.pressed(event.pos):
                    return
                elif exit_btn.pressed(event.pos):
                    return 1
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    while True:
        start_screen()
        play()
