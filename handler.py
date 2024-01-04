#Game handlers and chekers

import pygame
import random

#Bot Handler
class BotHandler(): 
    def __init__(self,screen,screensize,Bots,bot_group,bot_speed,bot_max_count,spawn_rate):
        self.screen = screen
        self.sw = screensize[0]
        self.sh = screensize[1]

        self.Bots = Bots ; self.bot_group = bot_group
        self.bot_speed = bot_speed
        self.bot_max_count = bot_max_count
        self.spawn_rate = spawn_rate
        self.next_spawn_time = 0

        self.set_spawn_range()

    def spawn_bot(self,time_now):
        delay = (1/self.spawn_rate)*1000 # in milliseconds
        
        if time_now >= self.next_spawn_time or len(self.bot_group) == 0:
            if len(self.bot_group) < self.bot_max_count:
                new_bot = self.Bots(self.screen, self.bot_speed, self.set_spawn())
                self.bot_group.add(new_bot)
                self.next_spawn_time = time_now + delay
                print(f"BOT SPAWNED, t: {time_now} ms" )

    def update_bot(self,player_pos):
        for bot in self.bot_group:
            bot.update(player_pos)
            bot.draw(self.screen)

    def set_spawn_range(self):
        self.range_x = [x for x in range(0 - 200 , self.sw + 200)]
        self.range_y = [y for y in range(0 - 200 , self.sh + 200)]
        self.range_x_exc = [x for x in self.range_x if x not in range(0,self.sw)]
        self.range_y_exc = [y for y in self.range_y if y not in range(0,self.sh)]

    def set_spawn(self):
        if random.randint(0,1):
            return (random.choice(self.range_x_exc), random.choice(self.range_y))
        else:
            return (random.choice(self.range_x), random.choice(self.range_y_exc))