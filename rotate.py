import pygame


def rotate(image, rect, angle):
    """Функция поворота картинки относительно её центра"""
    new_image = pygame.transform.rotate(image, angle)
    rect = new_image.get_rect(center=rect.center)
    return new_image, rect
