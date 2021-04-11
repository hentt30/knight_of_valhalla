"""
Class of dirt block
"""
import os
from .block import Block


class Dirt(Block):
    """
    Represents the block of dirt
    """
    def __init__(
        self,
        settings: any,
        path: str = 'advancing_hero/images/blocks/dirt.png',
    ) -> None:
        super().__init__(os.path.abspath(path),
                         settings,
                         settings.DIRT,
                         interactable=True)

    def player_interaction(self, player):
        super().player_interaction(player)
        player.speed = self.settings.DIRT_SPEED
