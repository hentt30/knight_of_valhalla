from .gamemode import GameMode
from advancing_hero.world import World
from advancing_hero.sprites import SpriteTest, Player, Bat
import pygame


class LevelGameMode(GameMode):
    def __init__(self, screen, level_file, settings):
        super().__init__(screen)
        self.level_file = level_file
        self.settings = settings
        self.stage = World(settings, self.level_file, screen)

        self.player = Player((512, 288), settings, self.stage, self.screen)
        self.helper_font = pygame.freetype.SysFont('Comic Sans MS', 16)

    def loop(self, events):
        self.stage.update(self.screen, self.player)

        self.player.update()
        self.player.draw()

        self.helper_font.render_to(self.screen,
                                   (0, self.settings.screen_height - 20),
                                   "W: UP   S: DOWN   A: LEFT   D: RIGHT",
                                   self.settings.WHITE)
