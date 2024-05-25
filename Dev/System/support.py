from csv import reader
from os import walk, path

import pygame

from settings import *

def import_csv_layout(filepath) -> list[list[str]]:
    if not path.isfile(filepath):
        return []
    terrain_map = []
    with open(filepath) as level_map:
        layout = reader(level_map, delimiter = ',')
        for row in layout:
            terrain_map.append(list(row))
        return terrain_map

def import_folder(path) -> list[pygame.surface.Surface]:
    surface_list = []

    for _, __, img_files in walk(path):
        for image in img_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)

    return surface_list

def draw_text(surf: pygame.Surface, text: str, size: int, x: int | None, y: int | None, color: tuple = (255,255,255)):
        font = pygame.font.Font("../Font/font.ttf", size) # (font, size)
        text_surface = font.render(text, True, color) # (string, whether antialias, color)
        text_rect = text_surface.get_rect() # set position
        if x is None:
            x = (surf.get_width() - text_rect.width) // 2
        if y is None:
            y = (surf.get_height() - text_rect.height) // 2
        text_rect.left = x
        text_rect.top = y
        surf.blit(text_surface, text_rect) # draw

def crop_img(filepath, width = TILESIZE, height = TILESIZE) -> list[pygame.surface.Surface]:
    surf_list = []
    image = pygame.image.load(filepath).convert_alpha()
    image_height = image.get_height()
    image_width = image.get_width()
    for y in range(image_height // height):
        for x in range(image_width // width):
            surf = image.subsurface((width * x, height * y, width, height))
            surf_list.append(surf)
    return surf_list

def fill_chr(text: str, chr: str = "0", length: int = 2) -> str:
    ori_length = len(text)
    if ori_length >= length:
        return text
    return chr*(length - ori_length) + text
