#Sprites

import pygame
import math
from pygame.sprite import Sprite, Group

class CameraGroup(Group):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.display_surface = pygame.display.get_surface()

    # Draws in order of y-axis
    def custom_draw(self, screen):
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):# Sorts self.sprites based on y_axis
            screen.blit(sprite.hit_sprite_rot, sprite.sprite_rect)
            screen.blit(sprite.sprite_rot, sprite.sprite_rect)
        
class Cursor(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.image = pygame.image.load("sprites/crosshair.png").convert_alpha()
        self.image.set_alpha(255)
        self.center = (0,0)
        self.rect = self.image.get_rect(center = self.center)

    def update(self):
        self.rect.bottomright = pygame.mouse.get_pos()

    def draw(self, screen):
        screen.blit(self.image, self.rect.center)

        

class Background(Sprite):
    def __init__(self,Group):
        super.__init__(Group)
        ...

#Player class
class Player(Sprite):
    def __init__(self,screen,pos,speed,focus_speed,lives,shield,SCREENSIZE):
        Sprite.__init__(self)
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.screen_width = SCREENSIZE[0]
        self.screen_height = SCREENSIZE[1]

        self.hitbox = pygame.Surface((8,8))
        self.rect = self.hitbox.get_rect(center = pos)

        # Load player image
        self.sprites = []
        self.frame = 1
        for i in range(1,9):
            sprite_frame = pygame.image.load(f"animated/player_sprite-{i}.png").convert_alpha()
            sprite_frame = pygame.transform.rotozoom(sprite_frame, 0, 0.5)
            self.sprites.append(sprite_frame)

        self.image = self.sprites[self.frame - 1]
        self.sprite_rect = self.image.get_rect(center = pos)

        # Stores center as float vector
        self.center = pygame.math.Vector2(pos)
        self.rect.center = self.center #start position

        # Variables
        self.angle = 0
        self.vel = speed
        self.focus = focus_speed
        self.is_focused = False
        self.res_vel = self.vel

        self.lives = lives
        self.shield = shield
        self.invincible_time = 1000
        self.invincible = False
        self.is_hit = False
        self.hit_time = 0

        self.hit_sfx = pygame.mixer.Sound("sfx/player_hit.wav")
        self.hit_sfx.set_volume(1.2)

    def animate_sprite(self):
        angle = -self.angle - 90
        if -22.5 <= angle < 22.5:
            self.image = self.sprites[0]
        elif 22.5 <= angle < 67.5:
            self.image = self.sprites[1]
        elif 67.5 <= angle < 112.5:
            self.image = self.sprites[2]
        elif 112.5 <= angle < 157.5:
            self.image = self.sprites[3]
        elif 157.5 <= angle <= 180 or -180 <= angle -157.5:
            self.image = self.sprites[4]
        elif -157.5 <= angle < -112.5:
            self.image = self.sprites[5]
        elif -112.5 <= angle < -67.5:
            self.image = self.sprites[6]
        elif -67.5 <= angle < -22.5:
            self.image = self.sprites[7]

    # Player is invincible after getting hit
    def update_invincibilty(self):
        if self.is_hit:
            print("hit")
            self.invincible = True
            self.hit_time = pygame.time.get_ticks()
            self.is_hit = False
        elif self.invincible:
            if pygame.time.get_ticks() - self.hit_time > self.invincible_time:
                self.invincible = False
                
    def hit(self):
        if self.lives:
            self.lives -= 1
            self.is_hit = True
            self.hit_sfx.play()

    # Checks for RMB click - activates focus mode
    def set_focused(self):
        if pygame.mouse.get_pressed()[2]:
            return True
        else:
            return False
        
    # handles player rotation towards mouse position
    def rotate_player(self):
        d_x, d_y = self.m_x - self.rect.centerx, self.m_y - self.rect.centery
        self.dir = (d_x, 
                    d_y)

        self.angle = math.degrees(math.atan2(-d_y,d_x)) - 90 #Correction
        self.pointer_rot = pygame.transform.rotozoom(self.image, self.angle, 0.5) 
        self.rect_rot = self.pointer_rot.get_rect(center = self.center)

    # Handles player movement
    def move_player(self):
        key = pygame.key.get_pressed()
        right = key[pygame.K_d] # value returns 1 if pressed, else returns 0
        left = key[pygame.K_a]
        up = key[pygame.K_w]
        down = key[pygame.K_s]

        dirvect = pygame.math.Vector2(right - left, 
                                      down - up)
        if dirvect.length_squared():
            dirvect.scale_to_length(self.res_vel) # divides diagonal velocity by sqrt(2)
            self.center += dirvect
            self.rect.center = (round(self.center.x),round(self.center.y))
            self.sprite_rect = self.image.get_rect(center = self.center)

    def update(self, *Args):
        self.animate_sprite()
        #get mouse pos
        self.m_x, self.m_y = pygame.mouse.get_pos()
        self.rotate_player()
        self.move_player()
        self.update_invincibilty()
        self.clamp()

    def clamp(self):
        self.center = (max(min(self.screen_width, self.center[0]), 0),
                       max(min(self.screen_height, self.center[1]), 0))

    def draw(self, screen):
        screen.blit(self.image,self.sprite_rect) # Main sprite
        # Pointer sprite
        '''pygame.draw.rect(screen,"Red",self.rect) '''#test hitbox (rect) size
