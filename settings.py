# Settings

import pygame

class Settings:
    def __init__(self):
        self.__init_gs()
        self.__init_gv()

    def __init_gs(self):
        # display settings
        self.SCREENWIDTH = 1366
        self.SCREENHEIGHT = 768
        self.SCREENSIZE = (self.SCREENWIDTH,self.SCREENHEIGHT)

        self.tps = 60

    def __init_gv(self):
        # Player
        self.start_pos = (self.SCREENWIDTH//2,self.SCREENHEIGHT//2) #Center start
        self.player_speed = 4
        self.focus_speed = 2
        self.speed_mp = 1.0 # speed multiplier

        self.player_lives = 3
        self.shield = 0
        self.max_shield = 3 
        self.invincible_time = 2 #seconds

        # Weapons
        # default
        self.bullet_speed_d = 10
        self.bullet_dmg_d = 10
        self.bullet_pen_d = 4
        self.bullet_count_d = 30
        self.fire_rate_d = 5
        self.reload_time_d = 2000 
        
        # rapid
        self.bullet_speed_r = 16
        self.bullet_dmg_r = 5
        self.bullet_pen_r = 1
        self.bullet_count_r = 100
        self.fire_rate_r = 15
        self.reload_time_r = 4200

        # spread (shotgun)
        self.bullet_speed_s = 16
        self.bullet_dmg_s = 20
        self.bullet_pen_s = 5
        self.bullet_count_s = 10
        self.fire_rate_s = 1.1
        self.reload_time_s = 1300
        self.lifetime_s = 750
        self.slow_mp = 0.010

        # Bots
        self.bot_spawn_area = (self.SCREENWIDTH*1.5,self.SCREENHEIGHT*1.5)
        self.bot_pos= self.start_pos
        
        # Default
        self.bot_speed = 1.6
        self.bot_speed_mp = 1.0
        self.bot_max_count = 100
        self.bot_spawn_rate = 2
        self.bot_hitpoints = 40
        self.bot_score_1 = 100

        # Ranged
        self.bot_speed_2 = 0.6
        self.bot_speed_mp_2 = 1.0
        self.bot_max_count_2 = 30
        self.bot_spawn_rate_2 = 0.75
        self.bot_hitpoints_2 = 40
        self.bot_fire_rate_2 = 0.3
        self.bot_bullet_speed_2 = 4
        self.bot_score_2 = 300

        # Big - DEPRACATED for now
        self.bot_speed_3 = 1
        self.bot_speed_mp_3 = 1.0
        self.bot_max_count_3 = 6
        self.bot_spawn_rate_3 = 0.1
        self.bot_hitpoints_3 = 150

        self.dm = 1.0 # difficulty multiplier
    

class Score():
    def __init__(self, score,  highscore, score_mp = 1.0):
        self.score = score
        self.highscore = highscore
    
    def add_score(self, score):
        self.score += score
    