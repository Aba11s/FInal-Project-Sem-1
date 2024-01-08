# Particles - DEPRACATED, NOT IN USE FOR THE MOMENT
import pygame
from pygame.sprite import Sprite
from random import uniform, randint

class Particles:
    def __init__(self, 
                 groups: pygame.sprite.Group, 
                 pos: tuple[int], 
                 color: str,):

        super().__init__(groups)
        self.pos = pos
        self.color = color
        self.direction = self.set_direction()
        self.speed = self.set_speed
    
    def create_surf(self):...

    def set_direction(self):
        return pygame.math.Vector2(uniform(-1,1), uniform(-1,1)).normalize()
    
    def set_speed(self):
        return randint(50,100)
    
    def move(self):
        self.pos += self.direction * self.speed
        self.rect.center = self.pos

    def update(self):
        self.move()

