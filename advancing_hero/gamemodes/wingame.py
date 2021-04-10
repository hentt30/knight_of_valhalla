"""
Game mode for win game
"""
from .gamemode import GameMode
import pygame
import os


class WinGame(GameMode):
    """
    Class for win game in pygame
    """
    def __init__(self, screen, settings):
        """
        Init end game class
        """
        super().__init__(screen)
        self.settings = settings
        self.background_image = pygame.transform.scale(
            pygame.image.load(
                os.path.abspath('advancing_hero/images/titlescreen.png')),
            self.settings.SIZE)
        self.congrats_font = pygame.font.Font(self.font_path, 80)
        self.press_key_font = pygame.font.Font(self.font_path, 30)
        self.music_path = os.path.abspath('advancing_hero/musics/level_music.wav')

    def play_music(self):
        pygame.mixer.init()
        pygame.mixer.music.load(self.music_path)
        pygame.music.play(-1)

    def loop(self, events):
        """
        main loop for the win screen
        """
        self.screen.blit(self.background_image, (0, 0))
        congrats_text = self.congrats_font.render('Congratulations', True,
                                               self.settings.BLACK)
        you_won_text = self.congrats_font.render('You Won  !', True,
                                               self.settings.BLACK)
        press_key_text = self.press_key_font.render(
            'Press any key to keep playing', True, self.settings.BLACK)
        congrats_rect = congrats_text.get_rect()
        you_won_rect = you_won_text.get_rect()
        press_rect = press_key_text.get_rect()
        congrats_rect.midtop = (self.settings.screen_width / 2, 80)
        you_won_rect.midtop = (self.settings.screen_width / 2,
                            congrats_rect.height + 80 + 25)
        press_rect.midtop = (self.settings.screen_width / 2,
                             you_won_rect.height + 240)
        self.screen.blit(congrats_text, congrats_rect)
        self.screen.blit(you_won_text, you_won_rect)
        self.screen.blit(press_key_text, press_rect)
        for event in events:
            if event.type == pygame.KEYDOWN:
                pygame.display.update()
                pygame.time.wait(500)
                pygame.event.post(
                    pygame.event.Event(pygame.USEREVENT,
                                       customType='title_screen'))
