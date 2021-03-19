import pygame

from data.sprites import SpriteTest
from world import World
from data import blocks
import settings

pygame.init()

clock = pygame.time.Clock()

screen = pygame.display.set_mode(
    (settings.screen_width, settings.screen_height))

pygame.display.set_caption('Advancing Hero')

stage1 = World(blocks, settings)

all_enemies = pygame.sprite.Group()
all_healthbars = pygame.sprite.Group()

S1 = SpriteTest(position=(512, 288), healthbars=all_healthbars, max_health=66)
S2 = SpriteTest(position=(256, 288), healthbars=all_healthbars, max_health=33)
S3 = SpriteTest(position=(512 + 256, 288),
                healthbars=all_healthbars,
                max_health=100)
all_enemies.add(S1)
all_enemies.add(S2)
all_enemies.add(S3)

run = True

while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    stage1.draw(screen)

    all_enemies.update()
    all_enemies.draw(screen)

    all_healthbars.update()
    all_healthbars.draw(screen)

    pygame.display.update()

pygame.quit()