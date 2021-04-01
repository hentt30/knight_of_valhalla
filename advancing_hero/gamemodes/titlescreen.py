from .gamemode import GameMode
import pygame
import pygame.freetype
import os


class TitleScreen(GameMode):

    def __init__(self, screen, settings):
        super().__init__(screen)
        self.settings = settings
        self.game_title = pygame.freetype.SysFont('Comic Sans MS', 50)
        self.background_image = pygame.transform.scale(
            pygame.image.load(os.path.abspath('advancing_hero/images/titlescreen.png')),
            self.settings.SIZE)
        self.selection_icon = pygame.transform.scale(
            pygame.image.load(os.path.abspath('advancing_hero/images/select_icon.png')),
            (40, 40))
        self.menu_font = pygame.freetype.SysFont('Comic Sans MS', 25)
        self.icon_position = 0

    def loop(self, events):
        self.screen.blit(self.background_image, (0, 0))
        self.game_title.render_to(self.screen,
                                  (self.settings.screen_width / 2 - 192, self.settings.screen_height / 2 - 256),
                                  "Knight of Valhalla",
                                  self.settings.BLACK)
        self.menu_font.render_to(self.screen,
                                 (self.settings.screen_width / 2 - 80, self.settings.screen_height / 2),
                                 "Play Game",
                                 self.settings.BLACK)
        self.menu_font.render_to(self.screen,
                                 (self.settings.screen_width / 2 - 86, self.settings.screen_height / 2 + 50),
                                 "Quit Game",
                                 self.settings.BLACK)
        self.screen.blit(self.selection_icon,
                         (self.settings.screen_width / 2 - 130,
                          self.settings.screen_height / 2 - 10 + self.icon_position * 50))
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.icon_position = (self.icon_position + 1) % 2
                if event.key == pygame.K_s:
                    self.icon_position = (self.icon_position - 1) % 2
                if event.key == pygame.K_SPACE:
                    if self.icon_position == 1:
                        pygame.event.post(pygame.event.Event(pygame.QUIT))
                    else:
                        pygame.event.post(pygame.event.Event(pygame.USEREVENT, customType='init_level',
                                                             level=self.settings.level_1))