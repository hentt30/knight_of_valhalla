import os
from .sprite import Sprite
import math
import pygame


class MonsterAttack(Sprite):
    """
    Represents a monster attack
    """
    def __init__(
        self,
        position,
        direction_angle,
        direction,
        final_position,
        screen,
        max_health: float = 100,
        path: str = 'advancing_hero/images/sprites/monster_attack/',
    ) -> None:
        super().__init__(path=os.path.abspath(path),
                         position=position,
                         max_health=max_health)
        self.direction = direction
        self.angle = direction_angle - math.pi / 2
        self.image = pygame.transform.rotate(self.image,
                                             180 * self.angle / math.pi)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.speed = 5
        self.position = position
        self.rect.x = position[0]
        self.rect.y = position[1]
        self.damage = 10
        self.collide_player = False
        self.explosion_frame = 5
        self.explosion_duration = 10
        self.final_position = final_position
        self.stopped = False
        self.initial_frame = 0
        self.music_path = os.path.abspath('advancing_hero/songs/explosion.wav')
        self.screen = screen
        self.life_time = 0

    def update(self, player, stage):
        super().update()
        if self.rect.colliderect(self.screen.get_rect()) == 0:
            self.kill()
        if math.dist(self.position,
                     self.final_position) > 5 and not self.stopped:
            self.position[0] += self.speed * self.direction.x
            self.position[1] += self.speed * self.direction.y
            self.rect.x = self.position[0]
            self.rect.y = self.position[1]
            self.image = self.image_list[self.initial_frame]
            self.initial_frame += 1
            self.initial_frame = self.initial_frame % 5
        elif not self.collide_player:
            self.image = self.image_list[0]
            self.stopped = True
            self.position[1] += stage.scroll_amount
            self.rect.y = self.position[1]
            self.life_time += 1
            if self.life_time >= 300:
                self.collide_player = True
                self.image = self.image_list[-1]
            self.player_collision(player)

        if self.explosion_frame % self.explosion_duration != 0 and self.collide_player:
            self.image = self.image_list[self.explosion_frame]
            self.explosion_frame += 1
        elif self.collide_player:
            self.play_music()
            self.kill()

    def player_collision(self, player):
        if pygame.sprite.collide_mask(self, player) and not self.collide_player:
            self.collide_player = True
            self.image = self.image_list[-1]
            player.hurt(self.damage)

    def play_music(self):
        sound = pygame.mixer.Sound(self.music_path)
        pygame.mixer.Channel(1).play(sound)