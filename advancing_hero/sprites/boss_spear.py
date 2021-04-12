import os
from .sprite import Sprite
from .healthbar import HealthBar
import pygame
import math


class BossSpear(Sprite):
    """
    Represents the boss
    """
    def __init__(
        self,
        position,
        screen,
        max_health: float = 1000,
        path: str = 'advancing_hero/images/sprites/boss_spear/',
    ) -> None:
        super().__init__(path=os.path.abspath(path),
                         position=position,
                         max_health=max_health)
        self.screen = screen
        self.image = self.image.convert_alpha()
        self.image = pygame.transform.scale(self.image,
                                       (self.image.get_rect().width * 3,
                                        self.image.get_rect().height * 3))
        self.original_image = self.image.convert_alpha()
        self.rect = self.image.get_rect()

        self.own_surface = pygame.surface.Surface((200, 200))
        self.own_surface.set_colorkey((0, 0, 0))

        self.state = 0
        self.angle = 0

        self.speed = 15

        self.moving = False
        self.moving_position = pygame.Vector2()

        self.true_position = pygame.Vector2((self.rect.centerx, self.rect.centery))
        self.mask = pygame.mask.from_surface(self.image)

        self.damage = 20

    def update(self, player, stage):
        super().update()
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.angle += 10

        self.move()

        self.rect.centerx = int(self.true_position.x)
        self.rect.centery = int(self.true_position.y)

        self.player_collision(player)

    def player_collision(self, player):
        if pygame.sprite.collide_mask(self, player):
            player.hurt(self.damage)

    def set_position(self, x, y):
        self.true_position.x = x
        self.true_position.y = y
        self.rect.centerx = int(self.true_position.x)
        self.rect.centery = int(self.true_position.y)

    def hurt(self, damage):
        return False

    def move(self):
        if self.moving:
            distance = pygame.math.Vector2.magnitude(self.moving_position-self.true_position)
            if distance >= self.speed:
                moving_dir = pygame.math.Vector2.normalize(self.moving_position-self.true_position)
                self.true_position += self.speed * moving_dir
            else:
                self.true_position += self.moving_position-self.true_position
                self.moving = False

    def move_lance(self, position):
        self.moving = True
        self.moving_position = position