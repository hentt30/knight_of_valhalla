import pygame

from advancing_hero.sprites.sprites.sprite_test import SpriteTest
from world import World
from sprites import blocks
import settings

pygame.init()

clock = pygame.time.Clock()

screen = pygame.display.set_mode(
    (settings.screen_width, settings.screen_height))

pygame.display.set_caption('Advancing Hero')

stage1 = World(blocks, settings)

all_enemies = pygame.sprite.Group()
S1 = SpriteTest((512, 288))
all_enemies.add(S1)

run = True

while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    stage1.draw(screen)

    all_enemies.update()
    all_enemies.draw(screen)

    pygame.display.update()



pygame.quit()