import os
from .sprite import Sprite
from .healthbar import HealthBar
from .boss_spear import BossSpear
from .boss_fire import BossFire
import pygame
import math
import random


class Boss(Sprite):
    """
    Represents the boss
    """
    def __init__(
        self,
        position,
        screen,
        max_health: float = 1000,
        path: str = 'advancing_hero/images/sprites/boss/',
    ) -> None:
        super().__init__(path=os.path.abspath(path),
                         position=position,
                         max_health=max_health)
        self.screen = screen
        self.mask_list = []
        self.damage = 20

        for i in range(len(self.image_list)):
            self.image_list[i] = \
                pygame.transform.scale(self.image_list[i],
                                       (self.image.get_rect().width * 3,
                                        self.image.get_rect().height * 3))
            self.mask_list.append(pygame.mask.from_surface(self.image_list[i]))
        self.image = self.image_list[0]
        self.aux_image = self.image.copy()
        self.mask = self.mask_list[0]
        self.rect = self.image.get_rect()
        self.rect.centerx = position[0]
        self.rect.centery = position[1]-64

        self.health_bar = HealthBar(screen=screen,
                                    parent_sprite=self,
                                    offset=(0, -60))

        self.true_position = pygame.Vector2((self.rect.centerx, self.rect.centery))
        self.speed = 12
        self.moving = False
        self.moving_position = pygame.Vector2()

        self.spear = BossSpear(position, self.screen)

        self.animation_framerate = 8

        self.state = 0
        self.substate = 0

        self.timer1 = 0
        self.counter1 = 0
        self.flag1 = False
        self.flag2 = False

    def update(self, player, stage):
        super().update()
        if self.current_health <= 0 and self.state != 100:
            self.state = 100
            self.spear.kill()
            self.update_image(18)
            self.timer1 = 60
            self.counter1 = 255

        if self.state == 0:
            self.state0_code(player, stage)
        elif self.state == 1:
            self.state1_code(player, stage)
        elif self.state == 2:
            self.state2_code(player, stage)
        elif self.state == 3:
            self.state3_code(player, stage)
        elif self.state == 100:
            self.death_code(player, stage)

    # Waiting for whole screen to stop moving (reach end of the level)
    def state0_code(self, player, stage):
        self.player_collision(player)
        if self.timer1 <= 50:
            if stage.scroll_amount > 0:
                self.true_position.y += stage.scroll_amount
                self.rect.centery = int(self.true_position.y)
                self.timer1 = 0
            else:
                self.timer1 += 1
        else:
            self.state = 1
            self.substate = 0
            self.spear.set_position(self.rect.centerx + 60, self.rect.centery - 45)
            self.update_image(3 + self.get_looking_direction(
                              pygame.Vector2((player.rect.centerx, player.rect.centery)), 1))
            self.groups()[0].add(self.spear)
            self.timer1 = 180
            self.counter1 = random.randint(1, 4)
            self.flag1 = False
            self.flag2 = False

    # Spin the spear, throw it and catch it back
    def state1_code(self, player, stage):
        self.health_bar.update()
        self.player_collision(player)
        if self.substate == 0:
            if not self.flag1:
                self.update_image(3+self.get_looking_direction(
                                  pygame.Vector2((player.rect.centerx, player.rect.centery)), 0)+9*self.flag2)
            else:
                self.update_image(6+self.get_looking_direction(
                                  pygame.Vector2((player.rect.centerx, player.rect.centery)), 0)+9*self.flag2)
        if self.substate != 2:
            if self.timer1 > 0:
                self.timer1 -= 1
            else:
                if self.counter1 > 0:
                    self.spear.move_lance(pygame.Vector2((player.rect.centerx, player.rect.centery)))
                    self.timer1 = 80
                    self.counter1 -= 1
                    self.flag1 = True
                else:
                    if not self.moving:
                        self.spear.move_lance(pygame.Vector2((player.rect.centerx, player.rect.centery)))
                        if player.rect.centery < self.true_position.y:
                            self.move_self(pygame.Vector2((player.rect.centerx + 60, player.rect.centery + 45)))
                        else:
                            self.move_self(pygame.Vector2((player.rect.centerx-60, player.rect.centery+45)))
                        self.update_image(3 + self.get_looking_direction(
                            pygame.Vector2((player.rect.centerx, player.rect.centery)), 1))
                        self.substate = 1
                    self.move()
                    if not self.moving:
                        self.substate = 2
                        self.timer1 = 60
        if self.substate == 2:
            if self.timer1 > 0:
                self.timer1 -= 1
            else:
                choose_attack = random.randint(0, 1)
                if choose_attack == 0:
                    self.call_state2()
                elif choose_attack == 1:
                    self.call_state3()

    # Dash at player's position and summon rotating fire
    def state2_code(self, player, stage):
        self.health_bar.update()
        self.player_collision(player)
        if self.substate == 0:
            if self.timer1 > 0:
                self.timer1 -= 1
            else:
                if not self.flag1:
                    print('dash')
                    self.move_self(pygame.Vector2((player.rect.centerx, player.rect.centery)))
                    self.flag1 = True
                self.move()
                if not self.moving:
                    self.substate = 1
                    self.timer1 = 30
                    self.update_image(0 + self.get_looking_direction(
                        pygame.Vector2((self.screen.get_width()/2, self.screen.get_height()/2)), 1))
        elif self.substate == 1:
            if self.timer1 > 0:
                self.timer1 -= 1
            else:
                self.update_image(3 + self.get_looking_direction(
                    pygame.Vector2((player.rect.centerx, player.rect.centery)), 1))
                if player.rect.centery < self.true_position.y:
                    self.spear.set_position(self.rect.centerx - 60, self.rect.centery - 45)
                else:
                    self.spear.set_position(self.rect.centerx + 60, self.rect.centery - 45)
                self.groups()[0].add(self.spear)
                self.substate = 2
        elif self.substate == 2:
            for i in range(8):
                fire = BossFire((self.rect.centerx, self.rect.centery), self.screen, i*45, 0)
                self.groups()[0].add(fire)
            self.substate = 3
            self.timer1 = 240
        elif self.substate == 3:
            if self.timer1 > 0:
                self.timer1 -= 1
            else:
                choose_attack = random.randint(0, 1)
                if choose_attack == 0:
                    self.call_state1(player)
                elif choose_attack == 1:
                    self.call_state3()

    # Turn invisible and summon fire bats
    def state3_code(self, player, stage):
        if self.substate == 0:
            if self.timer1 > 0:
                self.image.set_alpha(int(self.counter1))
                self.counter1 = max(0.0, self.counter1 - 255/30)
                self.timer1 -= 1
            else:
                self.image.set_alpha(0)
                self.substate = 1
                self.timer1 = 30
                self.counter1 = random.randint(8, 12)
        elif self.substate == 1:
            if self.counter1 > 0:
                if self.timer1 > 0:
                    self.timer1 -= 1
                else:
                    random_x = random.randrange(20, self.screen.get_width()-20)
                    random_y = random.randrange(20, self.screen.get_height()-20)
                    random_pos = (random_x, random_y)
                    firebat = BossFire(random_pos, self.screen, 0, 1)
                    self.groups()[0].add(firebat)
                    self.timer1 = 30
                    self.counter1 -= 1
            else:
                if len(self.groups()[0].sprites()) <= 2:
                    self.true_position.x = random.randrange(200, self.screen.get_width()-200)
                    self.true_position.y = random.randrange(100, self.screen.get_height()-100)
                    self.rect.centerx = int(self.true_position.x)
                    self.rect.centery = int(self.true_position.y)
                    self.substate = 2
                    self.timer1 = 60
                    self.counter1 = 0
        elif self.substate == 2:
            if self.timer1 > 0:
                self.image.set_alpha(int(self.counter1))
                self.counter1 = min(255.0, self.counter1 + 255/60)
                self.timer1 -= 1
            else:
                self.timer1 = 30
                self.substate = 3
        elif self.substate == 3:
            if self.timer1 > 0:
                self.timer1 -= 1
            else:
                choose_attack = random.randint(0, 1)
                if choose_attack == 0:
                    self.call_state1(player)
                elif choose_attack == 1:
                    self.call_state2()

    def death_code(self, player, stage):
        self.shake_stage(stage)
        if self.timer1 > 0:
            self.timer1 -= 1
        else:
            if self.counter1 > 0:
                self.image.set_alpha(int(self.counter1))
                self.counter1 = max(0.0, self.counter1 - 255/180)
                self.timer1 -= 1
            else:
                for tile in stage.tile_list:
                    tile[1].x = round(tile[1].x / 64) * 64
                self.kill()
                pygame.event.post(pygame.event.Event(pygame.USEREVENT, customType='win_game'))

    def shake_stage(self, stage):
        if self.frame_counter % 6 == 0:
            for tile in stage.tile_list:
                tile[1].x = round(tile[1].x/64)*64 - 3
        elif self.frame_counter % 3 == 0:
            for tile in stage.tile_list:
                tile[1].x = round(tile[1].x/64)*64 + 3

    def call_state1(self, player):
        self.update_image(3 + self.get_looking_direction(
            pygame.Vector2((player.rect.centerx, player.rect.centery)), 1))
        if player.rect.centery < self.true_position.y:
            self.spear.set_position(self.rect.centerx - 60, self.rect.centery - 45)
        else:
            self.spear.set_position(self.rect.centerx + 60, self.rect.centery - 45)
        self.flag2 = (player.rect.centery < self.true_position.y)
        self.substate = 0
        self.groups()[0].add(self.spear)
        self.timer1 = 180
        self.counter1 = random.randint(1, 4)
        self.flag1 = False
        self.state = 1

    def call_state2(self):
        self.update_image(0 + self.get_looking_direction(
            pygame.Vector2((self.screen.get_width() / 2, self.screen.get_height() / 2)), 1))
        self.spear.kill()
        self.timer1 = 30
        self.state = 2
        self.flag1 = False
        self.counter1 = 0
        self.substate = 0

    def call_state3(self):
        self.timer1 = 30
        self.state = 3
        self.flag1 = False
        self.counter1 = 255
        self.substate = 0
        self.spear.kill()
        self.update_image(0)

    def player_collision(self, player):
        if pygame.sprite.collide_mask(self, player):
            player.hurt(self.damage)

    def hurt(self, damage):
        if self.state != 3 and self.state != 0 and self.state != 100:
            self.current_health = max(self.current_health - damage, 0)
            return True
        else:
            return False

    def update_image(self, index):
        temp_rect = self.rect
        self.image = self.image_list[index]
        self.mask = self.mask_list[index]
        self.rect = self.image.get_rect()
        self.rect.centerx = temp_rect.centerx
        self.rect.centery = temp_rect.centery

    def get_looking_direction(self, point, vertical_flag) -> int:
        delta_x = point.x - self.rect.centerx
        delta_y = point.y - self.rect.centery
        direction_angle = -math.atan2(delta_y, delta_x)
        if math.pi/3 >= direction_angle >= 0:
            saida = 2+9*vertical_flag
        elif 0 <= direction_angle <= 2*math.pi/3:
            saida = 0+9*vertical_flag
        elif 0 <= direction_angle <= math.pi:
            saida = 1+9*vertical_flag
        elif 0 >= direction_angle >= -math.pi/3:
            saida = 2
        elif 0 >= direction_angle >= -2*math.pi/3:
            saida = 0
        else:
            saida = 1
        return saida

    def move_self(self, position):
        self.moving = True
        self.moving_position = position

    def move(self):
        if self.moving:
            distance = pygame.math.Vector2.magnitude(self.moving_position-self.true_position)
            if distance >= self.speed:
                moving_dir = pygame.math.Vector2.normalize(self.moving_position-self.true_position)
                self.true_position += self.speed * moving_dir
            else:
                self.true_position += self.moving_position-self.true_position
                self.moving = False
        self.rect.centerx = int(self.true_position.x)
        self.rect.centery = int(self.true_position.y)
