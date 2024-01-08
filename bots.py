from typing import Any
import pygame
from pygame.sprite import Sprite
import math

# Enemies

class Bots(Sprite):
    def __init__(self,screen,bot_speed,spawn_pos,hitpoints, score):
        Sprite.__init__(self)
        self.screen = screen

        # Load sprites
        self.sprites = []
        for i in range(1,6):
            sprite_frame = pygame.image.load(f"animated/pyroid-{i}.png")
            sprite_frame = pygame.transform.rotozoom(sprite_frame, 0, 1.5)
            self.sprites.append(sprite_frame)

        self.hit_sprites = []
        for i in range(6,11):
            sprite_frame = pygame.image.load(f"animated/pyroid-{i}.png")
            sprite_frame = pygame.transform.rotozoom(sprite_frame, 0, 1.5)
            self.hit_sprites.append(sprite_frame)

        self.frame = 0
        self.image = self.sprites[self.frame]
        self.hit_sprite = self.sprites[self.frame]
        self.sprite_rect = self.image.get_rect(center = spawn_pos)

        # hitbox
        self.bot = pygame.Surface((30,30))
        self.rect = self.bot.get_rect(center = spawn_pos)
        self.pos = pygame.math.Vector2(self.rect.topleft) # stores vector as float
        self.center = pygame.math.Vector2(spawn_pos)

        # variables
        self.hp = hitpoints
        self.speed = bot_speed
        self.colliding = False
        self.has_collided = False
        self.collidewith = []
        self.index = 0
        self.iframe = 0
 
        self.score = score

    def animate(self, frame_count):
        self.frame += 0.1
        if self.frame > len(self.sprites) - 1:
            self.frame = 0
        
        self.animate_hit(frame_count)
        self.image = self.sprites[int(self.frame)]
        self.hit_sprite = self.hit_sprites[int(self.frame)]

    def animate_hit(self, frame_count):
        if len(self.collidewith) > self.index:
            self.index += 1
            self.iframe = frame_count
            for sprite in self.sprites:
                sprite.set_alpha(0)

        if  frame_count - self.iframe >= 2:
            for sprite in self.sprites:
                sprite.set_alpha(255)

    def check_pos(self, target_pos):
        if self.pos[0] < target_pos[0]:
            self.sprite_rot = pygame.transform.flip(self.image, 1, 0)
            self.hit_sprite_rot = pygame.transform.flip(self.hit_sprite, 1, 0)
        else:
            self.sprite_rot = self.image
            self.hit_sprite_rot = self.hit_sprite
    
    # Follow player method
    def track_player(self,target_pos):
        self.dirvect = (pygame.math.Vector2(target_pos) - self.pos).normalize()
        self.pos += self.dirvect * self.speed
        self.rect.center = round(self.pos.x),round(self.pos.y)
        self.sprite_rect = self.image.get_rect(center = self.pos)

    def update(self,target_pos,frame_count):
        self.track_player(target_pos) # Move to player
        self.animate(frame_count)
        self.check_pos(target_pos)

    def draw(self, screen):
        screen.blit(self.hit_sprite_rot, self.sprite_rect)
        screen.blit(self.sprite_rot, self.sprite_rect)
        '''pygame.draw.circle(screen,"Grey",self.rect.center,10,3)'''

# Ranged bots
class BotsRanged(Sprite):
    def __init__(self,screen,bot_speed,spawn_pos,hitpoints,fire_rate, Bullet_speed, BotBullets, score):
        Sprite.__init__(self)
        self.screen = screen
        self.sprites = []
        #loads main sprite frames
        for i in range(1,6):
            sprite_frame = pygame.image.load(f"animated/Ectoid-{i}.png")
            sprite_frame = pygame.transform.rotozoom(sprite_frame, 0, 1.5)
            self.sprites.append(sprite_frame)

        #loads "hit" sprite frames
        self.hit_sprites = []
        for i in range(6,11):
            sprite_frame = pygame.image.load(f"animated/Ectoid-{i}.png")
            sprite_frame = pygame.transform.rotozoom(sprite_frame, 0, 1.5)
            self.hit_sprites.append(sprite_frame)

        self.frame = 0
        self.image = self.sprites[self.frame]
        self.hit_sprite = self.sprites[self.frame]
        self.sprite_rect = self.image.get_rect(center = spawn_pos)

        # hitbox
        self.bot = pygame.Surface((30,30))
        self.rect = self.bot.get_rect(center = spawn_pos)
        self.pos = pygame.math.Vector2(self.rect.topleft) # stores vector as float
        self.center = pygame.math.Vector2(spawn_pos)
        
        # Variables
        self.hp = hitpoints
        self.bot = pygame.Surface((20,20))
        self.rect = self.bot.get_rect(center = spawn_pos)
        self.pos = pygame.math.Vector2(self.rect.topleft) # stores vector as float (IMPORTANT TO PREVENT WEIRD JAGGED MOVEMENT)

        self.speed = bot_speed
        self.last_fired = 0
        self.fire_rate = fire_rate
        self.bullet_speed = Bullet_speed

        self.has_entered = False
        self.has_collided = False
        self.collidewith = []
        self.index = 0
        self.iframe = 0

        self.BB = BotBullets
        self.score = score
    
    # Loops through frames
    def animate(self, frame_count):
        self.frame += 0.1 # incrementing to slow down animation
        if self.frame > len(self.sprites) - 1:
            self.frame = 0
        
        self.animate_hit(frame_count)
        self.image = self.sprites[int(self.frame)]
        self.hit_sprite = self.hit_sprites[int(self.frame)]

    # Highlight when bot is hit with bullet
    def animate_hit(self, frame_count):
        if len(self.collidewith) > self.index:
            self.index += 1
            self.iframe = frame_count
            for sprite in self.sprites:
                sprite.set_alpha(0)

        if  frame_count - self.iframe >= 2:
            for sprite in self.sprites:
                sprite.set_alpha(255)

    # Check & get current pos
    def check_pos(self, target_pos):
        if self.pos[0] < target_pos[0]:
            self.sprite_rot = pygame.transform.flip(self.image, 1, 0)
            self.hit_sprite_rot = pygame.transform.flip(self.hit_sprite, 1, 0)
        else:
            self.sprite_rot = self.image
            self.hit_sprite_rot = self.hit_sprite

    ## Unique Method ##
    def fire_at_player(self, bot_projectiles):
        if not self.has_entered:
            if self.screen.get_rect().collidepoint(self.rect.center):
                self.has_entered = True
                self.last_fired = pygame.time.get_ticks()

        if pygame.time.get_ticks() - self.last_fired > 1/self.fire_rate *1000:
            bot_projectiles.add(self.BB(self.screen, self.rect.center, self.dirvect, self.bullet_speed, bot_projectiles))
            self.last_fired = pygame.time.get_ticks()

    # Follow player method
    def track_player(self,target_pos):
        self.dirvect = (pygame.math.Vector2(target_pos) - self.pos).normalize()
        self.pos += self.dirvect * self.speed
        self.rect.center = round(self.pos.x),round(self.pos.y)
        self.sprite_rect = self.image.get_rect(center = self.pos)

    def update(self,target_pos,frame_count,bot_projectile):
        self.track_player(target_pos) # Move to player
        self.animate(frame_count)
        self.check_pos(target_pos)
        self.fire_at_player(bot_projectile)

    def draw(self, screen):
        screen.blit(self.hit_sprite_rot, self.sprite_rect)
        screen.blit(self.sprite_rot, self.sprite_rect)
        '''pygame.draw.circle(screen,"Purple",self.rect.center,10,3)'''

############ MiniBoss ##############
class BotsBig(Sprite):
    def __init__(self,screen,bot_speed,spawn_pos,hitpoints,fire_rate, Bullet_speed, BotBullets, score):
        Sprite.__init__(self)
        self.screen = screen
        self.sprites = []
        #loads main sprite frames
        for i in range(6):
            sprite_frame = pygame.image.load(f"animated/ghosboss{i}.png")
            sprite_frame = pygame.transform.rotozoom(sprite_frame, 0, 1.5)
            sprite_frame = pygame.transform.flip(sprite_frame, True, False)
            self.sprites.append(sprite_frame)

        #loads "hit" sprite frames
        self.hit_sprites = []
        for i in range(6,12):
            sprite_frame = pygame.image.load(f"animated/ghosboss{i}.png")
            sprite_frame = pygame.transform.rotozoom(sprite_frame, 0, 1.5)
            sprite_frame = pygame.transform.flip(sprite_frame, True, False)
            self.hit_sprites.append(sprite_frame)

        self.frame = 0
        self.image = self.sprites[self.frame]
        self.hit_sprite = self.sprites[self.frame]
        self.sprite_rect = self.image.get_rect(center = spawn_pos)

        # hitbox
        self.bot = pygame.Surface((30,30))
        self.rect = self.bot.get_rect(center = spawn_pos)
        self.pos = pygame.math.Vector2(self.rect.topleft) # stores vector as float
        self.center = pygame.math.Vector2(spawn_pos)
        
        # Variables
        self.hp = hitpoints
        self.bot = pygame.Surface((20,20))
        self.rect = self.bot.get_rect(center = spawn_pos)
        self.pos = pygame.math.Vector2(self.rect.topleft) # stores vector as float (IMPORTANT TO PREVENT WEIRD JAGGED MOVEMENT)

        self.speed = bot_speed
        self.last_fired = 0
        self.fire_rate = fire_rate
        self.bullet_speed = Bullet_speed

        self.has_entered = False
        self.has_collided = False
        self.collidewith = []
        self.index = 0
        self.iframe = 0

        self.BB = BotBullets
        self.score = score
    
    # Loops through frames
    def animate(self, frame_count):
        self.frame += 0.1 # incrementing to slow down animation
        if self.frame > len(self.sprites) - 1:
            self.frame = 0
        
        self.animate_hit(frame_count)
        self.image = self.sprites[int(self.frame)]
        self.hit_sprite = self.hit_sprites[int(self.frame)]

    # Highlight when bot is hit with bullet
    def animate_hit(self, frame_count):
        if len(self.collidewith) > self.index:
            self.index += 1
            self.iframe = frame_count
            for sprite in self.sprites:
                sprite.set_alpha(0)

        if  frame_count - self.iframe >= 2:
            for sprite in self.sprites:
                sprite.set_alpha(255)

    # Check & get current pos
    def check_pos(self, target_pos):
        if self.pos[0] < target_pos[0]:
            self.sprite_rot = pygame.transform.flip(self.image, 1, 0)
            self.hit_sprite_rot = pygame.transform.flip(self.hit_sprite, 1, 0)
        else:
            self.sprite_rot = self.image
            self.hit_sprite_rot = self.hit_sprite

    ## Unique Method ##
    def set_vector(self, d, increment):
        opp_1 = math.sin(math.radians(-d[1] - increment))
        adj_1 = math.cos(math.radians(-d[0] - increment))
        return (adj_1, opp_1)

    def fire_at_player(self, bot_projectiles):
        if not self.has_entered:
            if self.screen.get_rect().collidepoint(self.rect.center):
                self.has_entered = True
                self.last_fired = pygame.time.get_ticks()

        if pygame.time.get_ticks() - self.last_fired > 1/self.fire_rate *1000:
            increment = 0
            for i in range(8):
                bot_projectiles.add(self.BB(self.screen, self.rect.center, self.set_vector(self.dirvect, increment),
                                            self.bullet_speed, bot_projectiles))
                increment += 45
            
            self.last_fired = pygame.time.get_ticks()

    # Follow player method
    def track_player(self,target_pos):
        self.dirvect = (pygame.math.Vector2(target_pos) - self.pos).normalize()
        self.pos += self.dirvect * self.speed
        self.rect.center = round(self.pos.x),round(self.pos.y)
        self.sprite_rect = self.image.get_rect(center = self.pos)

    def update(self,target_pos,frame_count,bot_projectile):
        self.track_player(target_pos) # Move to player
        self.animate(frame_count)
        self.check_pos(target_pos)
        self.fire_at_player(bot_projectile)

    def draw(self, screen):
        screen.blit(self.hit_sprite_rot, self.sprite_rect)
        screen.blit(self.sprite_rot, self.sprite_rect)
        '''pygame.draw.circle(screen,"Purple",self.rect.center,10,3)'''