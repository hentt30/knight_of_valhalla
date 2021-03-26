import pygame
import pickle
from os import path
import json

pygame.init()

clock = pygame.time.Clock()
fps = 30

#game window
tile_size = 64
screen_cols = 16
screen_rows = 9
cols = 16
rows = 46
screen_width = tile_size * screen_cols
screen_height = (tile_size * screen_rows)

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Level Editor')

#load images
grass_img = pygame.image.load(
    path.abspath('../advancing_hero/images/png/rpgTile019.png'))

dirt_img = pygame.image.load(
    path.abspath('../advancing_hero/images/png/rpgTile026.png'))
water_img = pygame.image.load(
    path.abspath('../advancing_hero/images/png/rpgTile029.png'))

brick_img = pygame.image.load(
    path.abspath('../advancing_hero/images/png/rpgTile061.png'))

asphalt_img = pygame.image.load(
    path.abspath('../advancing_hero/images/png/rpgTile133.png'))

#define game variables
clicked = False
level = 0

#define colours
white = (255, 255, 255)
green = (144, 201, 120)
gray = (197, 194, 197)

font = pygame.font.SysFont('Futura', 24)

## Create world data and try to load existent world
world_data = []
for row in range(rows):
    r = [0] * cols
    world_data.append(r)
## Load existant world
with open('../advancing_hero/world/world.json') as world_file:
    existant_world = json.load(world_file)

existant_world.reverse()
for row_index, row in enumerate(existant_world):
    for col_index, data in enumerate(row):
        if col_index >= cols or row_index >= rows:
            raise Exception("Incompatible sizes")
        world_data[rows - row_index - 1][col_index] = data

#print(world_data)


#function for outputting text onto the screen
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def draw_grid():
    ## drawn horizontal lines
    for i in range(rows + 2):
        pygame.draw.line(screen, white, (0, i * tile_size),
                         (screen_width, i * tile_size))
    ## drawn vertical lines
    for i in range(cols + 2):
        pygame.draw.line(screen, white, (i * tile_size, 0),
                         (i * tile_size, screen_height))


def draw_world():
    for row in range(screen_rows):
        for col in range(screen_cols):
            if world_data[rows - 1 - row - level][col] > 0:
                if world_data[rows - 1 - row - level][col] == 1:
                    #dirt blocks
                    img = pygame.transform.scale(grass_img,
                                                 (tile_size, tile_size))
                    screen.blit(img, (col * tile_size,
                                      (screen_rows - 1 - row) * tile_size))
                if world_data[rows - 1 - row - level][col] == 2:
                    #grass blocks
                    img = pygame.transform.scale(dirt_img,
                                                 (tile_size, tile_size))
                    screen.blit(img, (col * tile_size,
                                      (screen_rows - 1 - row) * tile_size))
                if world_data[rows - 1 - row - level][col] == 3:
                    #enemy blocks
                    img = pygame.transform.scale(water_img,
                                                 (tile_size, tile_size))
                    screen.blit(img, (col * tile_size,
                                      (screen_rows - 1 - row) * tile_size))
                if world_data[rows - 1 - row - level][col] == 4:
                    #horizontally moving platform
                    img = pygame.transform.scale(brick_img,
                                                 (tile_size, tile_size))
                    screen.blit(img, (col * tile_size,
                                      (screen_rows - 1 - row) * tile_size))
                if world_data[rows - 1 - row - level][col] == 5:
                    #vertically moving platform
                    img = pygame.transform.scale(asphalt_img,
                                                 (tile_size, tile_size))
                    screen.blit(img, (col * tile_size,
                                      (screen_rows - 1 - row) * tile_size))


class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self):
        action = False

        #get mouse position
        pos = pygame.mouse.get_pos()

        #check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        #draw button
        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action


#main game loop
run = True
while run:

    clock.tick(fps)

    #draw background
    screen.fill(green)

    #show the grid and draw the level tiles
    draw_grid()
    draw_world()

    #text showing current level
    draw_text(f'Level: {level}', font, white, tile_size, screen_height - 60)
    draw_text('Press UP or DOWN to change level', font, white, tile_size,
              screen_height - 40)

    #event handler
    for event in pygame.event.get():
        #quit game
        if event.type == pygame.QUIT:
            with open('world.json', 'w') as outfile:
                json.dump(world_data, outfile)
            run = False
        #mouseclicks to change tiles
        if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:
            clicked = True
            pos = pygame.mouse.get_pos()
            x = pos[0] // tile_size
            y = pos[1] // tile_size
            y = screen_rows - 1 - y
            y1 = rows - 1 - y - level

            #check that the coordinates are within the tile area
            if x < cols and y1 < rows:
                #update tile value
                if pygame.mouse.get_pressed()[0] == 1:
                    world_data[y1][x] += 1
                    if world_data[y1][x] > 8:
                        world_data[y1][x] = 0
                elif pygame.mouse.get_pressed()[2] == 1:
                    world_data[y1][x] -= 1
                    if world_data[y1][x] < 0:
                        world_data[y1][x] = 8
        if event.type == pygame.MOUSEBUTTONUP:
            clicked = False
        #up and down key presses to change level number
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and level <= rows - 1 - screen_rows:
                level += 1
            elif event.key == pygame.K_DOWN and level > 0:
                level -= 1

            #print(level)

    ## update scrollbar
    #update game display window

    pygame.display.update()

pygame.quit()