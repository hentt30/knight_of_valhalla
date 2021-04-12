import os
from .sprite import Sprite
import math
import pygame


class FirebatFire(Sprite):
    """
    Represents a firebat fire
    """
    def __init__(
        self,
        position,
        max_health: float = 100,
        path: str = 'advancing_hero/images/sprites/fire/',
    ) -> None:
        super().__init__(path=os.path.abspath(path),
                         position=position,
                         max_health=max_health)
        self.image = pygame.transform.scale2x(self.image)
        self.rect = self.image.get_rect()
        self.speed = 5
        self.position = position
        self.rect.centerx = position[0]
        self.rect.centery = position[1]
        self.mask = pygame.mask.from_surface(self.image)
        self.damage = 10

    def update(self, player, stage):
        super().update()
        if self.frame_counter >= 120:
            self.kill()
        if self.frame_counter % 5 == 0:
            self.image_frame = (self.image_frame + 1) % len(self.image_list)
            self.update_image(self.image_frame)
        self.player_collision(player)

    def update_image(self, index):
        temp_rect = self.rect
        self.image = self.image_list[index]
        self.image = pygame.transform.scale2x(self.image)
        self.rect = self.image.get_rect()
        self.rect.centerx = temp_rect.centerx
        self.rect.centery = temp_rect.centery

    def player_collision(self, player):
        if self.rect.colliderect(player.rect):
            player.hurt(self.damage)
            self.kill()

    def hurt(self, damage):
        return False