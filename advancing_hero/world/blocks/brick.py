"""
Class of brick block
"""
import os
from .block import Block


class Brick(Block):
    """
    Represents the block of brick
    """
    def __init__(
        self,
        settings: any,
        path: str = 'advancing_hero/images/png/rpgTile061.png',
    ) -> None:
        super().__init__(os.path.abspath(path),
                         settings,
                         settings.BRICK,
                         is_solid=True,
                         interactable=True)
