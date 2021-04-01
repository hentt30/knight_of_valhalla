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
        screen,
        max_health: float = 100,
        path: str = 'advancing_hero/images/sprites/player/',
    ) -> None:
        super().__init__(path=os.path.abspath(path), position=position, max_health=max_health)
        self.speed = 5
        self.screen = screen
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
        moving_flag = False  # Handles multiple key presses
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
            dx += 1

        if dx == 0 and dy == 0:
            self.walking_framerate = 0
            # If we were walking and stopped, keep last looking to
            # the direction we were looking before
            if self.moving_direction == 1:
                self.image_frame = 7
                self.update_rect()
            if self.moving_direction == 2:
                self.image_frame = 4
                self.update_rect()
            if self.moving_direction == 3:
                self.image_frame = 1
                self.update_rect()
            if self.moving_direction == 4:
                self.image_frame = 4
                self.update_rect(flip=True)

            self.moving_direction = 0

        for tile in self.stage.tile_list:
            # Check only blocks which are on screen and are interactable
            if tile[1].bottom > 0 and tile[1].top < self.settings.screen_height and tile[2].is_interactable:
                # Check if it's solid:
                if tile[2].is_solid and (dx or dy):
                    # Check collision in x direction
                    delta_x = self.speed * dx / math.sqrt(dx*dx+dy*dy)
                    delta_y = self.speed * dy / math.sqrt(dx*dx+dy*dy)
                    if tile[1].colliderect(self.rect.x+delta_x, self.rect.y, self.rect.width, self.rect.height):
                        dx = 0
                    # Check for collision in y direction
                    if tile[1].colliderect(self.rect.x, self.rect.y+delta_y, self.rect.width, self.rect.height):
                        dy = 0

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

    def auto_scroll_down(self, scroll):
        self.rect.y += scroll
        if self.rect.bottom > self.settings.screen_height:
            self.rect.bottom = self.settings.screen_height
            for tile in self.stage.tile_list:
                # Check only blocks which are on screen and are interactable
                if tile[1].bottom > 0 and tile[1].top < self.settings.screen_height and tile[2].is_interactable:
                    # Check if it's solid:
                    if tile[2].is_solid:
                        # Player is scrolled before the blocks, so we check collision with block's rect
                        # + scroll, or, equivalently, player - scroll, now that we have already fixed player's position
                        # in case he was next to screen's bottom.
                        if tile[1].colliderect(self.rect.x, self.rect.y-scroll, self.rect.width, self.rect.height):
                            pygame.event.post(pygame.event.Event(pygame.USEREVENT, customType='title_screen'))

    def draw(self):
        self.screen.blit(self.image, self.rect)
        pygame.draw.rect(self.screen, (255, 0, 0), self.rect, 2)

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