import os
import sys
import pygame
from Button import Button
from Hero import Player
from load_image import load_image
from tiles import Tile
from Camera import Camera

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
    pygame.mixer.music.load('.\data\Crystals.mp3')
    pygame.mixer.music.play(loops=-1)
    pygame.mixer.music.set_volume(0.9)
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

    pygame.mixer.music.load(".\data\Paris.mp3")
    pygame.mixer.music.play(loops=-1)
    pygame.mixer.music.set_volume(0.9)
    hero = Player(impassable_tiles_group)
    camera = Camera(WIDTH, HEIGHT, x=hero.rect.x, y=hero.rect.y)
    generate_level(load_level("./levels/level1.txt"))
    all_sprites.add(hero)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pass
                if event.button == 3:
                    pass
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w or \
                        event.key == pygame.K_a or \
                        event.key == pygame.K_s or \
                        event.key == pygame.K_d:
                    hero.moving = True
                    hero.motions.append(event.key)
            elif event.type == pygame.KEYUP:
                if event.key in hero.motions:
                    del hero.motions[hero.motions.index(event.key)]
                    if len(hero.motions) == 0:
                        hero.moving = False
                        hero.cur_frame = 0
                if event.key == pygame.K_ESCAPE:
                    flag = pause()
                    if flag == 1:
                        for elem in all_sprites:
                            elem.kill()
                        return
                    else:
                        pygame.mixer.music.set_volume(0.9)
        camera.update(hero)
        for sprite in all_sprites:
            camera.apply(sprite)
        all_sprites.update()
        screen.fill((0, 0, 0))
        tiles_group.draw(screen)
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(10)


def pause():
    pygame.mixer.music.set_volume(0.2)
    running = True
    while running:
        screen.fill((0, 0, 0))
        fon = pygame.transform.scale(load_image('hell.jpg'), (WIDTH, HEIGHT))
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
                    return 1
                elif exit_btn.pressed(event.pos):
                    terminate()

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    while True:
        start_screen()
        play()
