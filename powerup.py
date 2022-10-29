import pygame

from settings import *
import random

# temporary -> each powerup will have a unique color


# can make Powerup base class where different types of powerups extend this class
class Powerup(pygame.sprite.Sprite):

    # pos = position
    # group = sprite group
    def __init__(self, size, pos, color, group):
        super().__init__(group)
        self.image = pygame.Surface(size)
        self.image.fill(color)
        self.color = color
        self.rect = self.image.get_rect(topleft=pos)
        self.vector = pygame.math.Vector2()
        
    # Generates random y-axis bounds = (below score -> bottom of screen)
    def randomizeHeight(self):
        randomHeight = random.randrange(15 + POWERUP_SIZE[1], HEIGHT - POWERUP_SIZE[1])
        return randomHeight

    def changeHeight(self):
        self.image = pygame.Surface(POWERUP_SIZE)
        self.color = random.choice(COLOR_LIST)
        self.image.fill(self.color)
        new_size = ((WIDTH - POWERUP_SIZE[0]) /2 , (self.randomizeHeight()))
        self.rect = self.image.get_rect(topleft = new_size)

    # Easy way to handle "kill" sprite by moving it offscreen until powerup height resets
    def moveOffscreen(self):
        self.image = pygame.Surface(POWERUP_SIZE)
        color = random.choice(COLOR_LIST)
        self.image.fill(color)
        new_size = ((WIDTH + POWERUP_SIZE[0]  + 1) , (HEIGHT + POWERUP_SIZE[1] + 1)) #offscreen location
        self.rect = self.image.get_rect(topleft = new_size)