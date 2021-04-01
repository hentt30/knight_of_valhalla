"""
Class that defines the World
"""
import json
import pygame
from ..sprites import blocks


class World:
    """
    Defines the state of the world in which
    our hero walks
    """
    def __init__(self, settings, level_data) -> None:
        self.tile_list = []
        self.settings = settings
        with open(level_data) as world_file:
            self.stage_data = json.load(world_file)
        self.stage_data.reverse()

        self.blocks = {
            1: blocks.Grass,
            2: blocks.Dirt,
            3: blocks.Water,
            4: blocks.Brick,
            5: blocks.Asphalt
        }
        self.true_scroll = 0.0

        for row_index, row_element in enumerate(self.stage_data):
            for column_index, tile in enumerate(row_element):
                block = self.blocks[tile](settings=self.settings)
                self.tile_list = block.add_block_to_stage(
                    self.tile_list, column_index,
                    self.settings.SCREEN_ROWS - 1 - row_index)

    def draw(self, screen: any) -> None:
        """
        Draw the world accorfing to the player position

            Args:

                screen: pygame screen
        """
        if self.true_scroll <= (len(self.stage_data) -
                                self.settings.SCREEN_ROWS -
                                1) * self.settings.tile_size:
            self.true_scroll += self.settings.WORLD_SPEED
        scroll = int(self.true_scroll)

        for tile in self.tile_list:
            position = tile[1].copy()
            position.y += scroll
            screen.blit(tile[0], position)
