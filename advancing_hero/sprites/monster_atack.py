import os
from .sprite import Sprite
import math
import pygame


class MonsterAttack(Sprite):
    """
    Represents a monster attack
    """
    def __init__(
        self,
        position,
        direction_angle,
        direction,
        max_health: float = 100,
        path: str = 'advancing_hero/images/sprites/monster_attack/',
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
        self.rect.x = position[0]
        self.rect.y = position[1]
        self.damage = 1
        self.collide_player = False
        self.explosion_frame = 1
        self.explosion_duration = 5

    def update(self, player, stage):
        super().update()
        if not self.collide_player:
            self.position[0] += self.speed * self.direction.x
            self.position[1] += self.speed * self.direction.y
            self.rect.x = self.position[0]
            self.rect.y = self.position[1]
            self.player_collision(player)
        else:
            if self.explosion_frame % self.explosion_duration != 0:
                self.image = self.image_list[self.explosion_frame]
                self.explosion_frame += 1
            else:
                self.kill()

    def player_collision(self, player):
        if self.rect.colliderect(player.rect):
            self.collide_player = True
            self.image = self.image_list[-1]
            player.hurt(self.damage)