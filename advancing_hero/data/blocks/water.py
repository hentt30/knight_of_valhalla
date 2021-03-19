"""
Class of water block
"""
import os
from .block import Block


class Water(Block):
    """
    Represents the block of water
    """
    def __init__(
        self,
        settings: any,
        path: str = 'advancing_hero/images/png/rpgTile029.png',
    ):
        super().__init__(os.path.abspath(path), settings)
