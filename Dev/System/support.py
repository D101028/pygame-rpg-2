from csv import reader
from os import walk

import pygame

def import_csv_layout(path):
    terrain_map = []
    with open(path) as level_map:
        layout = reader(level_map, delimiter = ',')
        for row in layout:
            terrain_map.append(list(row))
        return terrain_map

def import_folder(path):
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
