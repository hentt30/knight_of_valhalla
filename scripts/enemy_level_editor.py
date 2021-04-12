## Editor for enemies in the game :)
import pygame
import math
import pickle
from os import path
import json
##### ENEMIES - ÚNICA PARTE EDITÁVEL DO CÓDIGO ###########
enemy_name = 'boss'
enemies_available = {
    'bat_sprite':
    pygame.image.load(
        path.abspath('../advancing_hero/images/sprites/bat/frame1.png')),
    'monster_sprite':
    pygame.image.load(
        path.abspath('../advancing_hero/images/sprites/monster/frame1.png')),
    'potion_heal':
    pygame.image.load(
        path.abspath(
            '../advancing_hero/images/sprites/potion_heal/red_potion.png')),
    'ship_sprite':
    pygame.image.load(
        path.abspath('../advancing_hero/images/sprites/ship/frame1.png')),
    'boss':
        pygame.image.load(
            path.abspath('../advancing_hero/images/sprites/boss/a.png'))
}
###########################################################

pygame.init()
BLUE = (0, 0, 255)
clock = pygame.time.Clock()
fps = 30

#game window
tile_size = 64
screen_cols = 16
screen_rows = 9
cols = 16
rows = 45
screen_width = tile_size * screen_cols
screen_height = (tile_size * screen_rows)

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Enemies Level Editor')

#load images
grass_img = pygame.image.load(
    path.abspath('../advancing_hero/images/blocks/grass.png'))

dirt_img = pygame.image.load(
    path.abspath('../advancing_hero/images/blocks/dirt.png'))
water_img = pygame.image.load(
    path.abspath('../advancing_hero/images/blocks/water.png'))

brick_img = pygame.image.load(
    path.abspath('../advancing_hero/images/blocks/brick.png'))

asphalt_img = pygame.image.load(
    path.abspath('../advancing_hero/images/blocks/asphalt.png'))

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
#./advancing_hero/world
with open('../advancing_hero/world/world.json') as world_file:
    existant_world = json.load(world_file)
aux = existant_world
enemies = existant_world['sprite_data']
existant_world = existant_world['block_data']

existant_world.reverse()
for row_index, row in enumerate(existant_world):
    for col_index, data in enumerate(row):
        if col_index < cols and row_index < rows:
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


def draw_enemies():
    #print(len(enemies))
    for _, sprite_element in enumerate(reversed(enemies)):
        d = screen_height - sprite_element[2] + level * 64

        if 0 <= d <= screen_height:
            img = enemies_available[sprite_element[0]]
            aux = sprite_element[2]
            if sprite_element[2] > screen_height:
                aux = (screen_height - sprite_element[2])
            screen.blit(img, (sprite_element[1], aux + level * 64))
            pygame.draw.circle(screen, BLUE,
                               (sprite_element[1], aux + level * 64), 10)


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
    draw_enemies()

    #text showing current level
    draw_text(f'Level: {level}', font, white, tile_size, screen_height - 60)
    draw_text('Press UP or DOWN to change level', font, white, tile_size,
              screen_height - 40)

    #event handler
    for event in pygame.event.get():
        #quit game
        if event.type == pygame.QUIT:
            with open('world.json', 'w') as outfile:
                aux['block_data'] = world_data
                aux['sprite_data'] = enemies
                json.dump(aux, outfile)
            run = False
        #mouseclicks to change tiles
        if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:
            clicked = True
            pos = pygame.mouse.get_pos()
            x = pos[0]
            y = pos[1]
            new_y = y + level * 64

            if new_y > screen_height:
                new_y = screen_height - y + level * 64

            a = []
            for index, enemy in enumerate(enemies):
                if math.dist([x, new_y], [enemy[1], enemy[2]]) < 10:
                    continue
                else:
                    a.append(enemy)

            if len(a) == len(enemies):
                a.append([enemy_name, x, new_y])
            enemies = a.copy()
        if event.type == pygame.MOUSEBUTTONUP:
            clicked = False
        #up and down key presses to change level number
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and level <= rows - 1 - screen_rows:
                level += 1
            elif event.key == pygame.K_DOWN and level > 0:
                level -= 1

    pygame.display.update()

pygame.quit()