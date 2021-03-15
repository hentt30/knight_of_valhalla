import pygame 

from pygame.locals import *
from settings import *
from classes.Blocks import *

class World():
    
    def __init__(self, stage_data):
        self.tile_list = []

        #Adding block images
        grass_img = pygame.image.load('img/PNG/rpgTile019.png')
        dirt_img = pygame.image.load('img/PNG/rpgTile026.png')
        water_img = pygame.image.load('img/PNG/rpgTile029.png')
        brick_img = pygame.image.load('img/PNG/rpgTile061.png')
        asphalt_img = pygame.image.load('img/PNG/rpgTile133.png')
        big_brush_img = pygame.image.load('img/PNG/rpgTile155.png')
        small_brush_img = pygame.image.load('img/PNG/rpgTile156.png')

        #Converting Stage Data to blocks
        row_count = 0
        for row in stage_data:
            col_count = 0
            for tile in row:

                #Grass blocks
                if tile == 1:
                    grass = Blocks(grass_img)
                    grass.add_block_to_stage(self.tile_list, col_count, row_count)

                #Dirt Blocks
                if tile == 2:
                    dirt = Blocks(dirt_img)
                    dirt.add_block_to_stage(self.tile_list, col_count, row_count)

                #Water Blocks
                if tile == 3:
                    water = Blocks(water_img)
                    water.add_block_to_stage(self.tile_list, col_count, row_count)

                #Brick Blocks
                if tile == 4:
                    brick = Blocks(brick_img)
                    brick.add_block_to_stage(self.tile_list, col_count, row_count)

                #Asphalt Blocks
                if tile == 5:
                    asphalt = Blocks(asphalt_img)
                    asphalt.add_block_to_stage(self.tile_list, col_count, row_count)


                col_count += 1
            row_count += 1
        

    def draw(self, screen):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            


