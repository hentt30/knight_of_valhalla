import pygame 

from classes.World import World
from settings import *
from pygame.locals import *

pygame.init()

clock = pygame.time.Clock()

screen =  pygame.display.set_mode( (screen_width, screen_height))
pygame.display.set_caption('Advancing Hero')


stage1_data = [
    [4, 1, 1, 1, 1, 1, 1, 1, 1, 5, 5, 1, 1, 1, 1, 1], 
    [4, 2, 2, 1, 1, 1, 1, 1, 1, 5, 5, 1, 1, 1, 1, 1], 
    [4, 2, 2, 1, 1, 1, 1, 1, 1, 5, 5, 1, 1, 1, 1, 1], 
    [4, 1, 1, 2, 1, 1, 1, 1, 1, 5, 5, 1, 1, 3, 1, 1], 
    [4, 1, 1, 2, 1, 1, 1, 1, 1, 5, 5, 1, 1, 3, 1, 1], 
    [4, 1, 1, 1, 1, 1, 1, 1, 1, 5, 5, 1, 1, 3, 1, 1], 
    [4, 1, 1, 1, 1, 1, 1, 1, 1, 5, 5, 1, 1, 1, 3, 1], 
    [4, 1, 1, 1, 1, 1, 1, 1, 1, 5, 5, 1, 1, 1, 3, 1], 
    [4, 1, 1, 1, 1, 1, 1, 1, 1, 5, 5, 1, 1, 1, 1, 3], 
    
]

stage1 = World(stage1_data)

run = True

while run:

    stage1.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()