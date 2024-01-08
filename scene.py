# Scenes
import pygame
from sys import exit


### START MENU ###
class Menu():
    def __init__(self, screen, SceneManager,
                 Settings, UI, Score):
        self.screen = screen
        self.Score = Score
        self.SceneManager = SceneManager
        self.gs = Settings
        self.UI = UI

        self.surface = pygame.Surface(self.gs.SCREENSIZE)
        self.menu_buttons = self.UI.draw_menu_buttons()
        self.load_stage = False

        self.Score.import_highscore()
    
    def check_button_updates(self):
        for button in self.menu_buttons:
            button.draw(self.screen)
            if button == self.menu_buttons[0]:
                if button.update(self.mouse_pos):
                    self.SceneManager.set_scene('Stage')
                    self.load_stage = True
            elif button == self.menu_buttons[1]:
                if button.update(self.mouse_pos):
                    exit()

    def run(self):
        self.mouse_pos = pygame.mouse.get_pos()
        pygame.mouse.set_visible(True)
        self.surface.fill("Black")
        self.screen.blit(self.surface, (0,0))

        self.check_button_updates()
        self.UI.draw_title(self.screen, self.UI.font_title)
        self.UI.draw_highscore(self.screen, self.UI.font_text, self.Score.highscore)
        
### STAGE / GAMEPLAY SCENE ###
class Stage:
    def __init__(self, screen, SceneManager):
        self.screen = screen
        self.SceneManager = SceneManager

    def load_main(self, Settings, Score, Camera, Cursor, Player, Bots, Ranged, Big, Cannon, CannonD, CannonR, CannonS, Bullet, Projectile,
                 BotHandler, Collisions, UI, Particles):

        self.Score = Score
        self.gs = Settings

        ### Sprite Groups ###
        self.pg = pygame.sprite.Group() # player group
        self.bg = pygame.sprite.Group() # bullet group default
        self.bp = pygame.sprite.Group() # bot projectile group
        self.bots_1 = pygame.sprite.Group() # Standard bots
        self.bots_2 = pygame.sprite.Group() # Ranged bots
        self.bots_3 = pygame.sprite.Group() # Big bots

        ### Constructors ###
        # Player
        self.CameraGroup = Camera(self.screen)
        self.Cursor = Cursor()
        self.Player = Player(self.screen,self.gs.start_pos,self.gs.player_speed,self.gs.focus_speed,self.gs.player_lives, self.gs.shield,self.gs.SCREENSIZE)
        self.pg.add(self.Player)


        # Bots
        self.BotsDefault = Bots
        self.BotsRanged = Ranged
        self.BotsBig = Big
        
        # Weapons
        self.CannonDefault = CannonD(self.screen, Bullet, self.bg, self.gs.bullet_speed_d, self.gs.fire_rate_d, self.gs.bullet_count_d, self.gs.bullet_dmg_d, self.gs.bullet_pen_d, self.gs.reload_time_d)
        self.CannonRapid = CannonR(self.screen, Bullet, self.bg, self.gs.bullet_speed_r, self.gs.fire_rate_r, self.gs.bullet_count_r, self.gs.bullet_dmg_r, self.gs.bullet_pen_r, self.gs.reload_time_r)
        self.CannonSpread = CannonS(self.screen, Bullet, self.bg, self.gs.bullet_speed_s, self.gs.fire_rate_s, self.gs.bullet_count_s, self.gs.bullet_dmg_s, self.gs.bullet_pen_s, self.gs.reload_time_s, self.gs.lifetime_s, self.gs.slow_mp)
        
        self.Cannon = Cannon(self.screen, self.CannonDefault, self.CannonRapid, self.CannonSpread)

        # Projectiles
        self.Bullet = Bullet
        self.Projectile = Projectile

        # Handlers
        self.BotHandler = BotHandler(self.screen, self.gs.SCREENSIZE, self.gs.bot_speed, self.gs.bot_spawn_rate, self.Score, self.BotsDefault, self.BotsRanged, self.BotsBig, self.CameraGroup,self.bots_1, self.bots_2, self.bots_3, self.bp)
        self.Collisions = Collisions(self.pg, self.bg, self.bots_1, self.bots_2, self.bots_3, self.bp)

        # Sprites and UI
        self.UI = UI(self.screen, self.gs.SCREENSIZE)
        
        ### Variables ###
        self.surface1 = pygame.surface.Surface(self.gs.SCREENSIZE)
        self.overlay = pygame.surface.Surface(self.gs.SCREENSIZE)
        self.overlay2 = pygame.surface.Surface(self.gs.SCREENSIZE)

        self.background = pygame.image.load("sprites/fuzzy_sky_background.png").convert_alpha()
        self.background = pygame.transform.scale_by(self.background, 1.5)

        self.bg_music = pygame.mixer.Sound("sfx/apparitions_stalk_the_night.mp3") # Special Thanks to ZUN frfr
        self.bg_music.set_volume(0.6)
        self.lose_sfx = pygame.mixer.Sound("sfx/crowd_laughing.mp3")
        self.playing_music = False

        self.pause_buttons = self.UI.draw_pause_buttons()

        self.Score.import_highscore()
        self.score = 0
        self.frame_count = 0

        self.time_now = 0
        self.time_paused = 0
        self.pause = False

    def play_bg_music(self):
        if not self.playing_music:
            self.bg_music.play(-1)
            self.playing_music = True

    def player_hit_warning(self):
        if self.Player.is_hit:
            self.overlay2.fill("Red")
            self.overlay2.set_alpha(150)
            self.screen.blit(self.overlay2,(0,0))

    # Updates and Blits Buttons
    def check_button_updates(self):
        for button in self.pause_buttons:
            button.draw(self.screen)
            if button == self.pause_buttons[0]:
                if button.update(self.mouse_pos):
                    self.SceneManager.set_scene('Menu')
                    self.playing_music = False
                    self.bg_music.stop()
            elif button == self.pause_buttons[1]:
                if button.update(self.mouse_pos):
                    self.pause = False

    # Main updates
    def run(self):
        self.mouse_pos = pygame.mouse.get_pos()
        self.time_now = pygame.time.get_ticks()
        if not self.pause and self.Player.lives:
            self.play_bg_music()
            pygame.mouse.set_visible(False)

            self.time_now = pygame.time.get_ticks()
            self.surface1.fill("Yellow")
            self.screen.blit(self.surface1,(0,0))
            self.screen.blit(self.background, (0,0))


            # calls player updates
            self.Player.update()
            self.Player.draw(self.screen)

            # calls bot updates
            self.BotHandler.spawn_default_bot(self.time_now, self.gs.bot_hitpoints, self.gs.bot_max_count, self.gs.bot_score_1)
            self.BotHandler.spawn_ranged_bot(self.gs.bot_speed_2, self.gs.bot_hitpoints_2, self.gs.bot_fire_rate_2, self.gs.bot_bullet_speed_2, 
                                             self.gs.bot_spawn_rate_2, self.gs.bot_max_count_2, self.Projectile, self.gs.bot_score_2)
            self.BotHandler.spawn_big_bot(self.gs.bot_speed_3, self.gs.bot_hitpoints_3, self.gs.bot_fire_rate_3, self.gs.bot_bullet_speed_3,
                                          self.gs.bot_spawn_rate_3, self.gs.bot_max_count_3, self.Projectile, self.gs.bot_score_3)
            self.BotHandler.update_bot(self.Player.center, self.frame_count)

            # calls cannon & bullet updates
            self.Cannon.update(self.Player.dir, self.Player.angle, self.Player.rect.center)
            self.CannonRapid.update()
        
            # removes bullet if offscreen
            for bullet in self.bg:
                bullet.update()
                bullet.draw(self.screen)

            for bp in self.bp:
                bp.update()
                bp.draw(self.screen)

            '''self.camera_group.update(self.Player.rect.center, self.frame_count)'''
            self.CameraGroup.custom_draw(self.screen)

            self.Collisions.check_all_collisions()
            self.player_hit_warning()

            self.UI.draw_weapon_icon(self.Cannon.type)
            self.UI.draw_hearts(self.screen, self.Player.lives)
            self.UI.draw_score(self.screen, self.Score.score, self.UI.font_text)

            self.Cursor.update()
            self.Cursor.draw(self.screen)
            
            self.frame_count += 1
            self.switched = False

        # Pauses Game
        else:
            if self.Player.lives:
                pygame.mouse.set_visible(True)
                # Pause Screen Overlay
                if not self.switched: #Ensures only blitted once
                    self.overlay.fill("Black")
                    self.overlay.set_alpha(180)
                    self.screen.blit(self.overlay, (0,0))

                self.switched = True
                self.UI.draw_pause_title(self.screen, self.UI.font_head)
                self.check_button_updates()

            # Game  over seqeunce
            else:
                # Lose Screen Overlay
                pygame.mouse.set_visible(False)
                if not self.switched:
                    self.overlay.fill("Black")
                    self.overlay.set_alpha(180)
                    self.screen.blit(self.overlay, (0,0))
                    self.lose_sfx.play()

                    self.Score.set_highscore()
                    self.UI.draw_lose_title(self.screen, self.UI.font_head, self.UI.font_subhead, self.UI.font_text, self.Score.score, self.Score.highscore)
                
                self.switched = True
                if pygame.key.get_pressed()[pygame.K_RETURN]:
                    self.SceneManager.set_scene('Menu')
                    self.lose_sfx.stop()
                    self.bg_music.stop()
                    self.playing_music = False

### SCENEMANAGER ###
class SceneManager:
    def __init__(self, CurrentScene):
        self.CurrentScene = CurrentScene

    def get_scene(self):
        return self.CurrentScene
    
    def set_scene(self, Scene):
        self.CurrentScene = Scene


