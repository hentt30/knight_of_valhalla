import os
from .sprite import Sprite
from .healthbar import HealthBar
from .monster_atack import MonsterAttack
import pygame
import math


class Monster(Sprite):
    """
    Represents a Monster
    """
    def __init__(
        self,
        position,
        screen,
        max_health: float = 100,
        path: str = 'advancing_hero/images/sprites/monster/',
    ) -> None:
        super().__init__(path=os.path.abspath(path),
                         position=position,
                         max_health=max_health)
        self.animation_framerate = 8
        self.attack_framerate = 180
        self.health_bar = HealthBar(screen=screen,
                                    parent_sprite=self,
                                    offset=(0, -32))
        self.screen = screen

    def update(self, player, stage):
        super().update()
        if self.current_health <= 0 or self.rect.colliderect(
                self.screen.get_rect()) == 0:
            self.kill()
        self.rect.y += 1
        if self.frame_counter % self.animation_framerate == 0:
            temp_rect = self.rect
            self.image_frame = (self.image_frame + 1) % (len(self.image_list) -
                                                         1)
            self.image = self.image_list[self.image_frame]
            self.rect = self.image.get_rect()
            self.rect.centerx = temp_rect.centerx
            self.rect.centery = temp_rect.centery

        self.health_bar.update()
        self.player_collision(player)

        if (self.frame_counter + 12) % self.attack_framerate == 0:
            self.image = self.image_list[-1]

        if self.frame_counter % self.attack_framerate == 0:
            self.image = self.image_list[-1]
            delta_x = player.rect.centerx - self.rect.centerx
            delta_y = player.rect.centery - self.rect.centery
            direction_angle = -math.atan2(delta_y, delta_x)
            direction = pygame.math.Vector2.normalize(
                pygame.Vector2((delta_x, delta_y)))
            position = [self.rect.centerx, self.rect.centery]
            new_projectile = MonsterAttack(
                position, direction_angle, direction,
                (player.rect.centerx, player.rect.centery))
            self.groups()[0].add(new_projectile)

    def player_collision(self, player):
        if self.rect.colliderect(player.rect):
            player.hurt(0.001)
            player.push()

    def hurt(self, damage):
        self.current_health = max(self.current_health - damage, 0)
        return True
