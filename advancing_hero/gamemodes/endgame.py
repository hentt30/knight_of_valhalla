"""
Game mode for end game
"""
from .gamemode import GameMode
import pygame
import os


class EndGame(GameMode):
    """
    Class for end game in pygame
    """
    def __init__(self, screen, settings):
        """
        Init end game class
        """
        super().__init__(screen)
        self.settings = settings
        self.background_image = pygame.transform.scale(
            pygame.image.load(
                os.path.abspath('advancing_hero/images/endscreen.png')),
            self.settings.SIZE)
        self.game_over_font = pygame.font.Font(self.font_path, 100)
        self.press_key_font = pygame.font.Font(self.font_path, 30)

    def loop(self, events):
        """
        main loop for the end screen
        """
        self.screen.blit(self.background_image, (0, 0))
        game_text = self.game_over_font.render('Game', True,
                                               self.settings.WHITE)
        over_text = self.game_over_font.render('Over', True,
                                               self.settings.WHITE)
        press_key_text = self.press_key_font.render(
            'Press any key to continue', True, self.settings.WHITE)
        game_rect = game_text.get_rect()
        over_rect = over_text.get_rect()
        press_rect = press_key_text.get_rect()
        game_rect.midtop = (self.settings.screen_width / 2, 80)
        over_rect.midtop = (self.settings.screen_width / 2,
                            game_rect.height + 80 + 25)
        press_rect.midtop = (self.settings.screen_width / 2,
                             over_rect.height + 240)
        self.screen.blit(game_text, game_rect)
        self.screen.blit(over_text, over_rect)
        self.screen.blit(press_key_text, press_rect)
        for event in events:
            if event.type == pygame.KEYDOWN:
                pygame.display.update()
                pygame.time.wait(500)
                pygame.event.post(
                    pygame.event.Event(pygame.USEREVENT,
                                       customType='title_screen'))
