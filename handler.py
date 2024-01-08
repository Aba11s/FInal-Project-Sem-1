#Game handlers and chekers

import pygame
import random


# Status checkers
# Collision checker

class Collisions():
    def __init__(self, player_group, bullet_group, bot_group, ranged_group, big_group, bp):
        self.player_group = player_group
        self.bullets = bullet_group
        self.bots = bot_group
        self.ranged = ranged_group
        self.big = big_group
        self.bp = bp
        ...
    
    def check_bullet_bot_collisions(self):
        collision = pygame.sprite.groupcollide(self.bullets, self.bots, False, False)
        for bullet, bot_list in collision.items():
            for bot in bot_list:  
                # Prevents bot and bullet from colliding more than once - theres probably a more efficient way *shrugs
                if bullet not in bot.collidewith:
                    bot.hp -= bullet.dmg
                    bot.collidewith.append(bullet)
                if bot not in bullet.collidewith:
                    bullet.hp -= 1
                    bullet.collidewith.append(bot)
    
    def check_bullet_ranged_collisions(self):
        collision = pygame.sprite.groupcollide(self.bullets, self.ranged, False, False)
        for bullet, bot_list in collision.items():
            for bot in bot_list:   
                # Prevents bot and bullet from colliding more than once - theres probably a more efficient way *shrugs
                if not bot.has_collided:
                    bot.has_collided = True
                if bullet not in bot.collidewith:
                    bot.hp -= bullet.dmg
                    bot.collidewith.append(bullet)
                if bot not in bullet.collidewith:
                    bullet.hp -= 1
                    bullet.collidewith.append(bot)
    
    def check_player_bot_collision(self):
        collision = pygame.sprite.groupcollide(self.player_group, self.bots, False, False)
        for collideitem in collision.items():
            if not collideitem[0].invincible:
                collideitem[0].hit()

        collision2 = pygame.sprite.groupcollide(self.player_group, self.ranged, False, False)
        for collideitem2 in collision2.items():
            if not collideitem2[0].invincible:
                collideitem2[0].hit()

    def check_player_projectile_collision(self):
        collision = pygame.sprite.groupcollide(self.player_group, self.bp, False, False)
        for collideitem in collision.items():
            if not collideitem[0].invincible:
                collideitem[0].hit()

    def check_all_collisions(self):
        self.check_bullet_bot_collisions()
        self.check_player_bot_collision()
        self.check_bullet_ranged_collisions()
        self.check_player_projectile_collision()
            

# Bot Handler
class BotHandler(): 
    def __init__(self,screen,screensize,bot_speed,spawn_rate,Score,Bots,BotsRanged,BotsBig, camera_group, bot_group, ranged_group, big_group, bot_projectiles):
        self.screen = screen
        self.sw = screensize[0]
        self.sh = screensize[1]

        self.bot_speed = bot_speed
        self.spawn_rate = spawn_rate
        self.next_spawn_time = 0

        self.Score = Score
        self.Bots = Bots
        self.BotsR = BotsRanged
        self.BotsB = BotsBig

        self.cg = camera_group
        self.bot_group = bot_group
        self.ranged_group = ranged_group
        self.big_group = big_group

        self.bot_projectiles = bot_projectiles
        self.last_spawned_d = 0
        self.last_spawned_r = 0
        self.last_spawned_b = 0

        self.set_spawn_range()
    
    # spawns normal bots - old *will fix maybe*
    def spawn_default_bot(self,time_now,hitpoints, bot_cap_default, default_score):
        delay = (1/self.spawn_rate)*1000 # in milliseconds
        if time_now >= self.next_spawn_time or len(self.bot_group) == 0:
            if len(self.bot_group) < bot_cap_default:
                new_bot = self.Bots(self.screen, self.bot_speed, self.set_spawn(), hitpoints, default_score)
                self.bot_group.add(new_bot)
                self.cg.add(new_bot)
                self.next_spawn_time = time_now + delay

    # Spawns ranged bots - new
    def spawn_ranged_bot(self, bot_speed, hitpoints, fire_rate, bullet_speed, spawn_rate, ranged_bot_cap, BotBullets, ranged_score):
        delay = (1/spawn_rate)*1000
        if pygame.time.get_ticks() - self.last_spawned_r > delay:
            print(pygame.time.get_ticks(),self.last_spawned_r, delay)
            if len(self.ranged_group) < ranged_bot_cap:
                new_bot = self.BotsR(self.screen, bot_speed, self.set_spawn(), hitpoints, fire_rate, bullet_speed, BotBullets, ranged_score)
                self.ranged_group.add(new_bot)
                self.cg.add(new_bot)
                self.last_spawned_r = pygame.time.get_ticks()

    def update_bot(self,player_pos,frame_count):
        for bot in self.bot_group:
            bot.update(player_pos,frame_count)
            if bot.hp <= 0:
                self.Score.add_score(bot.score)
                bot.kill()

        for bot in self.ranged_group:
            bot.update(player_pos, frame_count,self.bot_projectiles)
            if bot.hp <= 0:
                self.Score.add_score(bot.score)
                bot.kill()


    # Set spawn range within 1.5x width and height of screen offscreen
    def set_spawn_range(self):
        self.range_x = [x for x in range(0 - 200 , self.sw + 200)]
        self.range_y = [y for y in range(0 - 200 , self.sh + 200)]
        self.range_x_exc = [x for x in self.range_x if x not in range(0,self.sw)]
        self.range_y_exc = [y for y in self.range_y if y not in range(0,self.sh)]

    # Chooses spawnpoint
    def set_spawn(self):
        if random.randint(0,1):
            return (random.choice(self.range_x_exc), random.choice(self.range_y))
        else:
            return (random.choice(self.range_x), random.choice(self.range_y_exc))
        



            