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
        healthbars,
        max_health: float = 100,
        path: str = 'advancing_hero/images/sprites/sprite1/',
    ) -> None:
        super().__init__(path=os.path.abspath(path), position=position, max_health=max_health)
        self.animation_framerate = 120
        self.health_bar = HealthBar(parent_sprite=self, offset=(0, -32))
        healthbars.add(self.health_bar)

    def update(self):
        super().update()
        if self.frame_counter % self.animation_framerate == 0:
            self.image_frame = (self.image_frame + 1) % len(self.image_list)
            self.image = self.image_list[self.image_frame]
        if self.current_health > 0:
            self.current_health -= 0.05
        else:
            self.health_bar.kill()
            self.kill()