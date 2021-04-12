import os
from .sprite import Sprite
import math
import pygame


class BatAttack(Sprite):
    """
    Represents a bat
    """
    def __init__(
        self,
        position,
        direction_angle,
        direction,
        screen,
        max_health: float = 100,
        path: str = 'advancing_hero/images/sprites/bat_attack/',
    ) -> None:
        super().__init__(path=os.path.abspath(path),
                         position=position,
                         max_health=max_health)
        self.direction = direction
        self.angle = direction_angle - math.pi / 2
        self.image = pygame.transform.rotate(self.image,
                                             180 * self.angle / math.pi)
        self.image = pygame.transform.scale2x(self.image)
        self.rect = self.image.get_rect()
        self.speed = 5
        self.position = position
        self.rect.centerx = position[0]
        self.rect.centery = position[1]
        self.damage = 1
        self.screen = screen

    def update(self, player, stage):
        super().update()
        if self.rect.colliderect(self.screen.get_rect()) == 0:
            self.kill()
        self.position[0] += self.speed * self.direction.x
        self.position[1] += self.speed * self.direction.y
        self.rect.x = self.position[0]
        self.rect.y = self.position[1]
        self.player_collision(player)

    def player_collision(self, player):
        if self.rect.colliderect(player.rect):
            player.hurt(self.damage)
            self.kill()
