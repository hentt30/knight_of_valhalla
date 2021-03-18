import os
from .sprite import Sprite
import pygame


class SpriteTest(Sprite):
    """
    Represents a sprite test
    """
    def __init__(
        self,
        position,
        path: str = 'advancing_hero/images/sprites/sprite1/',
    ) -> None:
        super().__init__(path=os.path.abspath(path), position=position)
        self.animation_framerate = 120

    def update(self):
        super().update()
        if self.frame_counter % self.animation_framerate == 0:
            self.image_frame = (self.image_frame + 1) % len(self.image_list)
            self.image = self.image_list[self.image_frame]