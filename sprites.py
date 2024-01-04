#Sprites

import pygame
import math
from pygame.sprite import Sprite

class Cursor(Sprite):
    def __init__(self,screen,image,start_pos):
        Sprite.__init__(self)
        self.screen = screen
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect(center = start_pos)

    def update(self):
        ...

#Player class
class Player(Sprite):
    def __init__(self,screen,image,pos,speed,focus_speed,shield):
        self.screen = screen
        self.screen_rect = screen.get_rect()

        #Load player image
        self.player = pygame.image.load(image).convert_alpha()
        self.player = pygame.transform.scale(self.player, (8,8))
        self.rect = self.player.get_rect()

        self.player_image = pygame.image.load(image).convert_alpha()
        self.player_image = pygame.transform.scale(self.player_image, (20,20))


        #Stores center as float vector !important
        self.center = pygame.math.Vector2(pos)
        self.rect.center = self.center #start position

        self.speed = speed
        self.focus = focus_speed
        self.move_left, self.move_right, self.move_up, self.move_down = (False,)*4

        self.shield = shield
        self.invincible = False

    def rotate_player(self):
        d_x, d_y = self.m_x - self.rect.centerx, self.m_y - self.rect.centery
        self.dir = (d_x, #please imagine this as a vector thank you
                    d_y)

        self.angle = math.degrees(math.atan2(-d_y,d_x)) - 90 #Correction
        self.player_rot = pygame.transform.rotozoom(self.player_image, self.angle, 1) 
        self.rect_rot = self.player_rot.get_rect(center = self.center)

    def update(self):
        #get mouse pos
        self.m_x, self.m_y = pygame.mouse.get_pos()
        self.rotate_player()

        #Updates movement
        key = pygame.key.get_pressed()
        right = key[pygame.K_d] #value is 1 if pressed, else is 0
        left = key[pygame.K_a]
        up = key[pygame.K_w]
        down = key[pygame.K_s]

        dirvect = pygame.math.Vector2(right - left, 
                                      down - up)
        if dirvect.length_squared():
            dirvect.scale_to_length(self.speed) # using vectors for accurate diagonal movement
            self.center += dirvect
            self.rect.center = (round(self.center.x),round(self.center.y))

    def draw(self):
        self.screen.blit(self.player_rot,self.rect_rot.topleft)
        pygame.draw.rect(self.screen,"Red",self.rect) #test hitbox (rect) size


# Enemies
class Bots(Sprite):
    def __init__(self,screen,bot_speed,spawn_pos):
        Sprite.__init__(self)
        self.screen = screen

        self.bot = pygame.Surface((30,30))
        self.rect = self.bot.get_rect(center = spawn_pos)
        self.pos = pygame.math.Vector2(self.rect.topleft) # stores vector as float (IMPORTANT TO PREVENT WEIRD JAGGED MOVEMENT)

        self.speed = bot_speed

    def track_player(self,target_pos): # Player tracking
        self.dirvect = (pygame.math.Vector2(target_pos) - self.pos).normalize()
        self.pos += self.dirvect * self.speed

    def update(self,target_pos):
        self.track_player(target_pos) # Move to player
        self.rect.center = round(self.pos.x),round(self.pos.y)

    def draw(self, screen):
        pygame.draw.circle(screen,"Black",self.rect.center,15,3)