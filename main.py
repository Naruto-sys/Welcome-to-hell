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
from Turel import Turel
from coin import Coin

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
warring_tiles_group = pygame.sprite.Group()
lava_tiles_group = pygame.sprite.Group()
enemies_tiles_group = pygame.sprite.Group()
enemies_bullets_tiles_group = pygame.sprite.Group()
heroes_tiles_group = pygame.sprite.Group()


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
               "*": load_image("./tiles/brown_floor.jpg"),
               "&": load_image("./tiles/light_grey_floor.jpg"),
               "$": load_image("./tiles/warning_floor.jpg"),
               "~": load_image("./tiles/lava.jpg"),
               "|": load_image("./tiles/grey_rock_wall.jpg"),
               "\\": load_image("./tiles/brown_rock_wall.jpg"),
               "/": load_image("./tiles/brown_sugar_rock_wall.jpg"),
               "+": pygame.transform.scale(load_image("./turels/Turel.png", -1), (50, 50)),
               "@": pygame.transform.scale(load_image("./tiles/coin.png", -1), (50, 50))}


def generate_level(level):
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] in "\\|/":
                Tile(tile_images[level[y][x]], x, y, impassable_tiles_group, tiles_group, all_sprites)
            elif level[y][x] == '$':
                Tile(tile_images[level[y][x]], x, y, warring_tiles_group, tiles_group, all_sprites)
            elif level[y][x] == '~':
                Tile(tile_images[level[y][x]], x, y, lava_tiles_group, tiles_group, all_sprites)
            else:
                Tile(tile_images["#"], x, y, tiles_group, all_sprites)
    hero = Player(impassable_tiles_group)
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == "+":
                enemy = Turel(x, y, tile_images[level[y][x]],
                              impassable_tiles_group, hero, all_sprites, -1, enemies_tiles_group)
                impassable_tiles_group.add(enemy)
                enemies_tiles_group.add(enemy)
                all_sprites.add(enemy)
            if level[y][x] == "@":
                coin = Coin(x, y, hero)
                all_sprites.add(coin)
    return hero


def start_screen():
    pygame.mixer.music.load('./data/sounds/Crystals.mp3')
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
                    pygame.mixer.Sound('./data/sounds/Select.wav').play()
                    rule_screen()
                if exit_btn.pressed(event.pos):
                    terminate()
                if play_btn.pressed(event.pos):
                    pygame.mixer.Sound('./data/sounds/Select.wav').play()
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
                    pygame.mixer.Sound('./data/sounds/Select.wav').play()
                    return

        pygame.display.flip()
        clock.tick(FPS)


def play_level():
    win_flag = False
    level = 1
    while not win_flag:
        screen.fill((0, 0, 0))

        pygame.mixer.music.load("./data/sounds/Paris.mp3")
        pygame.mixer.music.play(loops=-1)
        pygame.mixer.music.set_volume(0.9)
        a = load_level(f"./levels/level{level}.txt")
        camera = Camera(WIDTH, HEIGHT, screen, all_sprites)
        hero = generate_level(a)
        all_sprites.add(hero)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        all_sprites.add(Bullet(load_image("./bullets/bullet.png", -1), 10,
                                               20, (hero.rect.x + hero.rect.w // 2, hero.rect.y + hero.rect.h // 2),
                                               event.pos, 600, impassable_tiles_group, hero, enemies_tiles_group, enemies_tiles_group))
                        pygame.mixer.Sound('./data/sounds/Shoot.wav').play()
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

            if pygame.sprite.spritecollideany(hero, warring_tiles_group) and level != 3:
                flag = start_new_level_screen()
                if flag:
                    for elem in all_sprites:
                        elem.kill()
                    level += 1
                    break
                else:
                    hero.motions = []
                    hero.moving = False
                    hero.rect.y -= 150

            if pygame.sprite.spritecollideany(hero, warring_tiles_group) and level == 3:
                congratulations_screen()

            if pygame.sprite.spritecollideany(hero, lava_tiles_group):
                hero.hp -= 1

            camera.update(hero)
            for sprite in all_sprites:
                camera.apply(sprite)
            all_sprites.update()
            screen.fill((0, 0, 0))
            tiles_group.draw(screen)
            all_sprites.draw(screen)

            hp = pygame.font.Font(None, 50)
            text_hp = hp.render(f"HP: {hero.hp}", 1, (255, 255, 255))
            text_hp_x = WIDTH // 13 * 11 - text_hp.get_width() // 2
            text_hp_y = HEIGHT // 12 - text_hp.get_height() // 2
            text_hp_w = text_hp.get_width()
            text_hp_h = text_hp.get_height()
            screen.blit(text_hp, (text_hp_x, text_hp_y))
            pygame.draw.rect(screen, (255, 255, 255), (text_hp_x - 10, text_hp_y - 10,
                                                       text_hp_w + 20, text_hp_h + 20), 3)

            lvl = pygame.font.Font(None, 50)
            text_lvl = lvl.render(f"Level: {level}", 1, (255, 255, 255))
            text_lvl_x = WIDTH // 13 * 2 - text_lvl.get_width() // 2
            text_lvl_y = HEIGHT // 12 - text_lvl.get_height() // 2
            text_lvl_w = text_lvl.get_width()
            text_lvl_h = text_lvl.get_height()
            screen.blit(text_lvl, (text_lvl_x, text_lvl_y))
            pygame.draw.rect(screen, (255, 255, 255), (text_lvl_x - 10, text_lvl_y - 10,
                                                       text_lvl_w + 20, text_lvl_h + 20), 3)

            coins = pygame.font.Font(None, 50)
            text_coins = coins.render(f"Coins: {hero.coins}", 1, (255, 255, 255))
            text_coins_x = WIDTH // 13 * 6.7 - text_coins.get_width() // 2
            text_coins_y = HEIGHT // 12 - text_coins.get_height() // 2
            text_coins_w = text_coins.get_width()
            text_coins_h = text_coins.get_height()
            screen.blit(text_coins, (text_coins_x, text_coins_y))
            pygame.draw.rect(screen, (255, 255, 255), (text_coins_x - 10, text_coins_y - 10,
                                                       text_coins_w + 20, text_coins_h + 20), 3)

            pygame.display.flip()
            clock.tick(20)


def congratulations_screen():
    print("Good job!")


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
                    pygame.mixer.Sound('./data/sounds/Select.wav').play()
                    return
                elif menu_btn.pressed(event.pos):
                    pygame.mixer.Sound('./data/sounds/Select.wav').play()
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
                    pygame.mixer.Sound('./data/sounds/Select.wav').play()
                    return
                elif exit_btn.pressed(event.pos):
                    pygame.mixer.Sound('./data/sounds/Select.wav').play()
                    return 1
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

        pygame.display.flip()
        clock.tick(FPS)


def start_new_level_screen():
    pygame.mixer.music.set_volume(1)
    running = True
    while running:
        fon = pygame.transform.scale(load_image('fons/warning_picture.png'), (WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))

        font = pygame.font.SysFont('Calibri', 72)
        text = font.render("Do you want to start new level?", 0, (255, 255, 10))
        screen.blit(text, (WIDTH // 10, HEIGHT // 4))

        back_btn = Button()
        back_btn.create_button(screen, (10, 10, 10), WIDTH // 4, HEIGHT // 2 + 150, 200, 75, 1, "BACK", (255, 0, 0))
        start_btn = Button()
        start_btn.create_button(screen, (10, 10, 10), WIDTH // 2, HEIGHT // 2 + 150, 200, 75, 1, "START", (255, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_btn.pressed(event.pos):
                    pygame.mixer.Sound('./data/sounds/Select.wav').play()
                    return False
                elif start_btn.pressed(event.pos):
                    pygame.mixer.Sound('./data/sounds/Select.wav').play()
                    return True

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    while True:
        start_screen()
        play_level()
