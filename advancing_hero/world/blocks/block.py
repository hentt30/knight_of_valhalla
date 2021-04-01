"""
Base class to implement blocks
"""
import pygame
import os


class Block:
    """
    General class that represents a block. All the classes
    have to inherit from this class
    """
    def __init__(self, path: str, settings: any) -> None:
        """
        Loads the image
        """
        self.settings = settings
        self.velocity_modifier = 0
        self.damage_to_hero = 0
        loaded_image = pygame.image.load(path)
        self.image_scaled = pygame.transform.scale(
            loaded_image, (self.settings.tile_size, self.settings.tile_size))
        self.image_rectangle = self.image_scaled.get_rect()

    def add_block_to_stage(self, tile_list: list, column: int,
                           row: int):
        """
        Add blocks to the world

            Args:
                tile_list (list): list with the images to load the map
                column (int): index of the column where the block will be put
                row (int): index of the row where the block will be put
                
        """
        self.image_rectangle.x = column * self.settings.tile_size
        self.image_rectangle.y = row * self.settings.tile_size
        tile = (self.image_scaled, self.image_rectangle)
        tile_list.append(tile)
        return tile_list
