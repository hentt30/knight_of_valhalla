import os
from .sprite import Sprite
from .healthbar import HealthBar
import pygame
import math


class BossFire(Sprite):
    """
    Represents the boss
    """

    def __init__(
            self,
            position,
            screen,
            initial_angle,
            max_health: float = 100,
            path: str = 'advancing_hero/images/sprites/firebat/',
    ) -> None:
        super().__init__(path=os.path.abspath(path),
                         position=position,
                         max_health=max_health)
        self.screen = screen
        self.image = pygame.transform.scale(self.image,
                                            (self.image.get_rect().width * 3,
                                             self.image.get_rect().height * 3))
        self.angle = initial_angle
        self.radius = 0

        self.angle_vel = 2
        self.radius_vel = 2
        self.angle_acc = 0.1
        self.radius_acc = 0.1

        self.retract_flag = False
        self.explode_flag = False

        self.mask = pygame.mask.from_surface(self.image)

        self.origin = pygame.Vector2((self.rect.centerx, self.rect.centery))
        self.true_position = self.origin + pygame.Vector2((
            self.radius * math.cos(self.angle * math.pi / 180), self.radius * math.sin(self.angle * math.pi / 180)))

    def update(self, player, stage):
        super().update()
        self.true_position = self.origin + pygame.Vector2((
            self.radius * math.cos(self.angle * math.pi / 180), self.radius * math.sin(self.angle * math.pi / 180)))
        self.rect.centerx = int(self.true_position.x)
        self.rect.centery = int(self.true_position.y)
        if not self.explode_flag:
            self.angle -= self.angle_vel
            if not self.retract_flag:
                self.radius += self.radius_vel
            else:
                self.radius = max(0, self.radius - self.radius_vel)
                if self.radius == 0:
                    self.explode_flag = True
            self.angle_vel += self.angle_acc
            self.radius_vel += self.radius_acc
            if self.radius_vel > 10:
                self.retract_flag = True
        else:
            self.radius += self.radius_vel
        self.player_collision(player)

    def player_collision(self, player):
        if pygame.sprite.collide_mask(self, player):
            player.hurt(10)

    def hurt(self, damage):
        return True
