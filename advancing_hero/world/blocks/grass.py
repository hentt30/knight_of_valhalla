"""
Class of grass block
"""
import os
from .block import Block


class Grass(Block):
    """
    Represents the block of grass
    """
    def __init__(
        self,
        settings,
        path: str = 'advancing_hero/images/png/rpgTile019.png',
    ) -> None:
        super().__init__(os.path.abspath(path), settings, settings.GRASS, interactable=True)

    def player_interaction(self, player):
        super().player_interaction(player)
        player.speed = self.settings.GRASS_SPEED