from turtle import speed
import pygame
from settings import *

class Ball(pygame.sprite.Sprite):
    # pos = position
    # group = sprite group
    def __init__(self, radius, pos, color, group):
        super().__init__(group)
        self.radius = radius
        self.speed = 7
        self.image = pygame.Surface((self.radius * 2, self.radius * 2))
        self.rect = self.image.get_rect(topleft = pos)
        pygame.draw.circle(self.image, color, (self.radius, self.radius), self.radius)
        self.velocity = [self.speed, self.speed]

    def update(self):


        self.rect.x += self.velocity[0] 
        self.rect.y += self.velocity[1] 

        if self.rect.x < 0:
            self.velocity[0] = -self.velocity[0]
        elif self.rect.x >= 1280 - (self.radius + 15):
             self.velocity[0] = -self.velocity[0]
        if self.rect.y < 0:
            self.velocity[1] = -self.velocity[1] 
        elif self.rect.y >= 960 - (self.radius + 15):
            self.velocity[1] = -self.velocity[1] 

        