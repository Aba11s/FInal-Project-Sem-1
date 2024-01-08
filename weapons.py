#Bullet Classes
import pygame
import math
import random
from pygame.sprite import Sprite

# Cannon
class Cannon():
    def __init__(self, screen, CannonDefault, CannonRapid, CannonSpread):
        self.screen = screen
        self.CannonDefault = CannonDefault
        self.CannonRapid = CannonRapid
        self.CannonSpread = CannonSpread
        self.type = 1
        self.level = 2 # Depracated - not in use currently
    # Cannon updates
    def set_angle(self, target, angle):
        self.target = target
        self.dist = math.hypot(*self.target)
        if not self.dist:
            self.dirvect = (0,1)
        else:
            self.dirvect = (self.target[0]/self.dist, self.target[1]/self.dist)

        self.angle = angle + 90 # +90 degree correction

    def fire(self, player_pos):
        if pygame.mouse.get_pressed()[2]:
            if self.CannonDefault.is_active:
                self.CannonDefault.fire(self.angle, self.dirvect, player_pos, True)
            elif self.CannonRapid.is_active:
                self.CannonRapid.fire(self.angle, player_pos,True)
            elif self.CannonSpread.is_active:
                self.CannonSpread.fire(self.angle, player_pos, True)
        elif pygame.mouse.get_pressed()[0]:
            if self.CannonDefault.is_active:
                self.CannonDefault.fire(self.angle, self.dirvect, player_pos)
            elif self.CannonRapid.is_active:
                self.CannonRapid.fire(self.angle, player_pos)
            elif self.CannonSpread.is_active:
                self.CannonSpread.fire(self.angle, player_pos)
            
        

        self.last_fire = pygame.time.get_ticks() # updates time when fired

    # Sets which weapons is currently active
    def set_active(self):
        if pygame.key.get_pressed()[pygame.K_1]:
            self.type = 1
            self.CannonDefault.is_active = True
            self.CannonRapid.is_active = False
            self.CannonSpread.is_active = False
        elif pygame.key.get_pressed()[pygame.K_2]:
            self.type = 2
            self.CannonDefault.is_active = False
            self.CannonRapid.is_active = True
            self.CannonSpread.is_active = False
        elif pygame.key.get_pressed()[pygame.K_3]:
            self.CannonDefault.is_active = False
            self.CannonRapid.is_active = False
            self.CannonSpread.is_active = True
            self.type = 3

    def update(self, target, angle, player_pos):
        self.set_active()
        self.set_angle(target, angle)
        self.fire(player_pos)



# Default cannon - removed ammo limit
class CannonDefault():
    def __init__(self, screen, Bullet, bullet_group, bullet_speed, fire_rate_d, bullet_count_d, bullet_dmg, bullet_pen_d, reload_time_d):
        self.screen = screen
        self.Bullet = Bullet
        self.bg = bullet_group
        self.is_active = True

        self.fire_rate = fire_rate_d
        self.max_bullets = bullet_count_d
        self.bullet_count = self.max_bullets
        self.bullet_speed = bullet_speed
        self.dmg = bullet_dmg
        self.hp = bullet_pen_d

        self.reload_time = reload_time_d
        self.last_reload = 0
        self.is_reloading = False
        self.last_fired = 0

        self.d = 5

    # 10 deg angle calculations
    def set_dirvects(self, angle, d):
        opp_1 = math.sin(math.radians(-d - angle))
        adj_1 = math.cos(math.radians(-d - angle))
        opp_2 = math.sin(math.radians(d - angle))
        adj_2 = math.cos(math.radians(d - angle))
        self.dv_1_1 = (adj_1, opp_1)
        self.dv_1_2 = (adj_2, opp_2)

    # alt firing conditions
    def check_if_alt(self, alt):
        if not alt:
            self.f_d = self.d
        else:
            self.f_d = self.d / 2

    # Spawns bullet to bullet group
    def spawn_bullet(self, angle, dirvect, player_pos, alt):
        self.check_if_alt(alt)
        if self.bullet_count and not self.is_reloading:
            if pygame.time.get_ticks() - self.last_fired > 1/self.fire_rate * 1000:
                self.set_dirvects(angle, self.f_d)
                self.bg.add(self.Bullet(self.screen, player_pos, dirvect, self.bullet_speed, self.hp, self.dmg))
                self.bg.add(self.Bullet(self.screen, player_pos, self.dv_1_1, self.bullet_speed, self.hp, self.dmg))
                self.bg.add(self.Bullet(self.screen, player_pos, self.dv_1_2, self.bullet_speed, self.hp, self.dmg))
                self.last_fired = pygame.time.get_ticks()

    # fires bullet
    def fire(self, angle, dirvect, player_pos, alt = False):
        self.spawn_bullet(angle, dirvect, player_pos, alt)


# Rapid cannon
class CannonRapid():
    def __init__(self, screen, Bullet, bullet_group, bullet_speed_r, fire_rate_r, bullet_count_r, bullet_dmg_r, bullet_pen_r, reload_time_r):
        self.screen = screen
        self.Bullet = Bullet
        self.bg = bullet_group
        self.is_active = False

        self.fire_rate = fire_rate_r
        self.focus_mp = 2
        self.max_bullets = bullet_count_r
        self.bullet_count = self.max_bullets
        self.bullet_speed = bullet_speed_r
        self.dmg = bullet_dmg_r
        self.hp = bullet_pen_r
        self.pellets = 0

        self.reload_time_r = reload_time_r
        self.reload_time = reload_time_r
        self.last_reload = 0
        self.is_reloading = False
        self.last_fired = 0
        self.last_active = 0

        self.angle_max = 5
        self.angle_min = -5

            
    def set_vector(self, angle, dev_mp = 1):
        self.deviation = random.randint(self.angle_min, self.angle_max) * dev_mp
        opp = math.sin(math.radians(-self.deviation - angle))
        adj = math.cos(math.radians(-self.deviation - angle))
        return (adj, opp)

    def reload(self):
        self.reload_time = ((self.max_bullets - self.bullet_count) / self.max_bullets) * (self.reload_time_r) # Reload is proportional to how much ammo is used

    def update(self):
        if pygame.time.get_ticks() - self.last_fired > self.reload_time:
            self.bullet_count = self.max_bullets

    # Checks if alt-firing
    def check_if_alt(self, angle, alt):
        if not alt:
            self.f_fire_rate = self.fire_rate
            self.f_dmg = self.dmg
            self.set_angle = self.set_vector(angle)
        else: 
            self.f_fire_rate = self.fire_rate * 3
            self.f_dmg = self.dmg
            self.set_angle = self.set_vector(angle)
    
    # Adds bullet to bullet group
    def add_bullet(self, angle, player_pos, alt):
        self.check_if_alt(angle, alt)
        if self.bullet_count and not self.is_reloading:
            if pygame.time.get_ticks() - self.last_fired > 1/self.f_fire_rate*1000:
                self.bg.add(self.Bullet(self.screen, player_pos, self.set_angle, self.bullet_speed, self.hp, self.f_dmg))
                self.bg.add(self.Bullet(self.screen, player_pos, self.set_angle, self.bullet_speed, self.hp, self.f_dmg))
                self.bullet_count -= 1
                self.last_fired = pygame.time.get_ticks()


    def fire(self, angle, player_pos, alt = False):
        self.add_bullet(angle, player_pos, alt)
        self.reload()
        
# Spread cannon - removed ammo limit
class CannonSpread():
    def __init__(self, screen, Bullet, bullet_group, bullet_speed_s, fire_rate_s, bullet_count_s, bullet_dmg_s, bullet_pen_s, reload_time_s, lifetime_s, slow_mp):
        self.screen = screen
        self.Bullet = Bullet
        self.bg = bullet_group
        self.is_active = False

        self.fire_rate = fire_rate_s
        self.max_bullets = bullet_count_s
        self.bullet_count = self.max_bullets
        self.bullet_speed = bullet_speed_s
        self.slow_mp = slow_mp

        self.dmg = bullet_dmg_s
        self.hp = bullet_pen_s
        self.pellets = 8

        self.reload_time = reload_time_s
        self.last_reload = 0
        self.is_reloading = False
        self.last_fired = 0
        self.lifetime = lifetime_s

        self.angle_min = -10
        self.angle_max = 10
        self.angle_mp = 1.0
        self.vel_mp = 1.0

    def set_vector(self, angle, angle_mp = 1.0):
        deviation = random.uniform(self.angle_min * angle_mp, self.angle_max * angle_mp)
        opp = math.sin(math.radians(-deviation - angle))
        adj = math.cos(math.radians(-deviation - angle))
        return (adj, opp)
    
    def set_vel(self, vel_mp):
        vel_factor = random.uniform(-0.2, 0.2)
        return self.bullet_speed*vel_mp + (self.bullet_speed*vel_factor)
    
    def check_if_alt(self, angle, alt):
        if not alt:
            self.f_vel_mp = self.vel_mp
            self.f_slow_mp = self.slow_mp
            self.f_angle_mp = self.angle_mp
        else:
            self.f_vel_mp = self.vel_mp * 1.5
            self.f_slow_mp = 0
            self.f_angle_mp = self.angle_mp / 4

    
    def add_bullet(self, angle, player_pos, alt):
        self.check_if_alt(angle, alt)
        if self.bullet_count and not self.is_reloading:
            if pygame.time.get_ticks() - self.last_fired > 1/self.fire_rate*1000:
                self.last_fired = pygame.time.get_ticks()
                for i in range(self.pellets):
                    self.bg.add(self.Bullet(self.screen, player_pos, self.set_vector(angle, self.f_angle_mp), self.set_vel(self.f_vel_mp), self.hp, self.dmg, self.lifetime, self.last_fired, self.f_slow_mp))
    
    def fire(self, angle, player_pos, alt = False):
        self.add_bullet(angle, player_pos, alt)
    
