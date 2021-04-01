"""
Class that defines the World
"""
import json
import pygame
from . import blocks


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

        self.frame_counter = 0

        for row_index, row_element in enumerate(self.stage_data):
            for column_index, tile in enumerate(row_element):
                block = self.blocks[tile](settings=self.settings)
                block.add_block_to_stage(
                    self.tile_list, column_index,
                    self.settings.SCREEN_ROWS - 1 - row_index)

    def update(self, screen: any, player) -> None:
        """
        Draw the world accorfing to the player position

            Args:

                screen: pygame screen
        """
        scroll = prev_scroll = 0
        if self.frame_counter % 2 == 0:
            prev_scroll = self.true_scroll
            if self.true_scroll <= (len(self.stage_data) -
                                    self.settings.SCREEN_ROWS -
                                    1) * self.settings.tile_size:
                self.true_scroll += self.settings.WORLD_SPEED
            scroll = int(self.true_scroll)
            player.auto_scroll_down(scroll-prev_scroll)

        for tile in self.tile_list:
            if self.frame_counter % 2 == 0:
                tile[1].y += scroll-prev_scroll
            screen.blit(tile[0], tile[1])
            pygame.draw.rect(screen, (255, 255, 255), tile[1], 2)

        self.frame_counter += 1