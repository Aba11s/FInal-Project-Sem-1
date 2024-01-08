# UI

import pygame
import random
from pygame.sprite import Sprite

class UI:
    def __init__(self, screen, SCREENSIZE,):
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.SCREENSIZE = SCREENSIZE
        self.SCREENWIDTH = self.SCREENSIZE[0]
        self.SCREENHEIGHT = self.SCREENSIZE[1]

        self.button = Button
        self.load_icons()
        self.load_fonts()

    # QOL method
    def get_key(self, val, dict):
        for key, value in dict.items():
            if val == value:
                return key
            
    def draw_text(self, screen, text, font, color, position):
        text = font.render(text, True, color)
        text_rect = text.get_rect(center = position)
        screen.blit(text, text_rect)

    # Load fonts
    def load_fonts(self):
        self.font_text = pygame.font.Font("font/silkscreen.ttf", 32)
        self.font_head = pygame.font.Font("font/silkscreen.ttf", 90)
        self.font_subhead = pygame.font.Font("font/silkscreen.ttf", 48)
        self.font_title = pygame.font.Font("font/silkscreen.ttf", 120)

    def load_icons(self):
        # Weapon Icon
        self.weapon_d = pygame.image.load("sprites/weapon_default.png").convert_alpha()
        self.weapon_r = pygame.image.load("sprites/weapon_rapid.png").convert_alpha()
        self.weapon_s = pygame.image.load("sprites/weapon_spread.png").convert_alpha()
        self.icon_dict = {self.weapon_d: 1, self.weapon_r: 2, self.weapon_s: 3}

        # Hearts
        self.hearts_icon = pygame.image.load("sprites/heart-1.png").convert_alpha()
        self.hearts_icon = pygame.transform.scale_by(self.hearts_icon, 2)

    def draw_weapon_icon(self, type):
        self.weapon_icon = self.get_key(type, self.icon_dict)
        self.weapon_icon.set_alpha(255)
        self.wi_rect = self.weapon_icon.get_rect()
        self.wi_rect.bottomleft = self.screen_rect.bottomleft
        self.screen.blit(self.weapon_icon, (self.wi_rect.x+10, self.wi_rect.y-10))

    # Draw Score on stage
    def draw_score(self, screen, score, font):
        self.draw_text(screen, str(score), font, "Black", (self.SCREENWIDTH // 2, 20))
    
    # Draw Menu Title
    def draw_title(self, screen, font):
        self.draw_text(screen, "FORTNITE", font, "White", (self.SCREENWIDTH // 2, 70))

    # Adds menu buttons
    def draw_menu_buttons(self):
        images = ["sprites/button_base-1.png","sprites/button_base-2.png"]
        self.menu_start_button = self.button(images, (self.SCREENWIDTH//2, 250), 2, "START", self.font_subhead)
        self.menu_exit_button = self.button(images, (self.SCREENWIDTH//2, 450), 2, "EXIT", self.font_subhead)
        return self.menu_start_button, self.menu_exit_button

    # Draw Pause Screen
    def draw_pause_title(self, screen, font):
        self.draw_text(screen, "PAUSED", font, "White", (self.SCREENWIDTH // 2, 70))

    # Adds menu buttons
    def draw_pause_buttons(self):
        images = ["sprites/button_base-1.png","sprites/button_base-2.png"]
        self.pause_restart_button = self.button(images, (self.SCREENWIDTH//2, 250), 2, "RESTART", self.font_subhead)
        self.pause_resume_button = self.button(images, (self.SCREENWIDTH//2, 500), 2, "RESUME", self.font_subhead)
        return self.pause_restart_button, self.pause_resume_button
    
    # Lose screen
    def draw_lose_title(self, screen, font, font2, font3, score):
         loser_text = ["You_Lost","You_Lost","You_Lost","You_Lost","You_Lost","You_Lost",
                       "Game_Over","Game_over","Game_over","Game_over","Game_over","Game_over",
                       "Nice_Try","Nice_Try","Nice_Try","Nice_Try","Nice_Try","Nice_Try",
                       "PRO TIP: DON\'T DIE"]
         self.draw_text(screen, random.choice(loser_text), font, "White", (self.SCREENWIDTH // 2, 180))
         self.draw_text(screen, "Final Score: " + str(score), font2, "White", (self.SCREENWIDTH // 2, 350))
         self.draw_text(screen, "Press Enter to continue", font3, "White", (self.SCREENWIDTH // 2, 520)) 

    # Hearts
    def draw_hearts(self, screen, lives):
        self.heart_rect = self.hearts_icon.get_rect()
        self.heart_rect.topleft = self.screen_rect.topleft
        for i in range(0, lives):
            screen.blit(self.hearts_icon, (self.heart_rect.x + (i*100) + 20, self.heart_rect.y + 20))

class Button():
    def __init__(self, images, position, scale, text, font):
        self.image = pygame.image.load(images[0])
        self.hover = pygame.image.load(images[1])
        width = self.image.get_width()
        height = self.image.get_height()
        self.image = pygame.transform.scale(self.image, (int(width*scale),int(height*scale)))
        self.hover = pygame.transform.scale(self.hover, (int(width*scale),int(height*scale)))
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.image_active = self.image
        self.clicked = False

        self.text = font.render(text, True, "White")
        self.text_rect = self.text.get_rect(center = self.rect.center)

    def update(self, mouse_pos):
        action = False
        if self.rect.collidepoint(mouse_pos):
            self.image_active = self.hover
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                self.clicked = True
                action = True
        else:
            self.image_active = self.image
        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False

        return action
        
    def draw(self, screen):
        screen.blit(self.image_active, (self.rect.x, self.rect.y))
        screen.blit(self.text, self.text_rect)