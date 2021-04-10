import os
from .sprite import Sprite
import pygame


class OxygenBar(Sprite):
    """
    Represents a generic health bar
    """
    def __init__(
            self,
            parent_sprite,
            screen,
            path: str = 'advancing_hero/images/sprites/oxygenbar/',
    ) -> None:
        super().__init__(path=os.path.abspath(path), position=(0, 0))
        self.initial_width = 100
        self.image = pygame.transform.scale(self.image, (self.initial_width, 10))
        self.rect = self.image.get_rect()
        self.parent_sprite = parent_sprite
        self.rect.x = 2
        self.rect.y = 0
        self.screen = screen

    def update(self):
        super().update()
        current_oxygen = self.parent_sprite.current_oxygen
        max_oxygen = self.parent_sprite.max_oxygen
        self.image = pygame.transform.scale(self.image, (round(self.initial_width * current_oxygen / max_oxygen), 10))
        self.screen.blit(self.image, self.rect)