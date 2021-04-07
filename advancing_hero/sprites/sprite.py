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

        image_files = os.listdir(path)
        image_files.sort()
        for file in image_files:
            if file.endswith(".png"):
                self.image_list.append(
                    pygame.image.load(os.path.join(path, file)))
        self.image = self.image_list[0]
        self.rect = self.image.get_rect()
        self.rect.centerx = position[0]
        self.rect.centery = position[1]
        self.frame_counter = 0

        self.max_health = max_health
        self.current_health = max_health

    def update(self, *args, **kwargs):
        self.frame_counter += 1

    def hurt(self, *args, **kwargs):
        pass