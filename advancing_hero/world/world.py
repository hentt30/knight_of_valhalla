"""
Class that defines the World
"""
import json
import pygame
from . import blocks
from .. import sprites


class World:
    """
    Defines the state of the world in which
    our hero walks
    """

    def __init__(self, settings, level_data, screen) -> None:
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
        self.screen = screen
        self.frame_counter = 0

        for row_index, row_element in enumerate(self.stage_data):
            for column_index, tile in enumerate(row_element):
                block = self.blocks[tile](settings=self.settings)
                block.add_block_to_stage(
                    self.tile_list, column_index,
                    self.settings.SCREEN_ROWS - 1 - row_index)

        self.all_enemies = pygame.sprite.Group()
        S1 = sprites.SpriteTest(position=(512, 288),
                                max_health=66,
                                screen=screen)
        S2 = sprites.SpriteTest(position=(256, 288),
                                max_health=33,
                                screen=screen)
        S3 = sprites.Bat(position=(512 + 256, 288),
                         max_health=100,
                         screen=screen)
        self.all_enemies.add(S1)
        self.all_enemies.add(S2)
        self.all_enemies.add(S3)

    def update(self, screen: any, player) -> None:
        """
        Draw the world accorfing to the player position

            Args:

                screen: pygame screen
                :param screen:
                :param player:
        """

        self.scroll_world(screen, player)

        self.all_enemies.update(player)
        self.all_enemies.draw(self.screen)

        self.frame_counter += 1

    def scroll_world(self, screen, player):
        scroll = prev_scroll = 0
        if self.frame_counter % 2 == 0:
            prev_scroll = self.true_scroll
            if self.true_scroll <= (len(self.stage_data) -
                                    self.settings.SCREEN_ROWS -
                                    1) * self.settings.tile_size:
                self.true_scroll += self.settings.WORLD_SPEED
            scroll = int(self.true_scroll)
            player.auto_scroll_down(scroll - prev_scroll)

        for tile in self.tile_list:
            if self.frame_counter % 2 == 0:
                tile[1].y += scroll - prev_scroll
            screen.blit(tile[0], tile[1])
            pygame.draw.rect(screen, (255, 255, 255), tile[1], 2)
