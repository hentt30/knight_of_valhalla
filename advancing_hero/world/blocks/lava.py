"""
Class of lava block
"""
import os
from .block import Block


class Lava(Block):
    """
    Represents the block of lava
    """
    def __init__(
        self,
        settings: any,
        path: str = 'advancing_hero/images/blocks/lava.png',
    ):
        super().__init__(os.path.abspath(path),
                         settings,
                         settings.LAVA,
                         interactable=True)

    def player_interaction(self, player, *args, **kwargs):
        super().player_interaction(player)
        player.hurt(10)