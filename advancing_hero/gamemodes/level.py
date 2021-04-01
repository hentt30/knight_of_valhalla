from .gamemode import GameMode
from advancing_hero.world import World
from advancing_hero.sprites import SpriteTest, Player
import pygame


class LevelGameMode(GameMode):

    def __init__(self, screen, level_file, settings):
        super().__init__(screen)
        self.level_file = level_file
        self.stage = World(settings, self.level_file)
        self.all_enemies = pygame.sprite.Group()
        self.all_healthbars = pygame.sprite.Group()
        S1 = SpriteTest(position=(512, 288), healthbars=self.all_healthbars, max_health=66)
        S2 = SpriteTest(position=(256, 288), healthbars=self.all_healthbars, max_health=33)
        S3 = SpriteTest(position=(512 + 256, 288), healthbars=self.all_healthbars, max_health=100)
        self.player = Player((512, 288), settings, self.stage)
        self.all_enemies.add(S1)
        self.all_enemies.add(S2)
        self.all_enemies.add(S3)

    def loop(self, events):
        self.stage.draw(self.screen)

        self.all_enemies.update()
        self.all_enemies.draw(self.screen)

        self.all_healthbars.update()
        self.all_healthbars.draw(self.screen)

        self.player.update()
        self.player.draw(self.screen)
