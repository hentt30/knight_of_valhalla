import os
from .sprite import Sprite
import math
import pygame
import math


class MonsterAttack(Sprite):
    """
    Represents a monster attack
    """
    def __init__(
        self,
        position,
        direction_angle,
        direction,
        final_position,
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
        self.damage = 8
        self.collide_player = False
        self.explosion_frame = 1
        self.explosion_duration = 5
        self.final_position = final_position
        self.stopped = False

    def update(self, player, stage):
        super().update()
        if math.dist(self.position,
                     self.final_position) > 5 and not self.stopped:
            self.position[0] += self.speed * self.direction.x
            self.position[1] += self.speed * self.direction.y
            self.rect.x = self.position[0]
            self.rect.y = self.position[1]
        else:
            self.stopped = True
            self.position[1] += stage.settings.WORLD_SPEED
            self.rect.y = self.position[1]
            self.player_collision(player)
            if self.explosion_frame % self.explosion_duration != 0 and self.collide_player:
                self.image = self.image_list[self.explosion_frame]
                self.explosion_frame += 1
            elif self.collide_player:
                self.kill()

    def player_collision(self, player):
        if self.rect.colliderect(player.rect) and not self.collide_player:
            self.collide_player = True
            self.image = self.image_list[-1]
            player.hurt(self.damage)