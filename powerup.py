import pygame

from settings import *
import random

# global variables? cant seem to put inside of class
POWERUP_SIZE = (50, 50)
POWERUP1_COLOR = (200, 0, 200)
POWERUP2_COLOR = (255, 255, 0)
POWERUP3_COLOR = (0, 255, 255)

# temporary -> each powerup will have a unique color
color_list = [POWERUP1_COLOR,POWERUP2_COLOR,POWERUP3_COLOR]

# can make Powerup base class where different types of powerups extend this class
class Powerup(pygame.sprite.Sprite):

    # pos = position
    # group = sprite group
    def __init__(self, size, pos, color, group):
        super().__init__(group)
        self.image = pygame.Surface(size)
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=pos)
        self.vector = pygame.math.Vector2()
        
    #Generates random y-axis bounds = (below score -> bottom of screen)
    def randomizeHeight(self):
        randomHeight = random.randrange(
        15 + POWERUP_SIZE[1], HEIGHT - POWERUP_SIZE[1]
        )
        return randomHeight

    def changeHeight(self):
        self.image = pygame.Surface(POWERUP_SIZE)
        color = random.choice(color_list)
        self.image.fill(color)
        new_size = ((WIDTH - POWERUP_SIZE[0]) /2 , (self.randomizeHeight()))
        self.rect = self.image.get_rect(topleft = new_size)