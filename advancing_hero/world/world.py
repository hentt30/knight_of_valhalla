"""
Class that defines the World
"""
import json
import pygame


class World():
    """
    Defines the state of the world in wich
    our hero walks
    """
    def __init__(self, blocks: any, settings) -> None:
        self.tile_list = []
        self.settings = settings
        with open('advancing_hero/world/world.json') as world_file:
            self.stage_data = json.load(world_file)
        self.blocks = {
            1: blocks.Grass,
            2: blocks.Dirt,
            3: blocks.Water,
            4: blocks.Brick,
            5: blocks.Asphalt
        }

        #Converting Stage Data to blocks
        for row_index, row_element in enumerate(self.stage_data):
            for column_index, tile in enumerate(row_element):
                block = self.blocks[tile](settings=self.settings)
                self.tile_list = block.add_block_to_stage(
                    self.tile_list, column_index, row_index)

    def draw(self, screen) -> None:
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
