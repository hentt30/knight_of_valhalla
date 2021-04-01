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
        path: str = 'advancing_hero/images/png/rpgTile133.png',
    ) -> None:
        super().__init__(os.path.abspath(path), settings, settings.ASPHALT)
