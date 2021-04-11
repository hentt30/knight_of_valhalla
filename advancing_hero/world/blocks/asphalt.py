"""
Class of asplaht block
"""
import os
from .block import Block


class Asphalt(Block):
    """
    Represents the block of asphalt
    """
    def __init__(
        self,
        settings: any,
        path: str = 'advancing_hero/images/blocks/asphalt.png',
    ) -> None:
        super().__init__(os.path.abspath(path),
                         settings,
                         settings.ASPHALT,
                         interactable=True)

    def player_interaction(self, player):
        super().player_interaction(player)
        player.speed = self.settings.ASPHALT_SPEED
