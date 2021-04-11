import os
from .sprite import Sprite
import math
import pygame


class PotionHeal(Sprite):
    """
    Represents a potion to heal the hero
    """
    def __init__(
        self,
        position,
        screen,
        path: str = 'advancing_hero/images/sprites/potion_heal/',
    ) -> None:
        super().__init__(path=os.path.abspath(path), position=position)

        self.rect = self.image.get_rect()
        self.speed = 5
        self.position = position
        self.rect.x = position[0]
        self.rect.y = position[1]
        self.heal = 35
        self.music_path = os.path.abspath('advancing_hero/songs/item.wav')

    def update(self, player, stage):
        super().update()
        self.rect.y += stage.scroll_amount
        self.player_collision(player)
        for tile in stage.tile_list:
            if tile[1].bottom > 0 and tile[
                    1].top < stage.settings.screen_height and tile[2].is_solid:
                if tile[1].colliderect(self.rect):
                    self.kill()

    def player_collision(self, player):
        if self.rect.colliderect(player.rect):
            player.heal(self.heal)
            self.play_music()
            self.kill()

    def play_music(self):
        sound = pygame.mixer.Sound(self.music_path)
        pygame.mixer.Channel(4).play(sound)
