import os
from .sprite import Sprite
from .healthbar import HealthBar
from .firebat_fire import FirebatFire
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
            initial_state,
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
        self.state = initial_state
        self.damage = 10

        self.angle_vel = 2
        self.radius_vel = 2
        self.angle_acc = 0.1
        self.radius_acc = 0.1

        self.timer1 = 0
        self.fly_direction = pygame.Vector2()

        self.retract_flag = False
        self.explode_flag = False

        self.mask = pygame.mask.from_surface(self.image)

        self.origin = pygame.Vector2((self.rect.centerx, self.rect.centery))
        self.true_position = self.origin + pygame.Vector2((
            self.radius * math.cos(self.angle * math.pi / 180), self.radius * math.sin(self.angle * math.pi / 180)))

    def update(self, player, stage):
        super().update()
        if self.state == 0:
            self.state0_code(player)
        elif self.state == 1:
            self.state1_code(player)

    # Rotating fire
    def state0_code(self, player):
        self.player_collision(player)
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
            if self.rect.colliderect(self.screen.get_rect()) == 0:
                self.kill()

    # Random spawning bats
    def state1_code(self, player):

        if self.image_frame <= 2:
            if self.frame_counter % 10 == 0:
                self.image_frame = self.image_frame + 1
                self.update_image(self.image_frame)
                self.timer1 = 60
        else:
            self.player_collision(player)
            if self.rect.colliderect(self.screen.get_rect()) == 0:
                self.kill()
            if self.frame_counter % 5 == 0:
                self.image_frame = ((self.image_frame + 1) % 3) + 3
                self.update_image(self.image_frame)
            if self.timer1 > 1:
                self.timer1 -= 1
            elif self.timer1 == 1:
                self.timer1 -= 1
                self.fly_direction = pygame.Vector2((
                    player.rect.centerx - self.rect.centerx,
                    player.rect.centery - self.rect.centery
                )).normalize()
            else:
                self.true_position += 7 * self.fly_direction
                self.rect.centerx = int(self.true_position.x)
                self.rect.centery = int(self.true_position.y)
                if self.frame_counter % 20 == 0:
                    if self.alive():
                        fire = FirebatFire((self.rect.centerx, self.rect.centery))
                        self.groups()[0].add(fire)

    def player_collision(self, player):
        if pygame.sprite.collide_mask(self, player):
            player.hurt(self.damage)

    def hurt(self, damage):
        return False

    def update_image(self, index):
        temp_rect = self.rect
        self.image = self.image_list[index]
        self.image = pygame.transform.scale(self.image,
                                            (self.image.get_rect().width * 3,
                                             self.image.get_rect().height * 3))
        self.rect = self.image.get_rect()
        self.rect.centerx = temp_rect.centerx
        self.rect.centery = temp_rect.centery
        self.mask = pygame.mask.from_surface(self.image)
