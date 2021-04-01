import pygame

import settings
import gamemodes

pygame.init()

clock = pygame.time.Clock()
global current_gamemode
global game_admin

screen = pygame.display.set_mode(
    (settings.screen_width, settings.screen_height))

pygame.display.set_caption(settings.TITLE)

pygame.event.post(pygame.event.Event(pygame.USEREVENT, customType='title_screen'))

run = True

while run:
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.USEREVENT:
            if event.customType == 'init_level':
                current_gamemode = gamemodes.modes['level_main']
                game_admin = current_gamemode(screen, event.level, settings)
                print('level_init')
            if event.customType == 'title_screen':
                current_gamemode = gamemodes.modes['title_screen']
                game_admin = current_gamemode(screen, settings)

    game_admin.loop(events)

    pygame.display.update()

    clock.tick(settings.FPS)


pygame.quit()
