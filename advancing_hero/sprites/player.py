import os
from .sprite import Sprite
import pygame
import math
from enum import Enum


#DOWN = 1
#SIDE = 4
#UP = 7


class Player(Sprite):
    """
    Represents a sprite test
    """
    def __init__(
        self,
        position,
        settings,
        stage,
        max_health: float = 100,
        path: str = 'advancing_hero/images/sprites/player/',
    ) -> None:
        super().__init__(path=os.path.abspath(path), position=position, max_health=max_health)
        self.speed = 5
        self.settings = settings
        self.stage = stage
        self.image_frame = 1
        self.update_rect()
        self.walking_framerate = 0
        self.moving_direction = 0

    def update(self):
        super().update()
        self.handle_movement()

    def handle_movement(self):
        dx = 0
        dy = 0
        moving_flag = False # Handles multiple key presses
        key = pygame.key.get_pressed()
        if key[pygame.K_w]:
            self.walk_animation(7, 1)
            moving_flag = True
            dy -= 1
        if key[pygame.K_a]:
            if not moving_flag:
                self.walk_animation(4, 2)
            moving_flag = True
            dx -= 1
        if key[pygame.K_s]:
            if not moving_flag:
                self.walk_animation(1, 3)
            moving_flag = True
            dy += 1
        if key[pygame.K_d]:
            if not moving_flag:
                self.walk_animation(4, 4, flip=True)
            moving_flag = True
            dx += 1

        if dx == 0 and dy == 0:
            self.walking_framerate = 0
            # If we were walking and stopped, keep last looking to
            # the direction we were looking before
            if (self.moving_direction == 1):
                self.image_frame = 7
                self.update_rect()
            if (self.moving_direction == 2):
                self.image_frame = 4
                self.update_rect()
            if (self.moving_direction == 3):
                self.image_frame = 1
                self.update_rect()
            if (self.moving_direction == 4):
                self.image_frame = 4
                self.update_rect(flip=True)

            self.moving_direction = 0

        if dx or dy:
            self.rect.x += self.speed * dx / math.sqrt(dx*dx+dy*dy)
            self.rect.y += self.speed * dy / math.sqrt(dx*dx+dy*dy)

        if self.rect.bottom > self.settings.screen_height:
            self.rect.bottom = self.settings.screen_height
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.right > self.settings.screen_width:
            self.rect.right = self.settings.screen_width
        if self.rect.left < 0:
            self.rect.left = 0

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)

    def walk_animation(self, still_frame, direction, flip=False):
        if self.walking_framerate == 0:
            self.image_frame = still_frame-1
            self.update_rect(flip)
        elif self.walking_framerate == 15 or self.walking_framerate == 45:
            self.image_frame = still_frame
            self.update_rect(flip)
        elif self.walking_framerate == 30:
            self.image_frame = still_frame+1
            self.update_rect(flip)
        self.moving_direction = direction
        self.walking_framerate = (self.walking_framerate + 1) % 60

    def update_rect(self, flip=False):
        temp_rect = self.rect
        self.image = self.image_list[self.image_frame]
        self.image = pygame.transform.scale2x(self.image)
        if flip:
            self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()
        self.rect.x = temp_rect.x
        self.rect.y = temp_rect.y