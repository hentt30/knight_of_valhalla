from .gamemode import GameMode
from advancing_hero.world import World
from advancing_hero.sprites import SpriteTest, Player, Bat
import pygame
import os


class LevelGameMode(GameMode):
    def __init__(self, screen, level_file, settings):
        super().__init__(screen)
        self.level_file = level_file
        self.music_path = os.path.abspath(
            'advancing_hero/songs/level1_music.wav')
        self.settings = settings
        self.play_music()
        self.stage = World(settings, self.level_file, screen)
        self.player = Player((512, 288), settings, self.stage, self.screen)
        self.helper_font = pygame.freetype.Font(self.font_path, 11)

    def play_music(self):
        pygame.mixer.init()
        pygame.mixer.music.load(self.music_path)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)


    def loop(self, events):
        self.stage.update(self.screen, self.player)
        self.player.update()
        self.player.draw()
        self.helper_font.render_to(
            self.screen, (5, self.settings.screen_height - 20),
            "W: UP   S: DOWN   A: LEFT   D: RIGHT   SPACE: HIT   UP: BOOMERANG    DOWN: ARROW",
            self.settings.BLACK)
