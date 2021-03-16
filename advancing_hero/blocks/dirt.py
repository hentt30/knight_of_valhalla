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
            path: str = 'advancing_hero/images/png/rpgTile026.png') -> None:
        super().__init__(os.path.abspath(path))
