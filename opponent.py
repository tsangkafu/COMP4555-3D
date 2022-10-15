import pygame
import random
from settings import *

class Opponent(pygame.sprite.Sprite):
    # pos = position
    # group = sprite group
    def __init__(self, size, pos, color, group):
        super().__init__(group)
        self.name = "opponent"
        self.score = 0
        self.speed = 7
        self.image = pygame.Surface(size)
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft = pos)

    def update(self):
        # set border
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT


    def updateColor(self, color):
        #theme color change
        self.image.fill(color)

    def chase_ball(self, ball):
        if self.rect.top < ball.rect.top:
            self.rect.y += self.speed
        if self.rect.top > ball.rect.bottom:
            self.rect.y -= self.speed
            