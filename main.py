# main shiz

import pygame
from sys import exit

from settings import Settings
from sprites import Cursor, Player, Bots
from bullet import Bullet, Cannon
from handler import BotHandler

# main loop

class Main:
    # main init
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock() # ding ding ding tu tutu tutu  young fly on the track
        self.gs = Settings() # game settings
        self.screen = pygame.display.set_mode((self.gs.SCREENWIDTH,self.gs.SCREENHEIGHT))
        self.surface1 = pygame.surface.Surface((self.gs.SCREENWIDTH,self.gs.SCREENHEIGHT))
        self.frame_count = 0
        self.load_main()

    # load sprites,groups,methods,handlers,etc
    def load_main(self):
        # groups
        self.bg = pygame.sprite.Group() # bullet group
        self.bots_1 = pygame.sprite.Group() # bot group 1
    
        # Handlers and checkers
        self.bh = BotHandler(self.screen, self.gs.SCREENSIZE, Bots, self.bots_1, self.gs.bot_speed, self.gs.bot_max_count, self.gs.bot_spawn_rate)

        self.player = Player(self.screen,"sprites/player_ship.png",self.gs.start_pos,self.gs.player_speed,self.gs.focus_speed,self.gs.shield)
        self.cannon = Cannon(self.screen, Bullet, self.bg, self.gs.max_bullet_count )


    # load highscores, settings, yo mama
    def __load_save(self):
        return True

    # self explanatory
    def display_update(self):
        self.surface1.fill("White")
        self.screen.blit(self.surface1,(0,0))

        self.player.update()
        self.player.draw()

        self.bh.spawn_bot(self.time_now)
        self.bh.update_bot(self.player.center)

        self.cannon.get_dirvect(self.player.dir)
        if self.frame_count % 1 == 0:
            self.cannon.fire_cannon(self.player.rect.center)

        for bullet in self.bg:
            bullet.update()
            if not self.screen.get_rect().collidepoint(bullet.player_pos):
                self.bg.remove(bullet)
                
        for bullet in self.bg:
            bullet.draw(self.screen)
        
    # main loop
    def run(self):
        while True:
            self.time_now = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            
            self.display_update()
            self.clock.tick(self.gs.tps)
            pygame.display.flip()
            self.frame_count += 1

        return True
    
if __name__ == "__main__":
    main = Main()
    main.run()
    exit()
