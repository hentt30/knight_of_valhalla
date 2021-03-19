import os
from .sprite import Sprite
import pygame


class HealthBar(Sprite):
    """
    Represents a generic health bar
    """
    def __init__(
        self,
        offset,
        parent_sprite,
        path: str = 'advancing_hero/images/sprites/healthbar/',
    ) -> None:
        super().__init__(path=os.path.abspath(path), position=(0, 0))
        self.image = pygame.transform.scale(self.image, (64, 10))
        self.rect = self.image.get_rect()
        self.parent_sprite = parent_sprite
        self.offset = offset
        self.rect.x = self.parent_sprite.rect.x+self.offset[0]
        self.rect.y = self.parent_sprite.rect.y+self.offset[1]

    def update(self):
        super().update()
        current_health = self.parent_sprite.current_health
        max_health = self.parent_sprite.max_health
        self.image = pygame.transform.scale(self.image, (round(64 * current_health / max_health), 10))
        self.rect.x = self.parent_sprite.rect.x+self.offset[0]
        self.rect.y = self.parent_sprite.rect.y+self.offset[1]
