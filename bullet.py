#Bullet Classes
import pygame
import math
from pygame.sprite import Sprite


# Bullet 
class Bullet(Sprite):
    def __init__(self,screen,player_pos,dirvect,bullet_speed):
        Sprite.__init__(self)
        self.screen = screen
        self.player_pos = player_pos
        self.x = self.player_pos[0]
        self.y = self.player_pos[1]
        self.dirvect = dirvect

        self.bullet = pygame.Surface((6,6))
        self.rect = self.bullet.get_rect(center = self.player_pos)
        self.speed = bullet_speed

    def update(self):
        self.x += self.dirvect[0] * self.speed
        self.y += self.dirvect[1] * self.speed
        self.player_pos = (self.x,
                           self.y)
        
        self.rect = self.bullet.get_rect(center = self.player_pos)
        
    def draw(self, screen):
        pygame.draw.circle(screen,"Black",self.rect.center,6,3) 


#Cannon - Bullet Handler   
class Cannon():
    def __init__(self, screen, Bullet, bullet_group, max_bullet_count):
        self.screen = screen
        self.Bullet = Bullet
        self.bg = bullet_group
        self.max = max_bullet_count

        self.type = 1
        self.level = 1
        ...

    #Cannon updates
    def get_dirvect(self, target):
        self.target = target
        self.dist = math.hypot(*self.target)
        print(self.dist)
        if not self.dist:
            self.dirvect = (0,1)
        else:
            self.dirvect = (self.target[0]/self.dist, self.target[1]/self.dist) #unit vector

        

    #Cannon types
    def default(self,player_pos): #single shot - upgrades into multi shot
        angles = (10,-10,20,-20) 

        #10deg angle spread
        sin_1 = math.asin(math.radians(10))
        opp_1 = sin_1 * self.dist
        cos_1 = math.acos(math.radians(10))
        adj_1 = cos_1 * self.dist

        sin_2 = math.asin(math.radians(-10))
        opp_2 = sin_2 * self.dist
        cos_2 = math.acos(math.radians(-10))
        adj_2 = cos_2 * self.dist
        print(self.target[0], adj_2)

        dv_1_1 = (adj_1/self.dist, opp_1/self.dist) #WiwiwiwWAWAW
        dv_1_2 = (adj_2/self.dist, opp_2/self.dist)
  
        self.bg.add(self.Bullet(self.screen, player_pos, self.dirvect,5 ))
        self.bg.add(self.Bullet(self.screen, player_pos, dv_1_2, 5))
        
    def rapid(self): #rapid & innacurate machine gun - upgrades for more bullets
        ...

    def spread(self):  #multishot & innacurate - upgrades for more bullets - limited range
        ...

    #Fire
    def fire_cannon(self,player_pos): 
        if len(self.bg) < self.max:    
            if self.type == 1:
                self.default(player_pos)
            elif self.type == 2:
                self.rapid()
            elif self.type == 3:
                self.spread()
            else:
                return False


        


