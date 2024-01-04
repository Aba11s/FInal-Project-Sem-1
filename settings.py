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

        self.tps = 120

    def __init_gv(self):
        self.start_pos = (self.SCREENWIDTH//2,self.SCREENHEIGHT//2) #Center start
        self.player_speed = 1.5
        self.focus_speed = 1

        self.max_bullet_count = 300

        self.shield = 0
        self.max_shield = 3
        self.invincible_time = 2 #seconds

        self.bot_spawn_area = (self.SCREENWIDTH*1.5,self.SCREENHEIGHT*1.5)
        self.bot_pos= self.start_pos
        self.bot_speed = 0.6
        self.bot_max_count = 100
        self.bot_spawn_rate = 2

        self.dm = 1.0
    


    