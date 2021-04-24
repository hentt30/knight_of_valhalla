import os
from .sprite import Sprite
import pygame
import math


class ShipAttack(Sprite):
    """
    Represents a ship attack
    """
    def __init__(
        self,
        position,
        direction_angle,
        direction,
        screen,
        max_health: float = 100,
        path: str = 'advancing_hero/images/sprites/ship_attack/',
    ) -> None:
        super().__init__(path=os.path.abspath(path),
                         position=position,
                         max_health=max_health)
        self.direction = direction
        self.angle = direction_angle - math.pi / 2
        self.image = pygame.transform.rotate(self.image,
                                             180 * self.angle / math.pi)
        self.image = pygame.transform.scale2x(self.image)
        self.rect = self.image.get_rect()
        self.speed = 3
        self.position = position
        self.rect.x = position[0]
        self.rect.y = position[1]
        self.damage = 8
        self.collide_player = False
        self.explosion_frame = 2
        self.explosion_duration = 6
        self.music_path = os.path.abspath('advancing_hero/songs/explosion.wav')
        self.screen = screen

    def update(self, player, stage):
        super().update()
        self.position[0] += self.speed * self.direction.x
        self.position[1] += self.speed * self.direction.y
        self.rect.x = self.position[0]
        self.rect.y = self.position[1]
        self.player_collision(player)
        if self.explosion_frame % self.explosion_duration != 0 and self.collide_player:
            self.image = self.image_list[self.explosion_frame]
            self.explosion_frame += 1
        elif self.collide_player:
            self.play_music()
            self.kill()
        if self.rect.colliderect(self.screen.get_rect()) == 0:
            self.kill()

    def player_collision(self, player):
        if self.rect.colliderect(player.rect):
            self.collide_player = True
            self.image = self.image_list[-1]
            player.hurt(self.damage)

    def play_music(self):
        sound = pygame.mixer.Sound(self.music_path)
        sound.set_volume(0.05)
        pygame.mixer.Channel(2).play(sound)
