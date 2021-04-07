import os
from .sprite import Sprite
import pygame


class Boomerang(Sprite):
    """
    Represents a sprite test
    """
    def __init__(
        self,
        position,
        initial_direction,
        player,
        path: str = 'advancing_hero/images/sprites/boomerang/',
    ) -> None:
        super().__init__(path=os.path.abspath(path), position=position)
        self.image = pygame.transform.scale2x(self.image_list[self.image_frame])
        self.animation_framerate = 10
        self.direction = initial_direction
        self.speed = 11
        self.acceleration = 0.2
        self.player = player
        self.state = 0

    def update(self):
        super().update()
        if self.frame_counter % self.animation_framerate == 0:
            self.image_frame = (self.image_frame + 1) % len(self.image_list)
            self.image = self.image_list[self.image_frame]
            self.image = pygame.transform.scale2x(self.image_list[self.image_frame])

        if self.state == 0:
            self.rect.x += self.speed * self.direction.x
            self.rect.y += self.speed * self.direction.y
            self.speed -= self.acceleration
            if self.speed <= 0:
                self.state = 1
        else:
            delta_x = self.player.rect.centerx - self.rect.centerx
            delta_y = self.player.rect.centery - self.rect.centery
            self.direction = pygame.Vector2((delta_x, delta_y))
            self.direction = pygame.math.Vector2.normalize(self.direction)
            self.rect.x += self.speed * self.direction.x
            self.rect.y += self.speed * self.direction.y
            self.speed += self.acceleration
            if self.rect.colliderect(self.player.rect):
                self.kill()

    def prepare_throw(self, position, direction):
        self.rect.x = position[0]
        self.rect.y = position[1]
        self.direction = direction
        self.speed = 4
        self.state = 0
