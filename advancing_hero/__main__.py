import pygame
from world import World
from sprites import blocks
import settings

pygame.init()

clock = pygame.time.Clock()

screen = pygame.display.set_mode(
    (settings.screen_width, settings.screen_height))

pygame.display.set_caption('Advancing Hero')

stage1 = World(blocks, settings)

run = True

while run:

    stage1.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()
    clock.tick(settings.FPS)

pygame.quit()