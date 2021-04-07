import os
from .sprite import Sprite
from .healthbar import HealthBar


class SpriteTest(Sprite):
    """
    Represents a sprite test
    """
    def __init__(
        self,
        position,
        screen,
        max_health: float = 100,
        path: str = 'advancing_hero/images/sprites/sprite1/',
    ) -> None:
        super().__init__(path=os.path.abspath(path), position=position, max_health=max_health)
        self.animation_framerate = 15
        self.health_bar = HealthBar(screen=screen, parent_sprite=self, offset=(0, -48))

    def update(self, player):
        super().update()
        self.health_bar.update()

        if self.frame_counter % self.animation_framerate == 0:
            self.image_frame = (self.image_frame + 1) % len(self.image_list)
            self.image = self.image_list[self.image_frame]
        if self.current_health > 0:
            self.current_health -= 0.5
        else:
            self.kill()