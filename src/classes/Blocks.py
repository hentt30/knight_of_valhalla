import pygame 

from pygame.locals import *
from settings import *


class Blocks():

    def __init__(self, img):
        self.velocity_modifier = 0
        self.damage_to_hero = 0
        self.img = pygame.transform.scale(img, (tile_size, tile_size))
        self.img_rect = img.get_rect()

    def add_block_to_stage(self, tile_list, col_count, row_count):
        self.img_rect.x = col_count * tile_size
        self.img_rect.y = row_count * tile_size
        tile = (self.img, self.img_rect)
        tile_list.append(tile)