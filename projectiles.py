import pygame
from pygame.sprite import Sprite
import math

# Player Projectile
class PlayerProjectile(Sprite):
    def __init__(self, screen, player_pos, dirvect, bullet_speed, bullet_hp, bullet_dmg, lifetime = None, time_fired = None, slow_mp = 0):
        Sprite.__init__(self)
        self.screen = screen
        self.image = pygame.image.load("sprites/bullet_projectile-1.png").convert_alpha()

        self.player_pos = player_pos
        self.x = self.player_pos[0]
        self.y = self.player_pos[1]
        self.dirvect = dirvect

        self.bullet = pygame.Surface((6,6))
        self.rect = self.bullet.get_rect(center = self.player_pos)
        self.hp = bullet_hp
        self.dmg = bullet_dmg

        self.speed = bullet_speed
        self.slow_mp = slow_mp
        self.vel_mp = 1

        self.collidewith = []
        self.check_lifetime(lifetime, time_fired)
        self.rotate()

    def rotate(self):
        self.angle = math.degrees(math.atan2(*self.dirvect)) - 90
        self.rot_sprite = pygame.transform.rotozoom(self.image, self.angle, 0.75)

    def set_vel(self):
        self.vel_mp = max((self.vel_mp - self.slow_mp), 0)

    def move(self):
        self.x += self.dirvect[0] * self.speed * self.vel_mp
        self.y += self.dirvect[1] * self.speed * self.vel_mp
        self.pos = (self.x,
                    self.y)
        
        self.rect = self.bullet.get_rect(center = self.pos) 
        self.rect_rot = self.rot_sprite.get_rect(center = self.pos)

    def check_lifetime(self, lifetime, time_fired):
        if lifetime:
            self.has_lifetime = True
            self.lifetime = lifetime
            self.time_fired = time_fired
        else:
            self.has_lifetime = False

    def kill_conditions(self):
        if self.hp <= 0:
            self.kill()
        if self.has_lifetime:
            if pygame.time.get_ticks() - self.time_fired > self.lifetime:
                self.kill()
        if not self.screen.get_rect().collidepoint(self.pos):
            self.kill()

    def update(self):
        self.set_vel()
        self.move()
        self.kill_conditions()
        
    def draw(self, screen):
        screen.blit(self.rot_sprite, self.rect_rot)
        '''pygame.draw.circle(screen,"Orange",self.rect.center,6,3) '''


# Bots projectile
class BotProjectile(Sprite):
    def __init__(self, screen, bot_pos, dirvect, bullet_speed, bot_projectiles):
        Sprite.__init__(self)
        self.screen = screen
        self.image = pygame.image.load("sprites/bot_projectile.png")
        self.image = pygame.transform.rotozoom(self.image, 0, 0.75)

        self.spawn_pos = bot_pos
        self.pos = bot_pos
        self.x = bot_pos[0]
        self.y = bot_pos[1]
        self.dirvect = dirvect

        self.bullet = pygame.Surface((6,6))
        self.rect = self.bullet.get_rect(center = bot_pos)
        self.speed = bullet_speed

    def move(self):
        self.x += self.dirvect[0] * self.speed
        self.y += self.dirvect[1] * self.speed
        self.pos = (self.x,
                    self.y)
        
        self.rect = self.bullet.get_rect(center = self.pos)
        self.rect_sprite = self.image.get_rect(center = self.pos)
    
    def kill_conditions(self):
        if not self.screen.get_rect().collidepoint(self.pos):
            self.kill()

    def update(self):
        self.kill_conditions()
        self.move()

    def draw(self, screen):
        screen.blit(self.image, self.rect_sprite)
        '''pygame.draw.circle(screen,"Red",self.rect.center,6,3)'''