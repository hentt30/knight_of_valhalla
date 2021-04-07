import os
from .sprite import Sprite
import pygame


class Arrow(Sprite):
    """
    Represents a sprite test
    """
    def __init__(
        self,
        position,
        initial_direction,
        settings,
        path: str = 'advancing_hero/images/sprites/arrow/',
    ) -> None:
        super().__init__(path=os.path.abspath(path), position=position)
        self.settings = settings
        temp_rect = self.rect
        self.image = pygame.transform.scale2x(self.image_list[self.image_frame])
        self.animation_framerate = 10
        speed = 10
        if initial_direction == 1:
            self.speed = pygame.Vector2((0, -speed))
        elif initial_direction == 2:
            self.speed = pygame.Vector2((-speed, 0))
            self.image = pygame.transform.rotate(self.image, 90)
        elif initial_direction == 3:
            self.speed = pygame.Vector2((0, speed))
            self.image = pygame.transform.rotate(self.image, 180)
        else:
            self.speed = pygame.Vector2((speed, 0))
            self.image = pygame.transform.rotate(self.image, 270)
        self.rect = self.image.get_rect()
        self.rect.x = temp_rect.x
        self.rect.y = temp_rect.y

    def update(self):
        super().update()
        self.rect.x += self.speed.x
        self.rect.y += self.speed.y

        if not self.rect.colliderect(pygame.Rect(0, 0, self.settings.screen_width, self.settings.screen_height)):
            self.kill()
