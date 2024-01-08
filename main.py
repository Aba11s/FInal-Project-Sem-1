# main shiz

import pygame
from sys import exit

from settings import Settings, Score
from scene import SceneManager, Menu, Stage
from player import CameraGroup, Cursor, Player
from weapons import Cannon, CannonDefault, CannonRapid, CannonSpread
from projectiles import PlayerProjectile as Bullet, BotProjectile
from bots import Bots, BotsBig, BotsRanged
from handler import BotHandler, Collisions
from interface import UI
from Particles import Particles

# main loop

class Main:
    # main init
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("FORTNITRE")
        self.clock = pygame.time.Clock() # ding ding ding tu tutu tutu  yung fly on the track
        self.gs = Settings() # game settings
        self.screen = pygame.display.set_mode((self.gs.SCREENWIDTH,self.gs.SCREENHEIGHT))
        self.surface1 = pygame.surface.Surface((self.gs.SCREENWIDTH,self.gs.SCREENHEIGHT))
        self.Score = Score()
        # Loads highscore from score.dat
        self.Score.import_highscore()
        self.frame_count = 0

        self.UI = UI(self.screen, self.gs.SCREENSIZE)
        self.load_scenes()

    #Init Scenes
    def load_scenes(self):
        self.SceneManager = SceneManager('Menu')
        self.Menu = Menu(self.screen, self.SceneManager, self.gs, self.UI, self.Score) # Menu screen
        self.Stage = Stage(self.screen, self.SceneManager) # Stage / Gameplay screen
        
        self.scenes = {'Menu':self.Menu, 'Stage':self.Stage}

    def load_stage(self):
        self.Stage.load_main(self.gs, self.Score, CameraGroup, Cursor, Player, Bots, BotsRanged, BotsBig, 
                           Cannon, CannonDefault, CannonRapid, CannonSpread, Bullet, BotProjectile,
                           BotHandler, Collisions, UI, Particles)

    # main loop
    def run(self):
        while True:
            self.real_time = pygame.time.get_ticks()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.SceneManager.get_scene() == 'Stage':
                            self.Stage.pause = not self.Stage.pause

            if self.Menu.load_stage:
                self.load_stage()
                self.Menu.load_stage = False
            self.scenes[self.SceneManager.get_scene()].run()

            self.clock.tick(self.gs.tps)
            pygame.display.flip()

          


    
if __name__ == "__main__":
    main = Main()
    main.run()
    exit()
