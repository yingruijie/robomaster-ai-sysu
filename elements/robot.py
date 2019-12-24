# class robot
import pygame
import numpy as np
from elements.bullet import bullet
from elements.define import *

vec = pygame.math.Vector2
class robot(pygame.sprite.Sprite):
    def __init__(self, image_path, bullet_path, player, x, y, yaw, bullet_num=100, hp=100):
        pygame.sprite.Sprite.__init__(self)
        self.bullet_group = pygame.sprite.Group()
        self.player = player
        self.yaw = yaw
        self.image_path = image_path
        self.origin = pygame.image.load(self.image_path).convert()
        rect_origin = self.origin.get_rect()
        self.w = rect_origin.w
        self.h = rect_origin.h
        self.image = pygame.transform.rotate(self.origin, yaw)
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        self.pos = vec(x, y)
        self.rect.center = self.pos
        self.bullet_path = bullet_path
        self.bullet_num = bullet_num
        self.hp = hp
        self.shoot_time = 30
        self.reward = 0
        self.state = [0, 0, 0, 0, 0, 0, 0]

    def shoot(self, if_shoot, robot_group, block_group, color=red):
        if self.shoot_time > 0:
            self.shoot_time -= 1
        if (self.bullet_num > 0) and (self.shoot_time == 0) and (if_shoot == 1):
            new_bullet_x = self.pos[0] - self.h/2 * np.math.sin(self.yaw * 3.1415926 / 180)
            new_bullet_y = self.pos[1] - self.h/2 * np.math.cos(self.yaw * 3.1415926 / 180)
            self.bullet_group.add(bullet(self.bullet_path, self.player, new_bullet_x, new_bullet_y, self.yaw,v=10))
            self.bullet_num -= 1
            self.shoot_time = 30

        for b in self.bullet_group:
            b.move(robot_group, block_group)
        hit = pygame.sprite.groupcollide(self.bullet_group, block_group, True, False)
        # reward 
        self.reward -= 1

        for robot in robot_group:
            hit = pygame.sprite.spritecollide(robot, self.bullet_group, True, False)
            hit_num = len(hit)
            while hit_num > 0:
                # reward
                self.reward += 20
                robot.be_hit()
                hit_num -= 1


    def move(self, vx, vy, rotate, robot_group, block_group):
        new_pos = self.pos + vec(vx, vy)
        new_yaw = float(int(self.yaw + rotate) % 360)
        self.image = pygame.transform.rotate(self.origin, new_yaw)
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        self.rect.center = new_pos
        if pygame.sprite.spritecollide(self, block_group, False, False) or \
           pygame.sprite.spritecollide(self, robot_group, False, False):
            self.rect.center = self.pos
            # reward
            self.reward -= 0.1
            return False
        else:
            self.pos = new_pos
            self.yaw = new_yaw
            # reward
            return True

    def get_state(self, robot_group):
        # x, y, yaw, hp, bullet_num, x_e, y_e,
        x_e, y_e = 0, 0
        for em in robot_group:
            x_e, y_e = em.pos[0], em.pos[1]
        self.state = [0, 0, 0, 0, 0, 0, 0]
        self.state[0] = self.pos[0]
        self.state[1] = self.pos[1]
        self.state[2] = self.yaw
        self.state[3] = self.hp
        self.state[4] = self.bullet_num
        self.state[5] = x_e
        self.state[6] = y_e
        return True

    def step(self, action, robot_group, block_group, bullet_color=red):
        self.reward = 0
        self.move(action[0], action[1], action[2], robot_group, block_group)
        self.shoot(action[3], robot_group, block_group, color=bullet_color)
        self.get_state(robot_group)
        return True

    def be_hit(self):
        self.hp -= 10
        self.reward -= 10
        # print(self.player + ' be hit ' + 'hp = ' + str(self.hp))
        # reward
        return True
    
    def win(self):
        # reward
        self.reward += 100
        return True
    
    def loss(self):
        # reward
        self.reward -= 100
        return True

    def reset(self, x, y):
        self.pos = vec(x, y)
        self.rect.center = self.pos
        self.hp = 100
        self.bullet_num = 100
        self.bullet_group.empty()
        return True
        