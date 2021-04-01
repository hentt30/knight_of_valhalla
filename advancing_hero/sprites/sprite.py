"""
Base class to implement sprites
"""
import pygame
import os
from advancing_hero import settings


class Sprite(pygame.sprite.Sprite):
    """
    General class that represents a sprite. All the classes
    have to inherit from this class
    """
    def __init__(self, path: str, position, max_health: float = 100):
        super().__init__()
        self.image_list = []
        self.image_frame = 0
        for file in os.listdir(path):
            if file.endswith(".png"):
                self.image_list.append(
                    pygame.image.load(os.path.join(path, file)))
        self.image = self.image_list[0]
        self.surf = pygame.Surface((settings.tile_size, settings.tile_size))
        self.rect = self.surf.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]
        self.frame_counter = 0

        self.max_health = max_health
        self.current_health = max_health

    def update(self, *args, **kwargs):
        self.frame_counter += 1

