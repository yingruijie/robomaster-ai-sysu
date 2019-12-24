# init game.py
import pygame
from elements.robot import robot
from elements.ground import ground
from elements.define import *
vec = pygame.math.Vector2
class game():
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("robomaster-ai")
        self.screen = pygame.display.set_mode((830, 530))
        self.clock = pygame.time.Clock()
        self.running = True
        self.done = False
        self.ground = ground('elements/resource/ground.png')
        self.robot1 = robot('elements/resource/robot1.png', 'elements/resource/red_bullet.png', 'robot1', 200, 200, 0)
        self.robot2 = robot('elements/resource/robot2.png', 'elements/resource/blue_bullet.png', 'robot2', 500, 300, 0)

        self.ground_group = pygame.sprite.Group()
        self.robot1_group = pygame.sprite.Group()
        self.robot2_group = pygame.sprite.Group()
        self.ground_group.add(self.ground)
        self.robot1_group.add(self.robot1)
        self.robot2_group.add(self.robot2)


    def run(self):
        while self.running:
            self.clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONUP:
                    print(pygame.mouse.get_pos()) 

            key = pygame.key.get_pressed()
            action1 = [0, 0, 0, 0]
            if key[pygame.K_a]: # move left
                action1[0] = -2 
            if key[pygame.K_d]: # move right
                action1[0] = 2
            if key[pygame.K_w]: # move up
                action1[1] = -2
            if key[pygame.K_s]: # move down
                action1[1] = 2
            if key[pygame.K_t]: # rotate counter clockwise
                action1[2] = 3
            if key[pygame.K_y]: # rotate clockwise
                action1[2] = -3
            if key[pygame.K_r]: # shoot
                action1[3] = 1


            action2 = [0, 0, 0, 0]
            if key[pygame.K_LEFT]:  # move left
                action2[0] = -2 
            if key[pygame.K_RIGHT]: # move right
                action2[0] = 2
            if key[pygame.K_UP]:    # move up
                action2[1] = -2
            if key[pygame.K_DOWN]:  # move down
                action2[1] = 2
            if key[pygame.K_j]:     # rotate counter clockwise
                action2[2] = 3
            if key[pygame.K_k]:     # rotate clockwise
                action2[2] = -3
            if key[pygame.K_l]:     # shoot
                action2[3] = 1

            # print(action1, action2)
            self.step(action1, action2)

            self.ground_group.draw(self.screen)
            self.ground.block_group.draw(self.screen)
            self.robot1_group.draw(self.screen)
            self.robot2_group.draw(self.screen)
            self.robot1.bullet_group.draw(self.screen)
            self.robot2.bullet_group.draw(self.screen)
            pygame.display.update()

    def state(self):

        return

    def step(self, action1, action2):
        self.robot1.step(action1, self.robot2_group, self.ground.block_group, bullet_color=red)
        self.robot2.step(action2, self.robot1_group, self.ground.block_group, bullet_color=blue)
        print(self.robot2.state)
        return
    
    def done(self):
        if self.robot1.hp <= 0 and self.robot2.hp > 0:
            self.robot1.loss()
            self.robot2.win()
            return True
        elif self.robot1.hp > 0 and self.robot2.hp <= 0:
            self.robot1.win()
            self.robot2.loss()
            return True
        elif self.robot1.hp <= 0 and self.robot2.hp <= 0:
            return True
        else:
            if self.robot1.bullet_num <= 0 and self.bullet_num <= 0:
                return True
        return False

    def reset(self):
        return

if __name__ == '__main__':
    rm_ai = game()
    rm_ai.run()

    
